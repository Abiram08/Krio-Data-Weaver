/**
 * Control Panel Component
 * User controls for selecting city, stock symbol, and date range
 */

import React, { useState, useEffect } from 'react';

interface ControlPanelProps {
    onRefresh: (city: string, symbol: string, dateRange: string) => void;
    loading: boolean;
    initialCity: string;
    initialSymbol: string;
    initialDateRange: string;
}

const CITIES = [
    'New York',
    'London',
    'Tokyo',
    'Paris',
    'Mumbai',
    'Los Angeles',
    'Chicago',
    'Singapore',
    'Hong Kong',
    'Sydney',
];

const POPULAR_STOCKS = [
    { symbol: 'AAPL', name: 'Apple Inc.' },
    { symbol: 'GOOGL', name: 'Alphabet Inc.' },
    { symbol: 'MSFT', name: 'Microsoft Corporation' },
    { symbol: 'AMZN', name: 'Amazon.com Inc.' },
    { symbol: 'TSLA', name: 'Tesla Inc.' },
    { symbol: 'META', name: 'Meta Platforms Inc.' },
    { symbol: 'NVDA', name: 'NVIDIA Corporation' },
    { symbol: 'JPM', name: 'JPMorgan Chase & Co.' },
];

const DATE_RANGES = [
    { value: '7d', label: '7 Days' },
    { value: '30d', label: '30 Days' },
    { value: '90d', label: '90 Days' },
    { value: '180d', label: '6 Months' },
    { value: '365d', label: '1 Year' },
];

const ControlPanel: React.FC<ControlPanelProps> = ({
    onRefresh,
    loading,
    initialCity,
    initialSymbol,
    initialDateRange,
}) => {
    const [city, setCity] = useState(initialCity);
    const [symbol, setSymbol] = useState(initialSymbol);
    const [dateRange, setDateRange] = useState(initialDateRange);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!loading && city && symbol && dateRange) {
            onRefresh(city, symbol, dateRange);
        }
    };

    return (
        <div className="card">
            <h2 className="text-xl font-semibold text-black">Data Selection</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* City Selector */}
                    <div>
                        <label htmlFor="city" className="block text-sm font-medium text-slate-300 mb-2">
                            City
                        </label>
                        <select
                            id="city"
                            className="select w-full"
                            value={city}
                            onChange={(e) => setCity(e.target.value)}
                            disabled={loading}
                        >
                            {CITIES.map((cityOption) => (
                                <option key={cityOption} value={cityOption}>
                                    {cityOption}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Stock Symbol Selector */}
                    <div>
                        <label htmlFor="symbol" className="block text-sm font-medium text-slate-300 mb-2">
                            Stock Symbol
                        </label>
                        <select
                            id="symbol"
                            className="select w-full"
                            value={symbol}
                            onChange={(e) => setSymbol(e.target.value)}
                            disabled={loading}
                        >
                            {POPULAR_STOCKS.map((stock) => (
                                <option key={stock.symbol} value={stock.symbol}>
                                    {stock.symbol} - {stock.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Date Range Selector */}
                    <div>
                        <label htmlFor="dateRange" className="block text-sm font-medium text-slate-300 mb-2">
                            Date Range
                        </label>
                        <select
                            id="dateRange"
                            className="select w-full"
                            value={dateRange}
                            onChange={(e) => setDateRange(e.target.value)}
                            disabled={loading}
                        >
                            {DATE_RANGES.map((range) => (
                                <option key={range.value} value={range.value}>
                                    {range.label}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* Analyze Button */}
                <div className="flex justify-end">
                    <button
                        type="submit"
                        className="btn-primary flex items-center space-x-2"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <svg
                                    className="animate-spin h-5 w-5 text-white"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                >
                                    <circle
                                        className="opacity-25"
                                        cx="12"
                                        cy="12"
                                        r="10"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                    ></circle>
                                    <path
                                        className="opacity-75"
                                        fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    ></path>
                                </svg>
                                <span>Analyzing...</span>
                            </>
                        ) : (
                            <>
                                <svg
                                    className="w-5 h-5"
                                    fill="none"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                                <span>Analyze Correlation</span>
                            </>
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ControlPanel;
