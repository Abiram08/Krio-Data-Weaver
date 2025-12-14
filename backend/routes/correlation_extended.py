"""
Extended correlation routes for advanced features:
- Correlation matrix (all variables)
- Historical trend analysis
"""

import logging
from flask import request, jsonify
from datetime import datetime, timedelta

from backend.routes import correlation_bp
from backend.services.data_service import DataService
from backend.services.correlation_service import CorrelationService
from scipy.stats import pearsonr
import pandas as pd

logger = logging.getLogger(__name__)

# Reuse existing service instances
from backend.routes.correlations import data_service, correlation_service


@correlation_bp.route('/matrix', methods=['POST'])
def get_correlation_matrix():
    """
    Calculate correlation matrix for all variable combinations.
    
    Request body:
        {
            "city": "New York",
            "symbol": "AAPL",
            "dateRange": "30d"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        city = data.get('city')
        symbol = data.get('symbol')
        date_range = data.get('dateRange', '30d')
        
        if not city or not symbol:
            return jsonify({'error': 'Missing required fields: city, symbol'}), 400
        
        # Parse date range
        end_date = datetime.now()
        if isinstance(date_range, str):
            days = int(date_range.rstrip('d'))
            start_date = end_date - timedelta(days=days)
        else:
            start_date = end_date - timedelta(days=30)
        
        logger.info(f"Calculating correlation matrix for {city}/{symbol}")
        
        # Fetch data
        combined_data = data_service.get_combined_data(
            city=city,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        weather_data = combined_data['weather']
        stock_data = combined_data['stock']
        
        if not weather_data or not stock_data:
            return jsonify({'error': 'Insufficient data for analysis'}), 400
        
        # Convert to DataFrames
        weather_df = pd.DataFrame([w.to_dict() for w in weather_data])
        stock_df = pd.DataFrame([s.to_dict() for s in stock_data])
        
        weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'])
        stock_df['timestamp'] = pd.to_datetime(stock_df['timestamp'])
        
        # Align time series
        aligned = pd.merge_asof(
            weather_df.sort_values('timestamp'),
            stock_df.sort_values('timestamp'),
            on='timestamp',
            direction='nearest',
            tolerance=pd.Timedelta('6H')
        ).dropna()
        
        if len(aligned) < 3:
            return jsonify({'error': 'Not enough aligned data points'}), 400
        
        # Define variables
        weather_vars = ['temperature', 'humidity', 'precipitation', 'wind_speed']
        stock_vars = ['open_price', 'close_price', 'high_price', 'low_price', 'volume']
        
        # Calculate correlation matrix
        matrix = []
        for weather_var in weather_vars:
            row = {'variable': weather_var, 'correlations': {}}
            for stock_var in stock_vars:
                if weather_var in aligned.columns and stock_var in aligned.columns:
                    try:
                        r, p = pearsonr(
                            aligned[weather_var].dropna(),
                            aligned[stock_var].dropna()
                        )
                        row['correlations'][stock_var] = {
                            'r': float(r),
                            'p': float(p),
                            'significant': p < 0.05
                        }
                    except Exception as e:
                        logger.warning(f"Failed to calculate {weather_var} vs {stock_var}: {e}")
                        row['correlations'][stock_var] = {
                            'r': 0.0,
                            'p': 1.0,
                            'significant': False
                        }
            matrix.append(row)
        
        return jsonify({
            'success': True,
            'matrix': matrix,
            'weather_variables': weather_vars,
            'stock_variables': stock_vars,
            'sample_size': len(aligned),
            'metadata': {
                'city': city,
                'symbol': symbol,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error calculating correlation matrix: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@correlation_bp.route('/trends', methods=['POST'])
def get_correlation_trends():
    """
    Calculate correlation trends over time (rolling window analysis).
    
    Request body:
        {
            "city": "New York",
            "symbol": "AAPL",
            "weather_variable": "temperature",
            "stock_variable": "close_price",
            "window_days": 30,
            "total_days": 180
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        city = data.get('city')
        symbol = data.get('symbol')
        weather_var = data.get('weather_variable', 'temperature')
        stock_var = data.get('stock_variable', 'close_price')
        window_days = data.get('window_days', 30)
        total_days = data.get('total_days', 180)
        
        if not city or not symbol:
            return jsonify({'error': 'Missing required fields: city, symbol'}), 400
        
        logger.info(f"Calculating correlation trends for {city}/{symbol}")
        
        # Calculate trends for different time windows
        trends = []
        today = datetime.now()
        
        # Create 6 windows (e.g., for 180 days with 30-day windows)
        for i in range(0, total_days, window_days):
            end = today - timedelta(days=i)
            start = end - timedelta(days=window_days)
            
            try:
                # Fetch data for this window
                combined_data = data_service.get_combined_data(
                    city=city,
                    symbol=symbol,
                    start_date=start,
                    end_date=end
                )
                
                weather_data = combined_data['weather']
                stock_data = combined_data['stock']
                
                if not weather_data or not stock_data:
                    continue
                
                # Convert and align
                weather_df = pd.DataFrame([w.to_dict() for w in weather_data])
                stock_df = pd.DataFrame([s.to_dict() for s in stock_data])
                
                weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'])
                stock_df['timestamp'] = pd.to_datetime(stock_df['timestamp'])
                
                aligned = pd.merge_asof(
                    weather_df.sort_values('timestamp'),
                    stock_df.sort_values('timestamp'),
                    on='timestamp',
                    direction='nearest',
                    tolerance=pd.Timedelta('6H')
                ).dropna()
                
                if len(aligned) >= 3 and weather_var in aligned.columns and stock_var in aligned.columns:
                    r, p = pearsonr(
                        aligned[weather_var].dropna(),
                        aligned[stock_var].dropna()
                    )
                    
                    trends.append({
                        'period_start': start.isoformat(),
                        'period_end': end.isoformat(),
                        'period_label': f"{start.strftime('%b %d')} - {end.strftime('%b %d')}",
                        'correlation': float(r),
                        'p_value': float(p),
                        'sample_size': len(aligned),
                        'significant': p < 0.05
                    })
            except Exception as e:
                logger.warning(f"Failed to calculate trend for window {start} - {end}: {e}")
                continue
        
        # Reverse to show oldest first
        trends.reverse()
        
        return jsonify({
            'success': True,
            'trends': trends,
            'metadata': {
                'city': city,
                'symbol': symbol,
                'weather_variable': weather_var,
                'stock_variable': stock_var,
                'window_days': window_days,
                'total_windows': len(trends)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error calculating correlation trends: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
