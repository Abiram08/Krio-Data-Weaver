"""Initialize routes package."""

from flask import Blueprint

# Create blueprints
data_bp = Blueprint('data', __name__, url_prefix='/api/data')
correlation_bp = Blueprint('correlations', __name__, url_prefix='/api/correlations')

# Import routes to register them with blueprints
from backend.routes import data, correlations

__all__ = ['data_bp', 'correlation_bp']

