"""Correlation results model for storing statistical analysis outcomes."""

from datetime import datetime
import uuid
from backend.models import db


class CorrelationResult(db.Model):
    """Model for storing correlation analysis results."""
    
    __tablename__ = 'correlation_results'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    calculated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, index=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    symbol = db.Column(db.String(10), nullable=False, index=True)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False)
    period_days = db.Column(db.Integer, nullable=False)
    correlation_value = db.Column(db.Numeric(8, 6), nullable=False)
    p_value = db.Column(db.Numeric(10, 8), nullable=False)
    sample_size = db.Column(db.Integer, nullable=False)
    weather_variable = db.Column(db.String(50), nullable=False)
    stock_variable = db.Column(db.String(50), nullable=False)
    significance_level = db.Column(db.String(20))
    analysis_notes = db.Column(db.Text)
    anomalies_detected = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite index and constraints
    __table_args__ = (
        db.Index('idx_correlation_city_symbol', 'city', 'symbol'),
        db.CheckConstraint('period_days > 0', name='valid_period'),
        db.CheckConstraint('correlation_value >= -1.0 AND correlation_value <= 1.0', name='valid_correlation'),
        db.CheckConstraint('p_value >= 0 AND p_value <= 1', name='valid_p_value'),
        db.CheckConstraint('sample_size > 0', name='valid_sample_size'),
        db.CheckConstraint('anomalies_detected >= 0', name='valid_anomalies'),
    )
    
    def __repr__(self):
        return f'<CorrelationResult {self.city}-{self.symbol}: r={self.correlation_value}, p={self.p_value}>'
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None,
            'city': self.city,
            'symbol': self.symbol,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'period_days': self.period_days,
            'correlation_value': float(self.correlation_value) if self.correlation_value is not None else None,
            'p_value': float(self.p_value) if self.p_value is not None else None,
            'sample_size': self.sample_size,
            'weather_variable': self.weather_variable,
            'stock_variable': self.stock_variable,
            'significance_level': self.significance_level,
            'significance': self.get_significance_category(),
            'analysis_notes': self.analysis_notes,
            'anomalies_detected': self.anomalies_detected,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_significance_category(self):
        """Determine significance category based on p-value."""
        if self.p_value is None:
            return 'unknown'
        
        p_val = float(self.p_value)
        if p_val < 0.001:
            return 'very_high'
        elif p_val < 0.01:
            return 'high'
        elif p_val < 0.05:
            return 'medium'
        elif p_val < 0.1:
            return 'low'
        else:
            return 'none'
    
    def get_correlation_strength(self):
        """Determine correlation strength category."""
        if self.correlation_value is None:
            return 'unknown'
        
        abs_corr = abs(float(self.correlation_value))
        if abs_corr >= 0.7:
            return 'strong'
        elif abs_corr >= 0.4:
            return 'moderate'
        elif abs_corr >= 0.2:
            return 'weak'
        else:
            return 'very_weak'
    
    def get_correlation_direction(self):
        """Determine correlation direction."""
        if self.correlation_value is None:
            return 'none'
        
        corr_val = float(self.correlation_value)
        if corr_val > 0.05:
            return 'positive'
        elif corr_val < -0.05:
            return 'negative'
        else:
            return 'none'
    
    @classmethod
    def get_recent(cls, limit=10):
        """Get recent correlation results."""
        return cls.query.order_by(cls.calculated_at.desc()).limit(limit).all()
    
    @classmethod
    def get_by_city_and_symbol(cls, city, symbol):
        """Get correlation results for specific city and symbol."""
        return cls.query.filter(
            cls.city == city,
            cls.symbol == symbol.upper()
        ).order_by(cls.calculated_at.desc()).all()
