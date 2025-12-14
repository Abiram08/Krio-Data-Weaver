# Data Weaver Dashboard

> Discover and visualize correlations between disparate data sources in real-time

A modern web application that analyzes statistical relationships between weather patterns and stock market movements using the Model Context Protocol (MCP) for external API integration.

## 🌟 Features

- **Real-time Data Fetching**: Fetch weather and stock market data from external APIs via MCP
- **Statistical Analysis**: Calculate Pearson correlation coefficients with significance testing
- **Interactive Visualizations**: Dual-axis charts showing weather and stock trends
- **Anomaly Detection**: Identify outliers using Z-score methodology
- **Natural Language Insights**: Human-readable explanations of correlation findings
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🛠 Technology Stack

### Backend
- **Flask 2.3** - Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL 15** - Relational database
- **Redis** - Caching layer
- **Pandas & SciPy** - Statistical analysis
- **MCP Protocol** - External API integration

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool
- **Tailwind CSS** - Styling framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client



## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+** and npm
- **PostgreSQL 15+**
- **Redis 7+** (optional, for caching)
- **API Keys** (optional, can use mock data):
  - OpenWeatherMap API key
  - Alpha Vantage API key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Kiro
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys and database connection:

```env
OPENWEATHERMAP_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dataweaver
REDIS_HOST=localhost
```

### 3. Set Up Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # On Windows
# source venv/bin/activate     # On macOS/Linux
pip install -r requirements.txt

# Initialize database
flask db upgrade  # Or create tables manually with schema.sql
```

### 4. Set Up Frontend

```bash
cd frontend
npm install
```

### 5. Start the Application

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
flask run
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 6. Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

## 📖 API Documentation

### Health Check

```bash
GET /api/health
```

Returns service status and version information.

### Refresh Data

```bash
POST /api/data/refresh
Content-Type: application/json

{
  "city": "New York",
  "symbol": "AAPL",
  "dateRange": "30d"
}
```

Fetches weather and stock data from external sources.

### Analyze Correlation

```bash
POST /api/correlations/analyze
Content-Type: application/json

{
  "city": "New York",
  "symbol": "AAPL",
  "dateRange": "30d",
  "weatherVariable": "temperature",
  "stockVariable": "close_price"
}
```

Performs statistical correlation analysis.

### Get Correlation Results

```bash
GET /api/correlations/{id}
GET /api/correlations/recent?limit=10
GET /api/correlations/search?city=New York&symbol=AAPL
GET /api/correlations/insights/{id}
```

Retrieve correlation analysis results and insights.

## 🗄 Database Schema

### weather_data
- `id`, `timestamp`, `city`, `temperature`, `humidity`, `precipitation`, `wind_speed`, `condition`

### stock_data
- `id`, `timestamp`, `symbol`, `open_price`, `close_price`, `high_price`, `low_price`, `volume`

### correlation_results
- `id`, `calculated_at`, `city`, `symbol`, `correlation_value`, `p_value`, `sample_size`, `weather_variable`, `stock_variable`, `analysis_notes`, `anomalies_detected`

## 🏗 Project Structure

```
Kiro/
├── backend/                 # Flask API
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   │   ├── mcp_client.py  # MCP integration
│   │   ├── data_service.py
│   │   └── correlation_service.py
│   ├── app.py             # Application entry
│   └── config.py          # Configuration
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   └── App.tsx
│   └── package.json
├── database/              # SQL schemas
├── .kiro/                 # MCP configuration
│   └── settings/
│       └── mcp.json
├── docker-compose.yml
└── README.md
```

## 🧪 Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🔧 Configuration

### MCP Servers

Edit `.kiro/settings/mcp.json` to configure MCP servers:

```json
{
  "mcpServers": {
    "weather": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-weather"],
      "env": {
        "OPENWEATHERMAP_API_KEY": "${OPENWEATHERMAP_API_KEY}"
      }
    },
    "stock": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-stock"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "${ALPHA_VANTAGE_API_KEY}"
      }
    }
  }
}
```

## 📊 How It Works

1. **Data Collection**: User selects a city, stock symbol, and date range
2. **External APIs**: System fetches data via MCP from OpenWeatherMap and Alpha Vantage
3. **Storage**: Data is validated, cleaned, and stored in PostgreSQL
4. **Analysis**: Correlation service aligns time series and calculates Pearson correlation
5. **Visualization**: Frontend displays results with interactive charts and insights

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
# On Windows: Check Services
# On macOS/Linux: sudo service postgresql status

# Test connection
psql -U postgres -d dataweaver
```

### API Errors

```bash
# Check backend logs in terminal
# Verify API keys in .env file
type .env | findstr API_KEY    # Windows
# cat .env | grep API_KEY      # macOS/Linux
```

### Frontend Build Issues

```bash
# Clear npm cache
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Flask, React, and the Model Context Protocol**
