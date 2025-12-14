"""
Direct API Client - bypasses MCP for direct API calls
Uses OpenWeatherMap and Alpha Vantage APIs directly
"""

import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)


class DirectAPIClient:
    """Direct API client for weather and stock data (bypasses MCP)."""
    
    def __init__(self):
        """Initialize with API keys from environment."""
        self.weather_api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.stock_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not self.weather_api_key:
            logger.warning("OPENWEATHERMAP_API_KEY not set")
        if not self.stock_api_key:
            logger.warning("ALPHA_VANTAGE_API_KEY not set")
    
    def get_weather_data(self, city: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Fetch weather data from OpenWeatherMap API.
        
        For demo purposes, using current weather data.
        In production, you'd use historical data API.
        """
        if not self.weather_api_key:
            logger.error("Weather API key not configured")
            return []
        
        try:
            # Using current weather API (free tier)
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Generate historical-like data from current weather
            # For demo: create data points for the date range
            weather_records = []
            days = (end_date - start_date).days
            
            for i in range(min(days, 30)):  # Limit to 30 days
                date = start_date + timedelta(days=i)
                # Vary temperature slightly for demo
                temp_variation = (i % 7 - 3) * 2  # Varies ±6 degrees
                
                weather_records.append({
                    'timestamp': date.isoformat(),
                    'temperature': data['main']['temp'] + temp_variation,
                    'humidity': data['main']['humidity'],
                    'precipitation': data.get('rain', {}).get('1h', 0),
                    'wind_speed': data['wind']['speed'] * 3.6,  # m/s to km/h
                    'condition': data['weather'][0]['main']
                })
            
            logger.info(f"Fetched {len(weather_records)} weather records for {city}")
            return weather_records
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in weather data fetch: {e}")
            return []
    
    def get_stock_data(self, symbol: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Fetch stock data from Alpha Vantage API.
        
        Using TIME_SERIES_DAILY function.
        """
        if not self.stock_api_key:
            logger.error("Stock API key not configured")
            return []
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': self.stock_api_key,
                'outputsize': 'compact'  # Last 100 days
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Error Message' in data:
                logger.error(f"Alpha Vantage error: {data['Error Message']}")
                return []
            
            if 'Time Series (Daily)' not in data:
                logger.error(f"Unexpected API response: {list(data.keys())}")
                return []
            
            time_series = data['Time Series (Daily)']
            stock_records = []
            
            for date_str, values in time_series.items():
                date = datetime.strptime(date_str, '%Y-%m-%d')
                
                # Filter by date range
                if start_date <= date <= end_date:
                    stock_records.append({
                        'timestamp': date.isoformat(),
                        'open_price': float(values['1. open']),
                        'close_price': float(values['4. close']),
                        'high_price': float(values['2. high']),
                        'low_price': float(values['3. low']),
                        'volume': int(values['5. volume'])
                    })
            
            # Sort by date
            stock_records.sort(key=lambda x: x['timestamp'])
            
            logger.info(f"Fetched {len(stock_records)} stock records for {symbol}")
            return stock_records
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching stock data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in stock data fetch: {e}")
            return []
