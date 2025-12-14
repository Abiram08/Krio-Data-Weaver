"""
Correlation routes for statistical analysis endpoints.
"""

import logging
from flask import request, jsonify
from datetime import datetime, timedelta

from backend.routes import correlation_bp
from backend.services.data_service import DataService
from backend.services.correlation_service import CorrelationService
from backend.services.ai_insights import AIInsightsService
from backend.models.correlation import CorrelationResult

logger = logging.getLogger(__name__)

# Initialize services (DirectAPIClient will be created automatically)
data_service = DataService()
correlation_service = CorrelationService()
ai_insights_service = AIInsightsService()


@correlation_bp.route('/analyze', methods=['POST'])
def analyze_correlation():
    """
    Perform correlation analysis between weather and stock data.
    
    Request body:
        {
            "city": "New York",
            "symbol": "AAPL",
            "dateRange": "30d",
            "weatherVariable": "temperature",
            "stockVariable": "close_price"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        city = data.get('city')
        symbol = data.get('symbol')
        date_range = data.get('dateRange', '30d')
        weather_var = data.get('weatherVariable', 'temperature')
        stock_var = data.get('stockVariable', 'close_price')
        
        # Validate inputs
        if not city or not symbol:
            return jsonify({'error': 'Missing required fields: city, symbol'}), 400
        
        # Parse date range
        end_date = datetime.now()
        
        if isinstance(date_range, str):
            days = int(date_range.rstrip('d'))
            start_date = end_date - timedelta(days=days)
        elif isinstance(date_range, dict):
            start_date = datetime.fromisoformat(date_range.get('start'))
            end_date = datetime.fromisoformat(date_range.get('end'))
        else:
            start_date = end_date - timedelta(days=30)
        
        logger.info(f"Analyzing correlation for {city}/{symbol} ({weather_var} vs {stock_var})")
        
        # Fetch data
        combined_data = data_service.get_combined_data(
            city=city,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )
        
        # Perform correlation analysis
        result = correlation_service.analyze_correlation(
            city=city,
            symbol=symbol,
            weather_data=combined_data['weather'],
            stock_data=combined_data['stock'],
            weather_variable=weather_var,
            stock_variable=stock_var
        )
        
        if not result:
            return jsonify({'error': 'Correlation analysis failed'}), 500
        
        return jsonify({
            'success': True,
            'correlation': result.to_dict()
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing correlation: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@correlation_bp.route('/<correlation_id>', methods=['GET'])
def get_correlation(correlation_id):
    """
    Get correlation result by ID.
    
    Path parameter:
        correlation_id: UUID of correlation result
    """
    try:
        result = CorrelationResult.query.get(correlation_id)
        
        if not result:
            return jsonify({'error': 'Correlation result not found'}), 404
        
        return jsonify({
            'success': True,
            'correlation': result.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting correlation: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@correlation_bp.route('/recent', methods=['GET'])
def get_recent_correlations():
    """
    Get recent correlation results.
    
    Query parameters:
        - limit: Number of results to return (default: 10, max: 100)
    """
    try:
        limit = min(int(request.args.get('limit', 10)), 100)
        
        results = CorrelationResult.get_recent(limit=limit)
        
        return jsonify({
            'success': True,
            'correlations': [r.to_dict() for r in results],
            'count': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting recent correlations: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@correlation_bp.route('/search', methods=['GET'])
def search_correlations():
    """
    Search correlations by city and symbol.
    
    Query parameters:
        - city: City name
        - symbol: Stock symbol
    """
    try:
        city = request.args.get('city')
        symbol = request.args.get('symbol')
        
        if not city or not symbol:
            return jsonify({'error': 'Missing required parameters: city, symbol'}), 400
        
        results = CorrelationResult.get_by_city_and_symbol(city, symbol)
        
        return jsonify({
            'success': True,
            'correlations': [r.to_dict() for r in results],
            'count': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching correlations: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@correlation_bp.route('/insights/<correlation_id>', methods=['GET'])
def get_insights(correlation_id):
    """
    Get detailed insights for a correlation result.
    
    Path parameter:
        correlation_id: UUID of correlation result
    """
    try:
        result = CorrelationResult.query.get(correlation_id)
        
        if not result:
            return jsonify({'error': 'Correlation result not found'}), 404
        
        insights = {
            'id': result.id,
            'summary': result.analysis_notes,
            'correlation': {
                'value': float(result.correlation_value),
                'strength': result.get_correlation_strength(),
                'direction': result.get_correlation_direction()
            },
            'significance': {
                'p_value': float(result.p_value),
                'level': result.significance_level,
                'category': result.get_significance_category()
            },
            'data': {
                'sample_size': result.sample_size,
                'period_days': result.period_days,
                'anomalies': result.anomalies_detected
            },
            'metadata': {
                'city': result.city,
                'symbol': result.symbol,
                'weather_variable': result.weather_variable,
                'stock_variable': result.stock_variable,
                'calculated_at': result.calculated_at.isoformat()
            }
        }
        
        return jsonify({
            'success': True,
            'insights': insights
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting insights: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@correlation_bp.route('/ai-insights/<correlation_id>', methods=['GET'])
def get_ai_insights(correlation_id):
    """
    Generate AI-powered insights for a correlation result.
    
    Path parameter:
        correlation_id: UUID of correlation result
    """
    try:
        result = CorrelationResult.query.get(correlation_id)
        
        if not result:
            return jsonify({'error': 'Correlation result not found'}), 404
        
        # Prepare data for AI analysis
        correlation_data = {
            'correlation_value': float(result.correlation_value),
            'p_value': float(result.p_value),
            'sample_size': result.sample_size,
            'city': result.city,
            'symbol': result.symbol,
            'weather_variable': result.weather_variable,
            'stock_variable': result.stock_variable,
            'anomalies_detected': result.anomalies_detected,
            'period_days': result.period_days
        }
        
        # Generate AI insights
        ai_insights = ai_insights_service.generate_insight(correlation_data)
        
        return jsonify({
            'success': True,
            'ai_insights': ai_insights,
            'correlation_id': correlation_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating AI insights: {e}", exc_info=True)
        return jsonify({'error': 'Failed to generate AI insights', 'details': str(e)}), 500

