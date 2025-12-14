"""
MCP Client for communicating with external Model Context Protocol servers.
Handles weather and stock data retrieval via MCP protocol.
"""

import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MCPClient:
    """Client for Model Context Protocol server communication."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize MCP client with configuration.
        
        Args:
            config_path: Path to MCP configuration JSON file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.retry_count = 0
        self.max_retries = 3
        
    def _load_config(self) -> Dict[str, Any]:
        """Load MCP server configuration from JSON file."""
        if not self.config_path or not self.config_path.exists():
            logger.warning(f"MCP config not found at {self.config_path}, using defaults")
            return {"mcpServers": {}, "caching": {"enabled": True, "ttl": 3600}}
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading MCP config: {e}")
            return {"mcpServers": {}, "caching": {"enabled": True, "ttl": 3600}}
    
    def _get_server_config(self, server_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific MCP server."""
        servers = self.config.get('mcpServers', {})
        return servers.get(server_name)
    
    def _execute_mcp_command(
        self,
        server_name: str,
        method: str,
        params: Dict[str, Any],
        timeout: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Execute MCP command via subprocess.
        
        Args:
            server_name: Name of MCP server (weather, stock)
            method: Method to call
            params: Parameters for the method
            timeout: Command timeout in seconds
            
        Returns:
            Response data from MCP server or None if failed
        """
        server_config = self._get_server_config(server_name)
        if not server_config:
            logger.error(f"No configuration found for MCP server: {server_name}")
            return None
        
        try:
            # Build command
            command = [server_config['command']] + server_config.get('args', [])
            
            # Build request payload
            request_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params
            }
            
            # Execute command with timeout
            process = subprocess.run(
                command,
                input=json.dumps(request_payload),
                capture_output=True,
                text=True,
                timeout=timeout,
                env=server_config.get('env', {})
            )
            
            if process.returncode != 0:
                logger.error(f"MCP command failed: {process.stderr}")
                return None
            
            # Parse response
            response = json.loads(process.stdout)
            return response.get('result')
            
        except subprocess.TimeoutExpired:
            logger.error(f"MCP command timeout for {server_name}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MCP response: {e}")
            return None
        except Exception as e:
            logger.error(f"Error executing MCP command: {e}")
            return None
    
    def get_weather_data(
        self,
        city: str,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch weather data from Weather MCP server.
        
        Args:
            city: City name
            start_date: Start date for data range
            end_date: End date for data range
            
        Returns:
            List of weather data points or None if failed
        """
        logger.info(f"Fetching weather data for {city} from {start_date} to {end_date}")
        
        params = {
            "city": city,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        result = self._execute_mcp_command('weather', 'get_weather', params)
        
        if result:
            logger.info(f"Retrieved {len(result.get('data', []))} weather data points")
            return result.get('data', [])
        
        # Retry logic
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            time.sleep(2 ** self.retry_count)  # Exponential backoff
            return self.get_weather_data(city, start_date, end_date)
        
        self.retry_count = 0
        logger.error(f"Failed to fetch weather data after {self.max_retries} retries")
        return None
    
    def get_stock_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch stock data from Stock MCP server.
        
        Args:
            symbol: Stock symbol (e.g., AAPL, GOOGL)
            start_date: Start date for data range
            end_date: End date for data range
            
        Returns:
            List of stock data points or None if failed
        """
        logger.info(f"Fetching stock data for {symbol} from {start_date} to {end_date}")
        
        params = {
            "symbol": symbol.upper(),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        result = self._execute_mcp_command('stock', 'get_stock', params)
        
        if result:
            logger.info(f"Retrieved {len(result.get('data', []))} stock data points")
            return result.get('data', [])
        
        # Retry logic
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            time.sleep(2 ** self.retry_count)  # Exponential backoff
            return self.get_stock_data(symbol, start_date, end_date)
        
        self.retry_count = 0
        logger.error(f"Failed to fetch stock data after {self.max_retries} retries")
        return None
    
    def test_connection(self, server_name: str) -> bool:
        """
        Test connection to an MCP server.
        
        Args:
            server_name: Name of server to test
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = self._execute_mcp_command(
                server_name,
                'health_check',
                {},
                timeout=10
            )
            return result is not None
        except Exception as e:
            logger.error(f"Connection test failed for {server_name}: {e}")
            return False
