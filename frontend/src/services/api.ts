/**
 * API client for Data Weaver Dashboard backend
 */

import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export interface DateRange {
    start?: string;
    end?: string;
}

export interface RefreshDataRequest {
    city: string;
    symbol: string;
    dateRange: string | DateRange;
}

export interface CorrelationRequest {
    city: string;
    symbol: string;
    dateRange: string | DateRange;
    weatherVariable?: string;
    stockVariable?: string;
}

export interface CorrelationResult {
    id: string;
    correlation_value: number;
    p_value: number;
    sample_size: number;
    significance: string;
    weather_variable: string;
    stock_variable: string;
    city: string;
    symbol: string;
    start_date: string;
    end_date: string;
    period_days: number;
    analysis_notes: string;
    anomalies_detected: number;
    calculated_at: string;
}

export interface WeatherData {
    id: number;
    timestamp: string;
    city: string;
    temperature: number;
    humidity: number;
    precipitation: number;
    wind_speed: number;
    condition: string;
}

export interface StockData {
    id: number;
    timestamp: string;
    symbol: string;
    open_price: number;
    close_price: number;
    high_price: number;
    low_price: number;
    volume: number;
}

class ApiClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Response interceptor for error handling
        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                console.error('API Error:', error.response?.data || error.message);
                return Promise.reject(error);
            }
        );
    }

    // Health check
    async healthCheck(): Promise<any> {
        const response = await this.client.get('/api/health');
        return response.data;
    }

    // Refresh data from external sources
    async refreshData(request: RefreshDataRequest): Promise<any> {
        const response = await this.client.post('/api/data/refresh', request);
        return response.data;
    }

    // Get time series data
    async getTimeSeries(
        city: string,
        symbol: string,
        startDate: string,
        endDate: string
    ): Promise<any> {
        const response = await this.client.get('/api/data/timeseries', {
            params: { city, symbol, start_date: startDate, end_date: endDate },
        });
        return response.data;
    }

    // Analyze correlation
    async analyzeCorrelation(request: CorrelationRequest): Promise<{ success: boolean; correlation: CorrelationResult }> {
        const response = await this.client.post('/api/correlations/analyze', request);
        return response.data;
    }

    // Get correlation by ID
    async getCorrelation(id: string): Promise<{ success: boolean; correlation: CorrelationResult }> {
        const response = await this.client.get(`/api/correlations/${id}`);
        return response.data;
    }

    // Get recent correlations
    async getRecentCorrelations(limit: number = 10): Promise<{ success: boolean; correlations: CorrelationResult[]; count: number }> {
        const response = await this.client.get('/api/correlations/recent', {
            params: { limit },
        });
        return response.data;
    }

    // Search correlations
    async searchCorrelations(city: string, symbol: string): Promise<{ success: boolean; correlations: CorrelationResult[]; count: number }> {
        const response = await this.client.get('/api/correlations/search', {
            params: { city, symbol },
        });
        return response.data;
    }

    // Get insights
    async getInsights(id: string): Promise<any> {
        const response = await this.client.get(`/api/correlations/insights/${id}`);
        return response.data;
    }

    // Generic GET method
    async get(endpoint: string, params?: any): Promise<any> {
        const response = await this.client.get(`/api${endpoint}`, {
            params
        });
        return response;
    }

    // Generic POST method
    async post(endpoint: string, data?: any): Promise<any> {
        const response = await this.client.post(`/api${endpoint}`, data);
        return response;
    }
}

export const apiClient = new ApiClient();
export default apiClient;
