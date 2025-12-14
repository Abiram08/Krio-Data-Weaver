/**
 * Main Dashboard Component
 * Orchestrates all sub-components including advanced features
 */

import React, { useState, useEffect } from 'react';
import ControlPanel from './ControlPanel';
import VisualizationPanel from './VisualizationPanel';
import MetricsPanel from './MetricsPanel';
import InsightsPanel from './InsightsPanel';
import AIInsightsPanel from './AIInsightsPanel';
import CorrelationMatrix from './CorrelationMatrix';
import HistoricalTrends from './HistoricalTrends';
import { MetricsSkeleton, ChartSkeleton, InsightsSkeleton } from './LoadingSkeletons';
import { useToast } from './ToastProvider';
import apiClient, { CorrelationResult, WeatherData, StockData } from '../services/api';

const Dashboard: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [correlationResult, setCorrelationResult] = useState<CorrelationResult | null>(null);
    const [weatherData, setWeatherData] = useState<WeatherData[]>([]);
    const [stockData, setStockData] = useState<StockData[]>([]);
    const [city, setCity] = useState('New York');
    const [symbol, setSymbol] = useState('AAPL');
    const [dateRange, setDateRange] = useState('30d');

    const { showToast } = useToast();

    const handleRefresh = async (
        newCity: string,
        newSymbol: string,
        newDateRange: string
    ) => {
        setLoading(true);
        setError(null);
        setCity(newCity);
        setSymbol(newSymbol);
        setDateRange(newDateRange);

        try {
            // Step 1: Refresh data from external sources
            const dataResponse = await apiClient.refreshData({
                city: newCity,
                symbol: newSymbol,
                dateRange: newDateRange,
            });

            if (dataResponse.success) {
                setWeatherData(dataResponse.data.weather);
                setStockData(dataResponse.data.stock);

                // Step 2: Analyze correlation
                const correlationResponse = await apiClient.analyzeCorrelation({
                    city: newCity,
                    symbol: newSymbol,
                    dateRange: newDateRange,
                    weatherVariable: 'temperature',
                    stockVariable: 'close_price',
                });

                if (correlationResponse.success) {
                    setCorrelationResult(correlationResponse.correlation);

                    // Success toast
                    showToast(
                        `✨ Analysis complete! Found ${Math.abs(correlationResponse.correlation.correlation_value).toFixed(2)} correlation with ${correlationResponse.correlation.sample_size} data points.`,
                        'success',
                        5000
                    );
                }
            }
        } catch (err: any) {
            const errorMessage = err.response?.data?.error || err.message || 'An error occurred';
            setError(errorMessage);

            // Error toast
            showToast(
                `❌ Analysis failed: ${errorMessage}`,
                'error',
                6000
            );

            console.error('Dashboard error:', err);
        } finally {
            setLoading(false);
        }
    };

    // Load initial data - REMOVED auto-analysis
    // User must click "Analyze Correlation" button to start

    return (
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
            {/* Control Panel */}
            <ControlPanel
                onRefresh={handleRefresh}
                loading={loading}
                initialCity={city}
                initialSymbol={symbol}
                initialDateRange={dateRange}
            />

            {/* Error Display */}
            {error && (
                <div className="mt-6 bg-white border-2 border-red-500 rounded-xl p-6 animate-fade-in">
                    <div className="flex items-start space-x-4">
                        <svg
                            className="w-8 h-8 text-red-500 flex-shrink-0 mt-1"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                        >
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        <div className="flex-1">
                            <h3 className="text-xl font-bold text-black mb-2">⚠️ Analysis Failed</h3>
                            <p className="text-gray-800 mb-4">{error}</p>

                            <div className="bg-gray-50 border border-gray-300 rounded-lg p-4 mt-4">
                                <h4 className="font-semibold text-black mb-2">💡 Need API Keys?</h4>
                                <p className="text-sm text-gray-700 mb-3">
                                    Climate Signal requires free API keys to fetch weather and stock data.
                                </p>
                                <div className="space-y-2 text-sm">
                                    <div>
                                        <strong className="text-black">OpenWeatherMap:</strong>{' '}
                                        <a href="https://openweathermap.org/api" target="_blank" rel="noopener noreferrer" className="text-[#C15F3C] hover:underline">
                                            Get Free Key →
                                        </a>
                                    </div>
                                    <div>
                                        <strong className="text-black">Alpha Vantage:</strong>{' '}
                                        <a href="https://www.alphavantage.co/support/#api-key" target="_blank" rel="noopener noreferrer" className="text-[#C15F3C] hover:underline">
                                            Get Free Key →
                                        </a>
                                    </div>
                                </div>
                                <p className="text-xs text-gray-600 mt-3">
                                    Add keys to <code className="bg-gray-200 px-2 py-1 rounded">.env</code> file and restart the backend server.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Loading State with Skeletons */}
            {loading && (
                <div className="mt-6 space-y-6">
                    <MetricsSkeleton />
                    <ChartSkeleton />
                    <InsightsSkeleton />
                </div>
            )}

            {/* Results Display */}
            {!loading && correlationResult && (
                <div className="space-y-6">
                    {/* Metrics Panel */}
                    <MetricsPanel correlation={correlationResult} />

                    {/* Visualization Panel */}
                    <VisualizationPanel
                        weatherData={weatherData}
                        stockData={stockData}
                        correlation={correlationResult}
                    />

                    {/* Insights Panel */}
                    <InsightsPanel
                        correlation={correlationResult}
                        weatherData={weatherData}
                        stockData={stockData}
                    />

                    {/* ⭐ NEW FEATURE: AI-Powered Insights */}
                    <AIInsightsPanel correlationId={correlationResult.id} />

                    {/* ⭐ NEW FEATURE: Correlation Matrix Heatmap */}
                    <CorrelationMatrix
                        city={city}
                        symbol={symbol}
                        dateRange={dateRange}
                    />

                    {/* ⭐ NEW FEATURE: Historical Trends */}
                    <HistoricalTrends
                        city={city}
                        symbol={symbol}
                        weatherVariable="temperature"
                        stockVariable="close_price"
                    />
                </div>
            )}

            {/* No Data State */}
            {!loading && !correlationResult && !error && (
                <div className="mt-16 text-center py-12">
                    <div className="inline-block p-6 bg-gradient-to-br from-[#C15F3C]/10 to-[#E07A47]/10 rounded-full mb-6">
                        <svg
                            className="w-20 h-20 text-[#C15F3C]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={1.5}
                                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                            />
                        </svg>
                    </div>
                    <h3 className="text-2xl font-bold text-[#2D2A26] mb-3">
                        Welcome to Climate Signal
                    </h3>
                    <p className="text-[#5D5A54] max-w-md mx-auto mb-8">
                        Select a city, stock symbol, and date range above, then click
                        <span className="font-semibold text-[#C15F3C]"> "Analyze Correlation" </span>
                        to discover hidden patterns between weather and markets.
                    </p>
                    <div className="flex items-center justify-center space-x-8 text-sm text-[#5D5A54]">
                        <div className="flex items-center space-x-2">
                            <svg className="w-5 h-5 text-[#6B8E4E]" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <span>AI Insights</span>
                        </div>
                        <div className="flex items-center space-x-2">
                            <svg className="w-5 h-5 text-[#6B8E4E]" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <span>Matrix Heatmap</span>
                        </div>
                        <div className="flex items-center space-x-2">
                            <svg className="w-5 h-5 text-[#6B8E4E]" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <span>Historical Trends</span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
