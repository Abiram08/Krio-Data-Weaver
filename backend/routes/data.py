"""
Data routes for fetching and refreshing external data sources.
"""

import logging
from flask import request, jsonify
from datetime import datetime, timedelta

from backend.routes import data_bp
from backend.services.data_service import DataService

logger = logging.getLogger(__name__)

# Initialize services (DirectAPIClient will be created automatically)
data_service = DataService()


@data_bp.route('/refresh', methods=['POST'])
def refresh_data():
    """
    Refresh data from external sources.
    
    Request body:
        {
            "city": "New York",
            "symbol": "AAPL",
            "dateRange": "30d" or {"start": "2024-01-01", "end": "2024-01-31"}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        city = data.get('city')
        symbol = data.get('symbol')
        date_range = data.get('dateRange')
        
        # Validate inputs
        if not city or not symbol:
            return jsonify({'error': 'Missing required fields: city, symbol'}), 400
        
        # Parse date range
        end_date = datetime.now()
        
        if isinstance(date_range, str):
            # Parse preset ranges (7d, 30d, 90d)
            days = int(date_range.rstrip('d'))
            start_date = end_date - timedelta(days=days)
        elif isinstance(date_range, dict):
            # Parse custom range
            start_date = datetime.fromisoformat(date_range.get('start'))
            end_date = datetime.fromisoformat(date_range.get('end'))
        else:
            # Default to 30 days
            start_date = end_date - timedelta(days=30)
        
        logger.info(f"Refreshing data for {city}/{symbol} from {start_date} to {end_date}")
        
        # Fetch data
        combined_data = data_service.get_combined_data(
            city=city,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        weather_count = len(combined_data['weather'])
        stock_count = len(combined_data['stock'])
        
        logger.info(f"Fetched {weather_count} weather records and {stock_count} stock records")
        
        return jsonify({
            'success': True,
            'data': {
                'weather': [w.to_dict() for w in combined_data['weather']],
                'stock': [s.to_dict() for s in combined_data['stock']]
            },
            'metadata': {
                'city': city,
                'symbol': symbol,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'weather_count': weather_count,
                'stock_count': stock_count
            }
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error refreshing data: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@data_bp.route('/timeseries', methods=['GET'])
def get_timeseries():
    """
    Get time series data for visualization.
    
    Query parameters:
        - city: City name
        - symbol: Stock symbol
        - start_date: Start date (ISO format)
        - end_date: End date (ISO format)
    """
    try:
        city = request.args.get('city')
        symbol = request.args.get('symbol')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Validate inputs
        if not all([city, symbol, start_date_str, end_date_str]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
        
        # Get data from database (cached)
        combined_data = data_service.get_combined_data(
            city=city,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'success': True,
            'data': {
                'weather': [w.to_dict() for w in combined_data['weather']],
                'stock': [s.to_dict() for s in combined_data['stock']]
            }
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error getting time series: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
