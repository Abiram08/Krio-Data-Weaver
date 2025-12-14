"""Stock market data model for storing financial information."""

from datetime import datetime
from backend.models import db


class StockData(db.Model):
    """Model for stock market data from external APIs."""
    
    __tablename__ = 'stock_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    symbol = db.Column(db.String(10), nullable=False, index=True)
    open_price = db.Column(db.Numeric(12, 4), nullable=False)
    close_price = db.Column(db.Numeric(12, 4), nullable=False)
    high_price = db.Column(db.Numeric(12, 4), nullable=False)
    low_price = db.Column(db.Numeric(12, 4), nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite index and constraints
    __table_args__ = (
        db.Index('idx_stock_symbol_timestamp', 'symbol', 'timestamp'),
        db.CheckConstraint('open_price > 0', name='valid_open_price'),
        db.CheckConstraint('close_price > 0', name='valid_close_price'),
        db.CheckConstraint('high_price > 0', name='valid_high_price'),
        db.CheckConstraint('low_price > 0', name='valid_low_price'),
        db.CheckConstraint('volume >= 0', name='valid_volume'),
        db.CheckConstraint(
            'low_price <= open_price AND low_price <= close_price AND '
            'open_price <= high_price AND close_price <= high_price',
            name='valid_price_range'
        ),
    )
    
    def __repr__(self):
        return f'<StockData {self.symbol} at {self.timestamp}: ${self.close_price}>'
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'symbol': self.symbol,
            'open_price': float(self.open_price) if self.open_price else None,
            'close_price': float(self.close_price) if self.close_price else None,
            'high_price': float(self.high_price) if self.high_price else None,
            'low_price': float(self.low_price) if self.low_price else None,
            'volume': self.volume,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @property
    def volatility(self):
        """Calculate daily volatility (high - low)."""
        if self.high_price and self.low_price:
            return float(self.high_price - self.low_price)
        return 0.0
    
    @property
    def daily_change(self):
        """Calculate daily price change (close - open)."""
        if self.close_price and self.open_price:
            return float(self.close_price - self.open_price)
        return 0.0
    
    @property
    def daily_change_percent(self):
        """Calculate daily percentage change."""
        if self.open_price and self.close_price and self.open_price > 0:
            return ((float(self.close_price) - float(self.open_price)) / float(self.open_price)) * 100
        return 0.0
    
    @classmethod
    def get_by_symbol_and_range(cls, symbol, start_date, end_date):
        """Get stock data for a specific symbol and date range."""
        return cls.query.filter(
            cls.symbol == symbol.upper(),
            cls.timestamp >= start_date,
            cls.timestamp <= end_date
        ).order_by(cls.timestamp.asc()).all()
    
    @classmethod
    def get_latest(cls, symbol, limit=10):
        """Get latest stock data for a symbol."""
        return cls.query.filter(
            cls.symbol == symbol.upper()
        ).order_by(cls.timestamp.desc()).limit(limit).all()
