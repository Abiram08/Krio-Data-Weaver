/**
 * Correlation Matrix Heatmap Component
 * Shows all weather vs stock variable correlations
 */

import React, { useState, useEffect } from 'react';
import api from '../services/api';

interface CorrelationMatrixProps {
    city: string;
    symbol: string;
    dateRange: string;
}

const CorrelationMatrix: React.FC<CorrelationMatrixProps> = ({ city, symbol, dateRange }) => {
    const [matrix, setMatrix] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Auto-fetch disabled - only load after button click
    // useEffect(() => {
    //     if (city && symbol) {
    //         fetchMatrix();
    //     }
    // }, [city, symbol, dateRange]);

    const fetchMatrix = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.post('/correlations/matrix', {
                city,
                symbol,
                dateRange
            });
            setMatrix(response.data);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to load correlation matrix');
        } finally {
            setLoading(false);
        }
    };

    const getColorForCorrelation = (r: number): string => {
        // Strong negative: dark red
        // Weak: white
        // Strong positive: dark green
        const absR = Math.abs(r);

        if (r > 0) {
            // Positive correlation - shades of green
            if (absR > 0.7) return 'bg-green-600 text-white';
            if (absR > 0.4) return 'bg-green-400 text-white';
            if (absR > 0.2) return 'bg-green-200 text-gray-800';
            return 'bg-green-50 text-gray-800';
        } else {
            // Negative correlation - shades of red
            if (absR > 0.7) return 'bg-red-600 text-white';
            if (absR > 0.4) return 'bg-red-400 text-white';
            if (absR > 0.2) return 'bg-red-200 text-gray-800';
            return 'bg-red-50 text-gray-800';
        }
    };

    const formatVariableName = (name: string): string => {
        return name.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    };

    if (loading) {
        return (
            <div className="card mt-6">
                <h3 className="text-xl font-bold text-[#C15F3C] mb-4">Correlation Matrix</h3>
                <div className="flex items-center justify-center py-12">
                    <div className="flex flex-col items-center space-y-3">
                        <div className="spinner"></div>
                        <p className="text-[#5D5A54]">Calculating correlation matrix...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card mt-6">
                <h3 className="text-xl font-bold text-[#C15F3C] mb-4">Correlation Matrix</h3>
                <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 text-red-800">
                    {error}
                </div>
            </div>
        );
    }

    if (!matrix) return null;

    return (
        <div className="card mt-6">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="text-2xl font-bold text-[#C15F3C]">Correlation Matrix</h3>
                    <p className="text-sm text-[#5D5A54] mt-1">
                        All weather variables vs all stock variables • Sample size: {matrix.sample_size}
                    </p>
                </div>
                <div className="flex items-center space-x-4 text-xs">
                    <div className="flex items-center space-x-2">
                        <div className="w-4 h-4 bg-red-500 rounded"></div>
                        <span className="text-[#5D5A54]">Negative</span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <div className="w-4 h-4 bg-white border border-gray-300 rounded"></div>
                        <span className="text-[#5D5A54]">Weak</span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <div className="w-4 h-4 bg-green-500 rounded"></div>
                        <span className="text-[#5D5A54]">Positive</span>
                    </div>
                </div>
            </div>

            {/* Matrix Table */}
            <div className="overflow-x-auto">
                <table className="w-full border-collapse">
                    <thead>
                        <tr>
                            <th className="border border-[#B1ADA1]/30 p-3 bg-secondary-100 text-left font-semibold text-[#2D2A26]">
                                Weather ↓ / Stock →
                            </th>
                            {matrix.stock_variables.map((stockVar: string) => (
                                <th key={stockVar} className="border border-[#B1ADA1]/30 p-3 bg-secondary-100 text-center font-semibold text-[#2D2A26] text-sm">
                                    {formatVariableName(stockVar)}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {matrix.matrix.map((row: any) => (
                            <tr key={row.variable} className="hover:bg-secondary-50 transition-colors">
                                <td className="border border-[#B1ADA1]/30 p-3 font-semibold text-[#2D2A26]">
                                    {formatVariableName(row.variable)}
                                </td>
                                {matrix.stock_variables.map((stockVar: string) => {
                                    const cell = row.correlations[stockVar];
                                    if (!cell) return <td key={stockVar} className="border border-[#B1ADA1]/30 p-3">-</td>;

                                    return (
                                        <td
                                            key={stockVar}
                                            className={`border border-[#B1ADA1]/30 p-3 text-center transition-all hover:scale-105 cursor-help ${getColorForCorrelation(cell.r)}`}
                                            title={`r=${cell.r.toFixed(3)}, p=${cell.p.toFixed(4)}${cell.significant ? ' (significant)' : ''}`}
                                        >
                                            <div className="font-mono font-bold text-sm">
                                                {cell.r >= 0 ? '+' : ''}{cell.r.toFixed(2)}
                                            </div>
                                            {cell.significant && (
                                                <div className="text-xs mt-1">
                                                    <span className="inline-block w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></span>
                                                </div>
                                            )}
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Legend */}
            <div className="mt-6 p-4 bg-secondary-50 rounded-lg border border-[#B1ADA1]/30">
                <h4 className="font-semibold text-[#2D2A26] mb-2 flex items-center space-x-2">
                    <svg className="w-5 h-5 text-[#C15F3C]" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                        <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>How to Read This Matrix</span>
                </h4>
                <ul className="text-sm text-[#5D5A54] space-y-1">
                    <li>• <strong>Values range from -1 to +1:</strong> Closer to -1 or +1 indicates stronger correlation</li>
                    <li>• <strong>Green cells:</strong> Positive correlation (variables move together)</li>
                    <li>• <strong>Red cells:</strong> Negative correlation (variables move opposite)</li>
                    <li>• <strong>Yellow dot:</strong> Statistically significant (p &lt; 0.05)</li>
                    <li>• <strong>Hover over cells</strong> to see exact r and p-values</li>
                </ul>
            </div>
        </div>
    );
};

export default CorrelationMatrix;
