"""
Data Weaver Dashboard - Flask Application
Main application entry point with API routes and configuration.
"""

import logging
import sys
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import get_config
from backend.models import init_db
from backend.routes import data_bp, correlation_bp
import backend.routes.correlation_extended  # Registers /matrix and /trends routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    logger.info(f"Starting Data Weaver Dashboard with {config_class.__name__}")
    
    # Initialize extensions
    # Enable CORS with full support for preflight requests
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(data_bp)
    app.register_blueprint(correlation_bp)  # Includes extended routes from correlation_extended.py
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'Data Weaver Dashboard',
            'version': '1.0.0'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information."""
        return jsonify({
            'service': 'Data Weaver Dashboard API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'data': {
                    'refresh': 'POST /api/data/refresh',
                    'timeseries': 'GET /api/data/timeseries'
                },
                'correlations': {
                    'analyze': 'POST /api/correlations/analyze',
                    'get': 'GET /api/correlations/<id>',
                    'recent': 'GET /api/correlations/recent',
                    'search': 'GET /api/correlations/search',
                    'insights': 'GET /api/correlations/insights/<id>'
                }
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Not found', 'message': str(error)}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal error: {error}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions."""
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred',
            'message': str(error)
        }), 500
    
    # Create database tables
    with app.app_context():
        from backend.models import db
        db.create_all()
        logger.info("Database tables created")
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
