/**
 * Insights Panel Component
 * Displays generated insights and analysis notes with export functionality
 */

import React from 'react';
import { CorrelationResult, WeatherData, StockData } from '../services/api';
import { exportCorrelationData, exportCorrelationSummary, exportToJSON, generatePDFReport } from '../services/export';

interface InsightsPanelProps {
    correlation: CorrelationResult;
    weatherData?: WeatherData[];
    stockData?: StockData[];
}

const InsightsPanel: React.FC<InsightsPanelProps> = ({ correlation, weatherData = [], stockData = [] }) => {
    const handleExportCSV = () => {
        if (weatherData.length > 0 && stockData.length > 0) {
            exportCorrelationData(correlation, weatherData, stockData);
        }
    };

    const handleExportSummary = () => {
        exportCorrelationSummary(correlation);
    };

    const handleExportJSON = () => {
        exportToJSON({
            correlation,
            weatherData,
            stockData
        }, `correlation_data_${correlation.id}`);
    };

    const handleExportPDF = () => {
        if (weatherData.length > 0 && stockData.length > 0) {
            generatePDFReport(correlation, weatherData, stockData);
        }
    };

    const getInsightIcon = (pValue: number) => {
        if (pValue < 0.05) {
            return (
                <svg
                    className="w-6 h-6 text-green-400"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            );
        }
        return (
            <svg
                className="w-6 h-6 text-yellow-400"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        );
    };

    return (
        <div className="mt-6">
            <h2 className="text-2xl font-semibold text-black mb-4">Insights & Analysis</h2>

            <div className="card bg-white border-2 border-gray-200">
                <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0 mt-1">
                        {getInsightIcon(correlation.p_value)}
                    </div>

                    <div className="flex-1">
                        <h3 className="text-lg font-semibold text-black mb-3">
                            Statistical Analysis
                        </h3>

                        <div className="prose prose-invert max-w-none">
                            <p className="text-black leading-relaxed">
                                {correlation.analysis_notes}
                            </p>
                        </div>

                        <div className="mt-6 pt-6 border-t border-slate-700">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                <div>
                                    <p className="text-black font-medium">Data Sources</p>
                                    <p className="text-black mt-1">
                                        {correlation.city} weather × {correlation.symbol} stock prices
                                    </p>
                                </div>

                                <div>
                                    <p className="text-black font-medium">Variables Analyzed</p>
                                    <p className="text-black mt-1">
                                        {correlation.weather_variable} vs {correlation.stock_variable}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-black font-medium">Time Period</p>
                                    <p className="text-black mt-1">
                                        {correlation.period_days} days
                                    </p>
                                </div>

                                <div>
                                    <p className="text-black font-medium">Analysis Date</p>
                                    <p className="text-black mt-1">
                                        {new Date(correlation.calculated_at).toLocaleDateString()}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="mt-6 pt-6 border-t border-slate-700">
                        <h4 className="text-sm font-semibold text-black mb-3">Export Options</h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                            <button
                                onClick={handleExportCSV}
                                className="btn-secondary text-sm flex items-center justify-center space-x-2"
                                disabled={weatherData.length === 0}
                            >
                                <svg className="w-4 h-4" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                    <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                <span>CSV Data</span>
                            </button>

                            <button
                                onClick={handleExportSummary}
                                className="btn-secondary text-sm flex items-center justify-center space-x-2"
                            >
                                <svg className="w-4 h-4" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                <span>Summary</span>
                            </button>

                            <button
                                onClick={handleExportJSON}
                                className="btn-secondary text-sm flex items-center justify-center space-x-2"
                            >
                                <svg className="w-4 h-4" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                    <path d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                                </svg>
                                <span>JSON</span>
                            </button>

                            <button
                                onClick={handleExportPDF}
                                className="btn-secondary text-sm flex items-center justify-center space-x-2"
                                disabled={weatherData.length === 0}
                            >
                                <svg className="w-4 h-4" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                    <path d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                </svg>
                                <span>PDF Report</span>
                            </button>
                        </div>
                    </div>

                    {correlation.anomalies_detected > 0 && (
                        <div className="mt-6 bg-red-900/20 border border-red-800/50 rounded-lg p-4">
                            <div className="flex items-start space-x-3">
                                <svg
                                    className="w-5 h-5 text-red-400 mt-0.5"
                                    fill="none"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <div>
                                    <h4 className="text-red-300 font-medium">Anomalies Detected</h4>
                                    <p className="text-red-400 text-sm mt-1">
                                        {correlation.anomalies_detected} outlier(s) detected in the dataset. These may represent unusual
                                        market or weather events that significantly deviate from normal patterns.
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default InsightsPanel;
