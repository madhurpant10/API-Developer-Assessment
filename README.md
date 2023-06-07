# API-Developer-Assessment
SteelEye API Developer technical test

Certainly! Here's a README file explaining the code for the Trade data REST API implemented using FastAPI:

## Trade Data API

This API provides endpoints to retrieve a list of trades, fetch a single trade by ID, search for trades, and filter trades based on various criteria. It is built using the FastAPI framework in Python.

### Requirements

- Python 3.7+
- FastAPI
- uvicorn (for running the API server)
- Pydantic (for defining data models)

### Installation

1. Clone the repository:

   ```
   git clone <repository_url>
   ```

2. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

3. Start the API server:

   ```
   uvicorn main:app --reload
   ```

   The API server will be accessible at http://localhost:8000.

### Endpoints

#### Fetching a list of trades

- **URL:** `/trades`
- **Method:** GET

This endpoint retrieves a list of trades.

#### Fetching a single trade by ID

- **URL:** `/trades/{trade_id}`
- **Method:** GET

This endpoint fetches a single trade by its ID.

#### Searching for trades

- **URL:** `/trades/search`
- **Method:** GET

This endpoint allows searching for trades using the provided search text. The search is performed across the fields `counterparty`, `instrumentId`, `instrumentName`, and `trader`.

#### Filtering trades

- **URL:** `/trades`
- **Method:** GET

This endpoint supports filtering trades based on the following query parameters:

- `asset_class`: Filters trades by asset class.
- `start`: Filters trades with a tradeDateTime greater than or equal to the specified date.
- `end`: Filters trades with a tradeDateTime less than or equal to the specified date.
- `min_price`: Filters trades with a tradeDetails price greater than or equal to the specified value.
- `max_price`: Filters trades with a tradeDetails price less than or equal to the specified value.
- `trade_type`: Filters trades by tradeDetails buySellIndicator (BUY or SELL).

#### Pagination and sorting

The `/trades` endpoint supports pagination and sorting. The following query parameters can be used:

- `page`: Specifies the page number (default: 1).
- `per_page`: Specifies the number of trades per page (default: 10).
- `sort_by`: Specifies the field to sort the trades by.
- `sort_desc`: Specifies whether to sort in descending order (default: False).

### Data Mocking

The API uses a mocked database interaction layer to store the trade data. The `Database` class provides methods for adding trades, retrieving trades by ID, searching trades, and filtering trades based on the provided criteria. The actual implementation of the database layer is left up to the user.

### Data Models

The API uses the following data models (defined using Pydantic) to represent the trade data:

- `Trade`: Represents a trade with properties such as ID, counterparty, instrument ID, instrument name, trader, asset class, trade date time, and trade details (price and buy/sell indicator).

### Examples

Here are some example API requests that can be made to interact with the Trade Data API:

- Fetch all trades: `GET /trades`
- Fetch a single trade by ID: `GET /trades/{trade_id}`
- Search for trades: `GET /trades/search?search=bob%20smith`
- Filter trades by asset class and date range: `GET /trades?asset_class=Equity&start=2023-01-01&end=2023-01-31`
-

 Filter trades by price range and trade type: `GET /trades?min_price=100.0&max_price=200.0&trade_type=BUY`
- Paginate and sort trades: `GET /trades?page=2&per_page=20&sort_by=instrumentName&sort_desc=true`

Please note that this API is a mock implementation and does not connect to a real database. The data is generated and stored within the API itself.

Feel free to explore the different endpoints and query parameters to retrieve, search, and filter trade data.
