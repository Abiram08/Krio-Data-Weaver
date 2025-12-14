"""
Data Service for fetching, validating, and storing data from external sources.
Integrates with MCP client and provides caching layer.
"""

import logging
import redis
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from backend.models import db
from backend.models.weather import WeatherData
from backend.models.stock import StockData
from backend.services.direct_api_client import DirectAPIClient  # Using direct API instead of MCP
from backend.config import get_config

logger = logging.getLogger(__name__)


class DataService:
    """Service for data fetching, validation, and persistence."""
    
    def __init__(self, api_client: Optional[DirectAPIClient] = None, redis_client: Optional[redis.Redis] = None):
        """
        Initialize data service.
        
        Args:
            api_client: Direct API client instance
            redis_client: Redis client for caching
        """
        self.api_client = api_client or DirectAPIClient()
        config = get_config()()
        
        # Initialize Redis cache
        if redis_client:
            self.redis = redis_client
        else:
            try:
                self.redis = redis.Redis(
                    host=config.REDIS_HOST,
                    port=config.REDIS_PORT,
                    db=config.REDIS_DB,
                    password=config.REDIS_PASSWORD,
                    decode_responses=True
                )
                self.redis.ping()  # Test connection
                logger.info("Redis cache connected successfully")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Caching disabled.")
                self.redis = None
        
        self.cache_ttl = config.CACHE_TTL_SECONDS
    
    def _get_cache_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key from parameters."""
        key_parts = [prefix] + [f"{k}:{v}" for k, v in sorted(kwargs.items())]
        return ":".join(key_parts)
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Retrieve data from cache."""
        if not self.redis:
            return None
        
        try:
            cached = self.redis.get(key)
            if cached:
                logger.debug(f"Cache hit: {key}")
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Cache retrieval error: {e}")
        
        return None
    
    def _set_cache(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store data in cache."""
        if not self.redis:
            return
        
        try:
            ttl = ttl or self.cache_ttl
            self.redis.setex(key, ttl, json.dumps(value))
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
    
    def _validate_weather_data(self, data: Dict[str, Any]) -> bool:
        """Validate weather data structure and values."""
        required_fields = ['timestamp', 'temperature', 'humidity', 'wind_speed', 'condition']
        
        # Check required fields
        if not all(field in data for field in required_fields):
            logger.warning(f"Missing required fields in weather data: {data}")
            return False
        
        # Validate ranges
        if not (-100 <= data['temperature'] <= 60):  # Celsius
            logger.warning(f"Invalid temperature: {data['temperature']}")
            return False
        
        if not (0 <= data['humidity'] <= 100):
            logger.warning(f"Invalid humidity: {data['humidity']}")
            return False
        
        if not (0 <= data['wind_speed'] <= 200):  # km/h
            logger.warning(f"Invalid wind speed: {data['wind_speed']}")
            return False
        
        return True
    
    def _validate_stock_data(self, data: Dict[str, Any]) -> bool:
        """Validate stock data structure and values."""
        required_fields = ['timestamp', 'open_price', 'close_price', 'high_price', 'low_price', 'volume']
        
        # Check required fields
        if not all(field in data for field in required_fields):
            logger.warning(f"Missing required fields in stock data: {data}")
            return False
        
        # Validate price relationships
        if not (data['low_price'] <= data['open_price'] <= data['high_price']):
            logger.warning(f"Invalid price relationship: L={data['low_price']}, O={data['open_price']}, H={data['high_price']}")
            return False
        
        if not (data['low_price'] <= data['close_price'] <= data['high_price']):
            logger.warning(f"Invalid price relationship: L={data['low_price']}, C={data['close_price']}, H={data['high_price']}")
            return False
        
        if data['volume'] < 0:
            logger.warning(f"Invalid volume: {data['volume']}")
            return False
        
        return True
    
    def fetch_and_store_weather(
        self,
        city: str,
        start_date: datetime,
        end_date: datetime,
        use_cache: bool = True
    ) -> List[WeatherData]:
        """
        Fetch weather data from MCP and store in database.
        
        Args:
            city: City name
            start_date: Start date for data range
            end_date: End date for data range
            use_cache: Whether to use cache
            
        Returns:
            List of WeatherData instances
        """
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(
                'weather',
                city=city,
                start=start_date.isoformat(),
                end=end_date.isoformat()
            )
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                return [WeatherData(**item) for item in cached_data]
        
        # Fetch from Direct API
        raw_data = self.api_client.get_weather_data(city, start_date, end_date)
        if not raw_data:
            logger.error(f"Failed to fetch weather data for {city}")
            return []
        
        # Validate and store
        weather_records = []
        for item in raw_data:
            if not self._validate_weather_data(item):
                continue
            
            # Check if record already exists
            existing = WeatherData.query.filter_by(
                city=city,
                timestamp=datetime.fromisoformat(item['timestamp'])
            ).first()
            
            if existing:
                weather_records.append(existing)
                continue
            
            # Create new record
            weather = WeatherData(
                timestamp=datetime.fromisoformat(item['timestamp']),
                city=city,
                temperature=item['temperature'],
                humidity=item['humidity'],
                precipitation=item.get('precipitation', 0),
                wind_speed=item['wind_speed'],
                condition=item['condition']
            )
            
            db.session.add(weather)
            weather_records.append(weather)
        
        # Commit to database
        try:
            db.session.commit()
            logger.info(f"Stored {len(weather_records)} weather records for {city}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to store weather data: {e}")
            return []
        
        # Cache results
        if use_cache and weather_records:
            cache_data = [w.to_dict() for w in weather_records]
            self._set_cache(cache_key, cache_data)
        
        return weather_records
    
    def fetch_and_store_stock(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        use_cache: bool = True
    ) -> List[StockData]:
        """
        Fetch stock data from MCP and store in database.
        
        Args:
            symbol: Stock symbol
            start_date: Start date for data range
            end_date: End date for data range
            use_cache: Whether to use cache
            
        Returns:
            List of StockData instances
        """
        symbol = symbol.upper()
        
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(
                'stock',
                symbol=symbol,
                start=start_date.isoformat(),
                end=end_date.isoformat()
            )
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                return [StockData(**item) for item in cached_data]
        
        # Fetch from Direct API
        raw_data = self.api_client.get_stock_data(symbol, start_date, end_date)
        if not raw_data:
            logger.error(f"Failed to fetch stock data for {symbol}")
            return []
        
        # Validate and store
        stock_records = []
        for item in raw_data:
            if not self._validate_stock_data(item):
                continue
            
            # Check if record already exists
            existing = StockData.query.filter_by(
                symbol=symbol,
                timestamp=datetime.fromisoformat(item['timestamp'])
            ).first()
            
            if existing:
                stock_records.append(existing)
                continue
            
            # Create new record
            stock = StockData(
                timestamp=datetime.fromisoformat(item['timestamp']),
                symbol=symbol,
                open_price=item['open_price'],
                close_price=item['close_price'],
                high_price=item['high_price'],
                low_price=item['low_price'],
                volume=item['volume']
            )
            
            db.session.add(stock)
            stock_records.append(stock)
        
        # Commit to database
        try:
            db.session.commit()
            logger.info(f"Stored {len(stock_records)} stock records for {symbol}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to store stock data: {e}")
            return []
        
        # Cache results
        if use_cache and stock_records:
            cache_data = [s.to_dict() for s in stock_records]
            self._set_cache(cache_key, cache_data)
        
        return stock_records
    
    def get_combined_data(
        self,
        city: str,
        symbol: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, List[Any]]:
        """
        Fetch both weather and stock data for correlation analysis.
        
        Returns:
            Dictionary with 'weather' and 'stock' lists
        """
        weather_data = self.fetch_and_store_weather(city, start_date, end_date)
        stock_data = self.fetch_and_store_stock(symbol, start_date, end_date)
        
        return {
            'weather': weather_data,
            'stock': stock_data
        }
