/**
 * Historical Trends Component  
 * Shows correlation trends over time - Fixed type errors
 */

import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import api from '../services/api';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

interface HistoricalTrendsProps {
    city: string;
    symbol: string;
    weatherVariable?: string;
    stockVariable?: string;
}

const HistoricalTrends: React.FC<HistoricalTrendsProps> = ({ city, symbol, weatherVariable = 'temperature', stockVariable = 'close_price' }) => {
    const [trends, setTrends] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (city && symbol) fetchTrends();
    }, [city, symbol, weatherVariable, stockVariable]);

    const fetchTrends = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.post('/correlations/trends', { city, symbol, weather_variable: weatherVariable, stock_variable: stockVariable, window_days: 30, total_days: 180 });
            setTrends(response.data);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to load historical trends');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="card mt-6"><h3 className="text-xl font-bold text-[#C15F3C] mb-4">Historical Trends</h3><div className="flex items-center justify-center py-12"><div className="spinner"></div></div></div>;
    if (error) return <div className="card mt-6"><h3 className="text-xl font-bold text-[#C15F3C] mb-4">Historical Trends</h3><div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 text-red-800">{error}</div></div>;
    if (!trends || !trends.trends || trends.trends.length === 0) return null;

    const chartData = { labels: trends.trends.map((t: any) => t.period_label), datasets: [{ label: 'Correlation', data: trends.trends.map((t: any) => t.correlation), borderColor: '#C15F3C', backgroundColor: 'rgba(193, 95, 60, 0.1)', borderWidth: 3, pointRadius: 6, pointBackgroundColor: trends.trends.map((t: any) => t.significant ? '#6B8E4E' : '#C15F3C'), pointBorderColor: '#fff', pointBorderWidth: 2, tension: 0.4, fill: true }] };

    const chartOptions: any = { responsive: true, maintainAspectRatio: false, scales: { y: { min: -1, max: 1 } } };
    const avgCorrelation = trends.trends.reduce((sum: number, t: any) => sum + t.correlation, 0) / trends.trends.length;
    const significantCount = trends.trends.filter((t: any) => t.significant).length;

    return (
        <div className="card mt-6">
            <h3 className="text-2xl font-bold text-[#C15F3C] mb-4">Historical Correlation Trends</h3>
            <div className="bg-white rounded-lg p-4" style={{ height: '400px' }}><Line data={chartData} options={chartOptions} /></div>
            <div className="mt-4 p-4 bg-secondary-50 rounded-lg"><p className="text-sm text-[#5D5A54]">Avg: {avgCorrelation.toFixed(3)} | Significant periods: {significantCount}/{trends.trends.length}</p></div>
        </div>
    );
};

export default HistoricalTrends;
