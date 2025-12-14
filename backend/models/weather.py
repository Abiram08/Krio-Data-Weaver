"""Weather data model for storing meteorological information."""

from datetime import datetime
from backend.models import db


class WeatherData(db.Model):
    """Model for weather data from external APIs."""
    
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    temperature = db.Column(db.Numeric(5, 2), nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    precipitation = db.Column(db.Numeric(6, 2), default=0)
    wind_speed = db.Column(db.Numeric(5, 2), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite index for efficient queries
    __table_args__ = (
        db.Index('idx_weather_city_timestamp', 'city', 'timestamp'),
        db.CheckConstraint('humidity >= 0 AND humidity <= 100', name='valid_humidity'),
        db.CheckConstraint('precipitation >= 0', name='valid_precipitation'),
        db.CheckConstraint('wind_speed >= 0', name='valid_wind_speed'),
    )
    
    def __repr__(self):
        return f'<WeatherData {self.city} at {self.timestamp}: {self.temperature}°C>'
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'city': self.city,
            'temperature': float(self.temperature) if self.temperature else None,
            'humidity': self.humidity,
            'precipitation': float(self.precipitation) if self.precipitation else 0.0,
            'wind_speed': float(self.wind_speed) if self.wind_speed else None,
            'condition': self.condition,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_city_and_range(cls, city, start_date, end_date):
        """Get weather data for a specific city and date range."""
        return cls.query.filter(
            cls.city == city,
            cls.timestamp >= start_date,
            cls.timestamp <= end_date
        ).order_by(cls.timestamp.asc()).all()
    
    @classmethod
    def get_latest(cls, city, limit=10):
        """Get latest weather data for a city."""
        return cls.query.filter(
            cls.city == city
        ).order_by(cls.timestamp.desc()).limit(limit).all()
