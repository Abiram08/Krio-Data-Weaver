/**
 * Metrics Panel Component
 * Displays KPI cards with correlation statistics
 */

import React from 'react';
import { CorrelationResult } from '../services/api';

interface MetricsPanelProps {
    correlation: CorrelationResult;
}

const MetricsPanel: React.FC<MetricsPanelProps> = ({ correlation }) => {
    const getCorrelationColor = (value: number): string => {
        const absValue = Math.abs(value);
        if (absValue >= 0.7) return 'text-green-400';
        if (absValue >= 0.4) return 'text-yellow-400';
        return 'text-slate-400';
    };

    const getSignificanceColor = (pValue: number): string => {
        if (pValue < 0.01) return 'text-green-400';
        if (pValue < 0.05) return 'text-yellow-400';
        return 'text-red-400';
    };

    const getCorrelationStrength = (value: number): string => {
        const absValue = Math.abs(value);
        if (absValue >= 0.7) return 'Strong';
        if (absValue >= 0.4) return 'Moderate';
        if (absValue >= 0.2) return 'Weak';
        return 'Very Weak';
    };

    const getSignificanceLevel = (pValue: number): string => {
        if (pValue < 0.001) return 'Very High';
        if (pValue < 0.01) return 'High';
        if (pValue < 0.05) return 'Moderate';
        return 'Not Significant';
    };

    return (
        <div className="mt-6">
            <h2 className="text-2xl font-semibold text-white mb-4">Key Metrics</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Correlation Coefficient */}
                <div className="card bg-gradient-to-br from-primary-900/50 to-primary-800/30">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Correlation Coefficient</p>
                            <p className={`text-3xl font-bold mt-2 ${getCorrelationColor(correlation.correlation_value)}`}>
                                {correlation.correlation_value.toFixed(3)}
                            </p>
                            <p className="text-xs text-slate-500 mt-1">
                                {getCorrelationStrength(correlation.correlation_value)}
                            </p>
                        </div>
                        <svg
                            className="w-12 h-12 text-primary-600"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="1.5"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    </div>
                </div>

                {/* P-Value */}
                <div className="card bg-gradient-to-br from-secondary-900/50 to-secondary-800/30">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Statistical Significance</p>
                            <p className={`text-3xl font-bold mt-2 ${getSignificanceColor(correlation.p_value)}`}>
                                {correlation.p_value < 0.001 ? '<0.001' : correlation.p_value.toFixed(4)}
                            </p>
                            <p className="text-xs text-slate-500 mt-1">
                                {getSignificanceLevel(correlation.p_value)}
                            </p>
                        </div>
                        <svg
                            className="w-12 h-12 text-secondary-600"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="1.5"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                </div>

                {/* Sample Size */}
                <div className="card bg-gradient-to-br from-slate-800/50 to-slate-700/30">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Sample Size</p>
                            <p className="text-3xl font-bold text-white mt-2">
                                {correlation.sample_size}
                            </p>
                            <p className="text-xs text-slate-500 mt-1">
                                {correlation.period_days} days
                            </p>
                        </div>
                        <svg
                            className="w-12 h-12 text-slate-600"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="1.5"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                        </svg>
                    </div>
                </div>

                {/* Anomalies */}
                <div className="card bg-gradient-to-br from-red-900/50 to-red-800/30">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Anomalies Detected</p>
                            <p className="text-3xl font-bold text-white mt-2">
                                {correlation.anomalies_detected}
                            </p>
                            <p className="text-xs text-slate-500 mt-1">
                                Outliers
                            </p>
                        </div>
                        <svg
                            className="w-12 h-12 text-red-600"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="1.5"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MetricsPanel;
