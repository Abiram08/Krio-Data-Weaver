"""
Correlation Service for statistical analysis of weather and stock data.
Implements Pearson correlation, significance testing, and anomaly detection.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from scipy import stats as scipy_stats

from backend.models import db
from backend.models.weather import WeatherData
from backend.models.stock import StockData
from backend.models.correlation import CorrelationResult

logger = logging.getLogger(__name__)


class CorrelationService:
    """Service for statistical correlation analysis."""
    
    def __init__(self):
        """Initialize correlation service."""
        self.min_sample_size = 10  # Minimum data points for correlation
        self.significance_threshold = 0.05  # P-value threshold
        self.anomaly_threshold = 3.0  # Z-score threshold for anomalies
    
    def align_time_series(
        self,
        weather_data: List[WeatherData],
        stock_data: List[StockData]
    ) -> pd.DataFrame:
        """
        Align weather and stock data by timestamp.
        
        Args:
            weather_data: List of WeatherData instances
            stock_data: List of StockData instances
            
        Returns:
            DataFrame with aligned data
        """
        # Convert to DataFrames
        weather_df = pd.DataFrame([{
            'timestamp': w.timestamp,
            'temperature': float(w.temperature) if w.temperature else None,
            'humidity': w.humidity,
            'precipitation': float(w.precipitation) if w.precipitation else 0.0,
            'wind_speed': float(w.wind_speed) if w.wind_speed else None
        } for w in weather_data])
        
        stock_df = pd.DataFrame([{
            'timestamp': s.timestamp,
            'close_price': float(s.close_price) if s.close_price else None,
            'volume': s.volume,
            'volatility': s.volatility,
            'daily_change': s.daily_change
        } for s in stock_data])
        
        if weather_df.empty or stock_df.empty:
            logger.warning("Empty dataset provided for alignment")
            return pd.DataFrame()
        
        # Set timestamp as index
        weather_df.set_index('timestamp', inplace=True)
        stock_df.set_index('timestamp', inplace=True)
        
        # Sort by timestamp
        weather_df.sort_index(inplace=True)
        stock_df.sort_index(inplace=True)
        
        # Merge using nearest timestamp (asof merge)
        aligned_df = pd.merge_asof(
            weather_df.reset_index(),
            stock_df.reset_index(),
            on='timestamp',
            direction='nearest',
            tolerance=pd.Timedelta(hours=12)  # Maximum time difference for matching
        )
        
        # Remove rows with missing critical data
        aligned_df.dropna(subset=['temperature', 'close_price'], inplace=True)
        
        logger.info(f"Aligned {len(aligned_df)} data points")
        return aligned_df
    
    def calculate_correlation(
        self,
        x: pd.Series,
        y: pd.Series
    ) -> Tuple[float, float]:
        """
        Calculate Pearson correlation coefficient and p-value.
        
        Args:
            x: First series
            y: Second series
            
        Returns:
            Tuple of (correlation_coefficient, p_value)
        """
        if len(x) < self.min_sample_size or len(y) < self.min_sample_size:
            logger.warning(f"Insufficient data for correlation: {len(x)} points")
            return 0.0, 1.0
        
        # Remove NaN values
        mask = ~(x.isna() | y.isna())
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) < self.min_sample_size:
            logger.warning("Insufficient clean data after removing NaN values")
            return 0.0, 1.0
        
        # Calculate Pearson correlation
        try:
            corr_coef, p_value = scipy_stats.pearsonr(x_clean, y_clean)
            logger.info(f"Correlation: r={corr_coef:.4f}, p={p_value:.6f}, n={len(x_clean)}")
            return float(corr_coef), float(p_value)
        except Exception as e:
            logger.error(f"Error calculating correlation: {e}")
            return 0.0, 1.0
    
    def detect_anomalies(
        self,
        data: pd.DataFrame,
        columns: List[str]
    ) -> Dict[str, List[int]]:
        """
        Detect anomalies using Z-score method.
        
        Args:
            data: DataFrame with time series data
            columns: Column names to check for anomalies
            
        Returns:
            Dictionary mapping column names to lists of anomaly indices
        """
        anomalies = {}
        
        for col in columns:
            if col not in data.columns:
                continue
            
            series = data[col].dropna()
            if len(series) < 10:  # Need enough data for meaningful statistics
                continue
            
            # Calculate Z-scores
            z_scores = np.abs(scipy_stats.zscore(series))
            
            # Find anomalies (Z-score > threshold)
            anomaly_mask = z_scores > self.anomaly_threshold
            anomaly_indices = series[anomaly_mask].index.tolist()
            
            if anomaly_indices:
                anomalies[col] = anomaly_indices
                logger.info(f"Found {len(anomaly_indices)} anomalies in {col}")
        
        return anomalies
    
    def generate_insights(
        self,
        correlation_value: float,
        p_value: float,
        weather_variable: str,
        stock_variable: str,
        sample_size: int,
        anomalies_count: int
    ) -> str:
        """
        Generate human-readable insights from correlation analysis.
        
        Args:
            correlation_value: Correlation coefficient
            p_value: Statistical significance
            weather_variable: Name of weather variable
            stock_variable: Name of stock variable
            sample_size: Number of data points analyzed
            anomalies_count: Number of anomalies detected
            
        Returns:
            Natural language insight text
        """
        insights = []
        
        # Correlation strength
        abs_corr = abs(correlation_value)
        if abs_corr >= 0.7:
            strength = "strong"
        elif abs_corr >= 0.4:
            strength = "moderate"
        elif abs_corr >= 0.2:
            strength = "weak"
        else:
            strength = "very weak"
        
        # Correlation direction
        if correlation_value > 0.05:
            direction = "positive"
            relationship = "increases with"
        elif correlation_value < -0.05:
            direction = "negative"
            relationship = "decreases with"
        else:
            direction = "negligible"
            relationship = "shows no clear relationship with"
        
        # Statistical significance
        if p_value < 0.001:
            significance = "very highly significant"
        elif p_value < 0.01:
            significance = "highly significant"
        elif p_value < 0.05:
            significance = "significant"
        elif p_value < 0.1:
            significance = "marginally significant"
        else:
            significance = "not statistically significant"
        
        # Build insights
        insights.append(
            f"Analysis of {sample_size} data points reveals a {strength} {direction} correlation "
            f"(r={correlation_value:.3f}) between {weather_variable} and {stock_variable}."
        )
        
        insights.append(
            f"The {stock_variable} {relationship} {weather_variable}. "
            f"This relationship is {significance} (p={p_value:.4f})."
        )
        
        if p_value < 0.05:
            insights.append(
                f"The correlation is statistically significant, suggesting a real relationship "
                f"rather than random chance."
            )
        else:
            insights.append(
                f"The correlation is not statistically significant, which means the observed "
                f"relationship could be due to random chance."
            )
        
        if anomalies_count > 0:
            insights.append(
                f"Detected {anomalies_count} anomalous data points that deviate significantly "
                f"from the normal pattern, which may represent unusual market or weather events."
            )
        
        return " ".join(insights)
    
    def analyze_correlation(
        self,
        city: str,
        symbol: str,
        weather_data: List[WeatherData],
        stock_data: List[StockData],
        weather_variable: str = 'temperature',
        stock_variable: str = 'close_price'
    ) -> Optional[CorrelationResult]:
        """
        Perform complete correlation analysis.
        
        Args:
            city: City name
            symbol: Stock symbol
            weather_data: List of weather data points
            stock_data: List of stock data points
            weather_variable: Weather variable to analyze
            stock_variable: Stock variable to analyze
            
        Returns:
            CorrelationResult instance or None if analysis fails
        """
        logger.info(f"Analyzing correlation between {weather_variable} and {stock_variable}")
        
        # Align time series
        aligned_df = self.align_time_series(weather_data, stock_data)
        
        if aligned_df.empty:
            logger.error("No aligned data available for correlation analysis")
            return None
        
        # Calculate correlation
        corr_value, p_value = self.calculate_correlation(
            aligned_df[weather_variable],
            aligned_df[stock_variable]
        )
        
        # Detect anomalies
        anomalies = self.detect_anomalies(
            aligned_df,
            [weather_variable, stock_variable]
        )
        anomalies_count = sum(len(indices) for indices in anomalies.values())
        
        # Calculate period
        start_date = aligned_df['timestamp'].min()
        end_date = aligned_df['timestamp'].max()
        period_days = (end_date - start_date).days
        
        # Generate insights
        insights = self.generate_insights(
            corr_value,
            p_value,
            weather_variable,
            stock_variable,
            len(aligned_df),
            anomalies_count
        )
        
        # Determine significance level
        if p_value < 0.001:
            significance_level = "p < 0.001"
        elif p_value < 0.01:
            significance_level = "p < 0.01"
        elif p_value < 0.05:
            significance_level = "p < 0.05"
        else:
            significance_level = "not significant"
        
        # Create correlation result
        result = CorrelationResult(
            city=city,
            symbol=symbol.upper(),
            start_date=start_date,
            end_date=end_date,
            period_days=period_days,
            correlation_value=corr_value,
            p_value=p_value,
            sample_size=len(aligned_df),
            weather_variable=weather_variable,
            stock_variable=stock_variable,
            significance_level=significance_level,
            analysis_notes=insights,
            anomalies_detected=anomalies_count
        )
        
        # Save to database
        try:
            db.session.add(result)
            db.session.commit()
            logger.info(f"Saved correlation result with ID: {result.id}")
            return result
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to save correlation result: {e}")
            return None
