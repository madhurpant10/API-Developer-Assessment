from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# Mocked database interaction layer
class Database:
    def __init__(self):
        self.trades = []

    def add_trade(self, trade):
        self.trades.append(trade)

    def get_trade_by_id(self, trade_id):
        for trade in self.trades:
            if trade.id == trade_id:
                return trade
        return None

    def search_trades(self, search_text):
        results = []
        for trade in self.trades:
            if (
                search_text.lower() in trade.counterparty.lower()
                or search_text.lower() in trade.instrumentId.lower()
                or search_text.lower() in trade.instrumentName.lower()
                or search_text.lower() in trade.trader.lower()
            ):
                results.append(trade)
        return results

    def filter_trades(
        self,
        asset_class: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        trade_type: Optional[str] = None,
    ):
        results = []
        for trade in self.trades:
            if (
                (not asset_class or trade.assetClass == asset_class)
                and (not start or trade.tradeDateTime >= start)
                and (not end or trade.tradeDateTime <= end)
                and (not min_price or trade.tradeDetails.price >= min_price)
                and (not max_price or trade.tradeDetails.price <= max_price)
                and (not trade_type or trade.tradeDetails.buySellIndicator == trade_type)
            ):
                results.append(trade)
        return results


db = Database()


# Schema models
class TradeDetails(BaseModel):
    price: float
    buySellIndicator: str


class Trade(BaseModel):
    id: int
    counterparty: str
    instrumentId: str
    instrumentName: str
    trader: str
    assetClass: str
    tradeDateTime: str
    tradeDetails: TradeDetails


# Endpoint to fetch a list of trades
@app.get("/trades")
def get_trades(
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_desc: Optional[bool] = Query(False, description="Sort in descending order"),
    asset_class: Optional[str] = Query(None, description="Asset class of the trade"),
    start: Optional[str] = Query(None, description="Minimum date for tradeDateTime field"),
    end: Optional[str] = Query(None, description="Maximum date for tradeDateTime field"),
    min_price: Optional[float] = Query(None, description="Minimum value for tradeDetails.price field"),
    max_price: Optional[float] = Query(None, description="Maximum value for tradeDetails.price field"),
    trade_type: Optional[str] = Query(None, description="Trade type (BUY or SELL)"),
):
    filtered_trades = db.filter_trades(
        asset_class=asset_class,
        start=start,
        end=end,
        min_price=min_price,
        max_price=max_price,
        trade_type=trade_type,
    )

    if sort_by:
        reverse = sort_desc
        filtered_trades = sorted(filtered_trades, key=lambda trade: getattr(trade, sort_by), reverse=reverse)

    total_trades = len(filtered_trades)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_trades = filtered_trades[start_index:end_index]

    return {
        "trades": paginated_trades,
        "total_trades": total_trades,
        "page": page,
        "per_page": per_page,
    }


# Endpoint to fetch a trade by id
@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: int):
    trade = db.get_trade_by_id(trade_id)
    if trade:
        return trade
    else:
        return {"message": "Trade not found"}


# Endpoint to search for trades
@app.get("/trades/search")
def search_trades(
    search_text: str = Query(..., min_length=1, description="Search text"),
):
    results = db.search_trades(search_text)
    if results:
        return results
    else:
        return {"message": "No matching trades found"}


# Add some example trades to the database
trade1 = Trade(
    id=1,
    counterparty="ABC Corp",
    instrumentId="ABC123",
    instrumentName="Stock A",
    trader="John Doe",
    assetClass="Equity",
    tradeDateTime="2023-01-01T10:00:00Z",
    tradeDetails=TradeDetails(price=100.0, buySellIndicator="BUY"),
)
trade2 = Trade(
    id=2,
    counterparty="DEF Inc",
    instrumentId="DEF456",
    instrumentName="Stock B",
    trader="Jane Smith",
    assetClass="Equity",
    tradeDateTime="2023-01-02T11:00:00Z",
    tradeDetails=TradeDetails(price=200.0, buySellIndicator="SELL"),
)
db.add_trade(trade1)
db.add_trade(trade2)
