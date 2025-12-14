/**
 * Visualization Panel Component
 * Displays charts for weather and stock data correlation
 */

import React, { useMemo } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ChartOptions,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { WeatherData, StockData, CorrelationResult } from '../services/api';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface VisualizationPanelProps {
    weatherData: WeatherData[];
    stockData: StockData[];
    correlation: CorrelationResult;
}

const VisualizationPanel: React.FC<VisualizationPanelProps> = ({
    weatherData,
    stockData,
    correlation,
}) => {
    // Prepare chart data
    const chartData = useMemo(() => {
        // Sort and align data by timestamp
        const weatherSorted = [...weatherData].sort(
            (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        );
        const stockSorted = [...stockData].sort(
            (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
        );

        const labels = weatherSorted.map((w) =>
            new Date(w.timestamp).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
            })
        );

        const temperatures = weatherSorted.map((w) => w.temperature);
        const prices = stockSorted.map((s) => s.close_price);

        return {
            labels,
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: temperatures,
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    yAxisID: 'y',
                    tension: 0.3,
                },
                {
                    label: `${correlation.symbol} Close Price ($)`,
                    data: prices,
                    borderColor: 'rgb(168, 85, 247)',
                    backgroundColor: 'rgba(168, 85, 247, 0.5)',
                    yAxisID: 'y1',
                    tension: 0.3,
                },
            ],
        };
    }, [weatherData, stockData, correlation.symbol]);

    const chartOptions: ChartOptions<'line'> = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index' as const,
            intersect: false,
        },
        plugins: {
            legend: {
                position: 'top' as const,
                labels: {
                    color: 'rgb(203, 213, 225)',
                    font: {
                        size: 12,
                    },
                },
            },
            title: {
                display: true,
                text: `${correlation.city} Weather vs ${correlation.symbol} Stock Price`,
                color: 'rgb(248, 250, 252)',
                font: {
                    size: 16,
                    weight: 'bold',
                },
            },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleColor: 'rgb(248, 250, 252)',
                bodyColor: 'rgb(203, 213, 225)',
                borderColor: 'rgb(51, 65, 85)',
                borderWidth: 1,
            },
        },
        scales: {
            y: {
                type: 'linear' as const,
                display: true,
                position: 'left' as const,
                title: {
                    display: true,
                    text: 'Temperature (°C)',
                    color: 'rgb(59, 130, 246)',
                },
                ticks: {
                    color: 'rgb(148, 163, 184)',
                },
                grid: {
                    color: 'rgba(51, 65, 85, 0.5)',
                },
            },
            y1: {
                type: 'linear' as const,
                display: true,
                position: 'right' as const,
                title: {
                    display: true,
                    text: 'Stock Price ($)',
                    color: 'rgb(168, 85, 247)',
                },
                ticks: {
                    color: 'rgb(148, 163, 184)',
                },
                grid: {
                    drawOnChartArea: false,
                },
            },
            x: {
                ticks: {
                    color: 'rgb(148, 163, 184)',
                },
                grid: {
                    color: 'rgba(51, 65, 85, 0.5)',
                },
            },
        },
    };

    return (
        <div className="mt-6">
            <h2 className="text-2xl font-semibold text-white mb-4">Data Visualization</h2>

            <div className="card">
                <div className="h-96">
                    <Line data={chartData} options={chartOptions} />
                </div>

                <div className="mt-6 pt-6 border-t border-slate-700">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                        <div>
                            <p className="text-sm text-slate-500">Avg Temperature</p>
                            <p className="text-xl font-bold text-blue-400 mt-1">
                                {(weatherData.reduce((sum, w) => sum + w.temperature, 0) / weatherData.length).toFixed(1)}°C
                            </p>
                        </div>

                        <div>
                            <p className="text-sm text-slate-500">Avg Stock Price</p>
                            <p className="text-xl font-bold text-purple-400 mt-1">
                                ${(stockData.reduce((sum, s) => sum + s.close_price, 0) / stockData.length).toFixed(2)}
                            </p>
                        </div>

                        <div>
                            <p className="text-sm text-slate-500">Temp Range</p>
                            <p className="text-xl font-bold text-slate-300 mt-1">
                                {Math.min(...weatherData.map(w => w.temperature)).toFixed(1)}° - {Math.max(...weatherData.map(w => w.temperature)).toFixed(1)}°
                            </p>
                        </div>

                        <div>
                            <p className="text-sm text-slate-500">Price Range</p>
                            <p className="text-xl font-bold text-slate-300 mt-1">
                                ${Math.min(...stockData.map(s => s.close_price)).toFixed(2)} - ${Math.max(...stockData.map(s => s.close_price)).toFixed(2)}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default VisualizationPanel;
