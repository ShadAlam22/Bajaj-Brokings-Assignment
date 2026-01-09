# Trading API Wrapper SDK - Bajaj Broking Assignment

A lightweight, Python-based REST API wrapper that simulates core trading platform functionalities. This project implements instrument management, order placement, trade execution, and portfolio tracking with in-memory storage.

##  Project Overview

This SDK provides a simplified trading backend that allows users to:
- Browse available financial instruments across multiple exchanges
- Place market and limit orders with proper validation
- Track order status through different lifecycle stages
- View executed trades history
- Monitor portfolio holdings with real-time calculations

##  Architecture & Design

### Technology Stack
- **Framework:** FastAPI (modern, fast web framework)
- **Language:** Python 3.x
- **Data Validation:** Pydantic models
- **Storage:** In-memory dictionaries and lists
- **API Documentation:** Auto-generated Swagger UI

### Project Structure
```
BAJAJ_ASSIGNMENT/
├── app/
│   ├── instruments.py      # Instrument listing endpoints
│   ├── orders.py           # Order management and placement
│   ├── trades.py           # Trade execution records
│   ├── portfolio.py        # Portfolio calculation logic
│   ├── models.py           # Pydantic data models and enums
│   └── main.py             # FastAPI app initialization
├── test_api.py             # Automated API test suite
├── requirements.txt        # Python dependencies
├── README.md              # This file

```

### Key Design Decisions

**1. Modular Architecture**
Each domain (instruments, orders, trades, portfolio) is separated into its own module for better maintainability and scalability.

**2. Automatic Trade Generation**
When a market order is placed, the system automatically:
- Changes order status to EXECUTED
- Creates a corresponding trade record
- Updates portfolio calculations dynamically

**3. Dynamic Portfolio Calculation**
Portfolio holdings are computed on-the-fly from executed orders rather than maintaining separate storage, ensuring data consistency.

**4. Centralized Error Handling**
Global exception handler catches all errors and returns standardized error responses.

##  Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone or extract the project**
   ```bash
   cd BAJAJ_ASSIGNMENT
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API**
   - **Swagger UI:** http://127.0.0.1:8000/docs
   - **ReDoc:** http://127.0.0.1:8000/redoc
   - **Base API:** http://127.0.0.1:8000/api/v1

##  API Documentation

### Base URL
```
http://127.0.0.1:8000/api/v1
```

### 1. Instruments API

#### Get All Instruments
```http
GET /api/v1/instruments/
```

**Response:**
```json
[
  {
    "symbol": "AAPL",
    "exchange": "NASDAQ",
    "instrumentType": "EQUITY",
    "lastTradedPrice": 180.0
  },
  {
    "symbol": "GOOGL",
    "exchange": "NASDAQ",
    "instrumentType": "EQUITY",
    "lastTradedPrice": 2700.0
  },
  {
    "symbol": "NIFTY21JULFUT",
    "exchange": "NSE",
    "instrumentType": "FUTURE",
    "lastTradedPrice": 18000.0
  }
]
```

### 2. Orders API

#### Place a New Order
```http
POST /api/v1/orders/
Content-Type: application/json
```

**Request Body (Market Order):**
```json
{
  "symbol": "AAPL",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 10
}
```

**Request Body (Limit Order):**
```json
{
  "symbol": "AAPL",
  "orderType": "SELL",
  "orderStyle": "LIMIT",
  "quantity": 5,
  "price": 185.50
}
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "symbol": "AAPL",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 10,
  "price": 180.0,
  "status": "EXECUTED",
  "timestamp": "2026-01-09T10:30:45.123456"
}
```

**Validation Rules:**
- Quantity must be greater than 0
- Price is mandatory for LIMIT orders and must be > 0
- MARKET orders execute immediately
- LIMIT orders are placed for future execution

#### Get Order Status
```http
GET /api/v1/orders/{orderId}
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "symbol": "AAPL",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 10,
  "price": 180.0,
  "status": "EXECUTED",
  "timestamp": "2026-01-09T10:30:45.123456"
}
```

**Order Status Values:**
- `NEW` - Order created but not yet submitted
- `PLACED` - Order submitted to exchange (LIMIT orders)
- `EXECUTED` - Order completed (MARKET orders)
- `CANCELLED` - Order cancelled by user

### 3. Trades API

#### Get All Trades
```http
GET /api/v1/trades/
```

**Response:**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "orderId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "symbol": "AAPL",
    "quantity": 10,
    "price": 180.0,
    "timestamp": "2026-01-09T10:30:45.123456"
  }
]
```

