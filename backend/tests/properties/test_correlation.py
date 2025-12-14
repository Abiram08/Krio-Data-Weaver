"""
Property-based tests for correlation engine
Feature: data-weaver-dashboard, Property 4: Data alignment and correlation accuracy
"""

import pytest
from hypothesis import given, strategies as st
import pandas as pd
import numpy as np
from backend.services.correlation_service import CorrelationService
from backend.models.weather import WeatherData
from backend.models.stock import StockData
from datetime import datetime, timedelta


class TestCorrelationAccuracy:
    """Property 4: Timestamp alignment and correlation calculations should be mathematically correct"""
    
    @given(
        data_points=st.integers(min_value=10, max_value=100),
        correlation_strength=st.floats(min_value=-1.0, max_value=1.0)
    )
    def test_correlation_coefficient_bounds(self, data_points, correlation_strength):
        """Property test: Correlation coefficient must always be between -1 and 1"""
        service = CorrelationService()
        
        # Generate synthetic correlated data
        x = np.random.randn(data_points)
        noise = np.random.randn(data_points) * np.sqrt(1 - correlation_strength**2)
        y = correlation_strength * x + noise
        
        x_series = pd.Series(x)
        y_series = pd.Series(y)
        
        corr_value, p_value = service.calculate_correlation(x_series, y_series)
        
        # Property: Correlation must be in valid range
        assert -1.0 <= corr_value <= 1.0
        # Property: P-value must be between 0 and 1
        assert 0.0 <= p_value <= 1.0
    
    @given(
        n_points=st.integers(min_value=15, max_value=50)
    )
    def test_perfect_correlation(self, n_points):
        """Property test: Perfectly correlated data should have r ≈ 1.0 or -1.0"""
        service = CorrelationService()
        
        x = np.arange(n_points, dtype=float)
        y_perfect_positive = x * 2 + 5  # Perfect positive correlation
        y_perfect_negative = -x * 3 + 10  # Perfect negative correlation
        
        corr_pos, _ = service.calculate_correlation(pd.Series(x), pd.Series(y_perfect_positive))
        corr_neg, _ = service.calculate_correlation(pd.Series(x), pd.Series(y_perfect_negative))
        
        # Property: Perfect positive correlation
        assert abs(corr_pos - 1.0) < 0.01
        # Property: Perfect negative correlation  
        assert abs(corr_neg + 1.0) < 0.01


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
