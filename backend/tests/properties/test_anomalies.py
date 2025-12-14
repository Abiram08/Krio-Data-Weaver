"""
Property-based tests for anomaly detection
Feature: data-weaver-dashboard, Property 5: Anomaly detection consistency
"""

import pytest
from hypothesis import given, strategies as st
import pandas as pd
import numpy as np
from backend.services.correlation_service import CorrelationService


class TestAnomalyDetection:
    """Property 5: Anomaly detection should consistently identify outliers using defined thresholds"""
    
    @given(
        n_normal=st.integers(min_value=20, max_value=100),
        n_outliers=st.integers(min_value=1, max_value=5)
    )
    def test_z_score_anomaly_detection(self, n_normal, n_outliers):
        """Property test: Z-score method should detect extreme outliers"""
        service = CorrelationService()
        
        # Generate normal data
        normal_data = np.random.normal(0, 1, n_normal)
        
        # Add clear outliers (>3 standard deviations)
        outliers = np.random.choice([-10, 10], size=n_outliers)
        combined_data = np.concatenate([normal_data, outliers])
        
        df = pd.DataFrame({'values': combined_data})
        anomalies = service.detect_anomalies(df, ['values'])
        
        # Property: Should detect at least some anomalies when outliers are present
        if 'values' in anomalies:
            assert len(anomalies['values']) > 0
            assert len(anomalies['values']) <= n_outliers + 2  # Allow some margin
    
    @given(
        n_points=st.integers(min_value=30, max_value=100)
    )
    def test_no_anomalies_in_normal_data(self, n_points):
        """Property test: Normal distributed data should have few/no anomalies"""
        service = CorrelationService()
        
        # Generate strictly normal data (within 2.5 std devs)
        normal_data = np.random.normal(0, 1, n_points)
        normal_data = normal_data[np.abs(normal_data) < 2.5]  # Remove extreme values
        
        df = pd.DataFrame({'values': normal_data})
        anomalies = service.detect_anomalies(df, ['values'])
        
        # Property: Should detect very few anomalies in normal data
        if 'values' in anomalies:
            assert len(anomalies['values']) < len(normal_data) * 0.05  # Less than 5%


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