### 4. Portfolio API

#### Get Portfolio Holdings
```http
GET /api/v1/portfolio/
```

**Response:**
```json
[
  {
    "symbol": "AAPL",
    "quantity": 10,
    "averagePrice": 180.0,
    "currentValue": 1800.0
  },
  {
    "symbol": "GOOGL",
    "quantity": 3,
    "averagePrice": 2700.0,
    "currentValue": 8100.0
  }
]
```

**Calculation Logic:**
- `quantity` = Total BUY quantity - Total SELL quantity
- `averagePrice` = Total investment / Current quantity
- `currentValue` = quantity × averagePrice

##  Testing

### Automated Test Suite

Run the comprehensive test suite:
```bash
python test_api.py
```

**Test Coverage:**
- ✅ Fetch all instruments
- ✅ Place market order (BUY)
- ✅ Place limit order (SELL)
- ✅ Check order status
- ✅ View executed trades
- ✅ View portfolio
- ✅ Error: Missing price for LIMIT order
- ✅ Error: Invalid quantity (≤ 0)

### Manual Testing with cURL

**1. Get Instruments:**
```bash
curl http://127.0.0.1:8000/api/v1/instruments/
```

**2. Place Market Order:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","orderType":"BUY","orderStyle":"MARKET","quantity":5}'
```

**3. Place Limit Order:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{"symbol":"GOOGL","orderType":"SELL","orderStyle":"LIMIT","quantity":2,"price":2800.0}'
```

**4. Get Order Status:**
```bash
curl http://127.0.0.1:8000/api/v1/orders/{orderId}
```

**5. View Trades:**
```bash
curl http://127.0.0.1:8000/api/v1/trades/
```

**6. View Portfolio:**
```bash
curl http://127.0.0.1:8000/api/v1/portfolio/
```

### Interactive Testing

Visit **http://127.0.0.1:8000/docs** for the Swagger UI interface where you can:
- View all endpoints with detailed schemas
- Test APIs directly from the browser
- See request/response examples
- Download OpenAPI specification

##  Assumptions & Limitations

### Assumptions
1. **Single User:** No authentication or multi-user support implemented
2. **In-Memory Storage:** All data is stored in memory and lost on server restart
3. **Instant Execution:** Market orders execute immediately at last traded price
4. **No Market Depth:** Price discovery uses simple last traded price
5. **Simplified States:** Limit orders move directly from PLACED to EXECUTED (manual simulation required)
6. **No Partial Fills:** Orders execute completely or not at all
7. **UTC Timestamps:** All timestamps are in UTC format

### Known Limitations
- No persistent database (data lost on restart)
- No real-time market data integration
- No order modification or cancellation endpoints
- No authentication/authorization
- No rate limiting or API quotas
- Portfolio doesn't track unrealized P&L
- No support for advanced order types (Stop-Loss, Trailing Stop, etc.)
- No websocket support for real-time updates

##  Bonus Features Implemented

 **Centralized Exception Handling:** Global error handler for consistent error responses

 **Swagger Documentation:** Auto-generated interactive API documentation

 **Unit Tests:** Comprehensive test suite covering success and error scenarios

 **Order Execution Simulation:** Market orders execute immediately with trade generation

 **Clean Code Structure:** Modular design with separation of concerns

 **Logging:** Basic logging setup for debugging

##  Configuration

### Environment Variables (Optional)
You can set these environment variables to customize the application:

```bash
export HOST=0.0.0.0
export PORT=8000
```

Then run:
```bash
uvicorn app.main:app --host $HOST --port $PORT --reload
```

##  Troubleshooting

**Issue: Port already in use**
```bash
# Change the port
uvicorn app.main:app --reload --port 8001
```

**Issue: Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Virtual environment not activating**
```bash
# Windows - use PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```


##  License

This project is created as an assignment submission for Bajaj Broking and is for educational purposes only.

---

