/**
 * Export utility functions for data and reports
 */

import { CorrelationResult, WeatherData, StockData } from './api';

/**
 * Export data to CSV format
 */
export const exportToCSV = (data: any[], filename: string): void => {
    if (!data || data.length === 0) return;

    // Get headers from first object
    const headers = Object.keys(data[0]);

    // Create CSV content
    const csvContent = [
        headers.join(','),
        ...data.map(row =>
            headers.map(header => {
                const value = row[header];
                // Escape commas and quotes
                if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                    return `"${value.replace(/"/g, '""')}"`;
                }
                return value;
            }).join(',')
        )
    ].join('\n');

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', `${filename}.csv`);
    link.style.visibility = 'hidden';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

/**
 * Export correlation data with weather and stock data
 */
export const exportCorrelationData = (
    correlation: CorrelationResult,
    weatherData: WeatherData[],
    stockData: StockData[]
): void => {
    const combinedData = weatherData.map((w, index) => {
        const stock = stockData[index] || {};
        return {
            timestamp: w.timestamp,
            city: w.city,
            temperature: w.temperature,
            humidity: w.humidity,
            precipitation: w.precipitation,
            wind_speed: w.wind_speed,
            condition: w.condition,
            symbol: stock.symbol || '',
            open_price: stock.open_price || '',
            close_price: stock.close_price || '',
            high_price: stock.high_price || '',
            low_price: stock.low_price || '',
            volume: stock.volume || ''
        };
    });

    const filename = `correlation_${correlation.city}_${correlation.symbol}_${new Date().toISOString().split('T')[0]}`;
    exportToCSV(combinedData, filename);
};

/**
 * Export correlation results summary
 */
export const exportCorrelationSummary = (correlation: CorrelationResult): void => {
    const summary = [{
        id: correlation.id,
        city: correlation.city,
        symbol: correlation.symbol,
        correlation_coefficient: correlation.correlation_value,
        p_value: correlation.p_value,
        significance_level: correlation.significance,
        sample_size: correlation.sample_size,
        period_days: correlation.period_days,
        weather_variable: correlation.weather_variable,
        stock_variable: correlation.stock_variable,
        anomalies_detected: correlation.anomalies_detected,
        analysis_notes: correlation.analysis_notes,
        calculated_at: correlation.calculated_at
    }];

    const filename = `correlation_summary_${correlation.id}`;
    exportToCSV(summary, filename);
};

/**
 * Export data to JSON format
 */
export const exportToJSON = (data: any, filename: string): void => {
    const jsonContent = JSON.stringify(data, null, 2);

    const blob = new Blob([jsonContent], { type: 'application/json' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', `${filename}.json`);
    link.style.visibility = 'hidden';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

/**
 * Generate and download PDF report (simplified version)
 */
export const generatePDFReport = (
    correlation: CorrelationResult,
    weatherData: WeatherData[],
    stockData: StockData[]
): void => {
    // Create HTML content for PDF
    const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <title>Correlation Analysis Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    h1 { color: #0ea5e9; }
    h2 { color: #0369a1; margin-top: 30px; }
    .metric { background: #f1f5f9; padding: 15px; margin: 10px 0; border-radius: 8px; }
    .metric-label { font-weight: bold; color: #475569; }
    .metric-value { font-size: 24px; color: #0f172a; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #cbd5e1; padding: 8px; text-align: left; }
    th { background: #e2e8f0; }
  </style>
</head>
<body>
  <h1>Data Weaver Dashboard - Correlation Analysis Report</h1>
  
  <div class="metric">
    <div class="metric-label">Analysis Date</div>
    <div>${new Date(correlation.calculated_at).toLocaleString()}</div>
  </div>

  <h2>Data Sources</h2>
  <div class="metric">
    <div class="metric-label">Location</div>
    <div>${correlation.city}</div>
  </div>
  <div class="metric">
    <div class="metric-label">Stock Symbol</div>
    <div>${correlation.symbol}</div>
  </div>
  <div class="metric">
    <div class="metric-label">Time Period</div>
    <div>${correlation.period_days} days (${correlation.sample_size} data points)</div>
  </div>

  <h2>Correlation Results</h2>
  <div class="metric">
    <div class="metric-label">Correlation Coefficient</div>
    <div class="metric-value">${correlation.correlation_value.toFixed(4)}</div>
  </div>
  <div class="metric">
    <div class="metric-label">P-Value (Statistical Significance)</div>
    <div class="metric-value">${correlation.p_value < 0.001 ? '<0.001' : correlation.p_value.toFixed(4)}</div>
  </div>
  <div class="metric">
    <div class="metric-label">Anomalies Detected</div>
    <div>${correlation.anomalies_detected}</div>
  </div>

  <h2>Analysis Insights</h2>
  <p>${correlation.analysis_notes}</p>

  <h2>Data Summary</h2>
  <h3>Weather Statistics (${correlation.weather_variable})</h3>
  <table>
    <tr>
      <th>Metric</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Average Temperature</td>
      <td>${(weatherData.reduce((sum, w) => sum + w.temperature, 0) / weatherData.length).toFixed(2)}°C</td>
    </tr>
    <tr>
      <td>Min Temperature</td>
      <td>${Math.min(...weatherData.map(w => w.temperature)).toFixed(2)}°C</td>
    </tr>
    <tr>
      <td>Max Temperature</td>
      <td>${Math.max(...weatherData.map(w => w.temperature)).toFixed(2)}°C</td>
    </tr>
  </table>

  <h3>Stock Statistics (${correlation.stock_variable})</h3>
  <table>
    <tr>
      <th>Metric</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Average Close Price</td>
      <td>$${(stockData.reduce((sum, s) => sum + s.close_price, 0) / stockData.length).toFixed(2)}</td>
    </tr>
    <tr>
      <td>Min Close Price</td>
      <td>$${Math.min(...stockData.map(s => s.close_price)).toFixed(2)}</td>
    </tr>
    <tr>
      <td>Max Close Price</td>
      <td>$${Math.max(...stockData.map(s => s.close_price)).toFixed(2)}</td>
    </tr>
  </table>

  <hr/>
  <p style="text-align: center; color: #64748b; font-size: 12px;">
    Generated by Data Weaver Dashboard | ${new Date().toLocaleDateString()}
  </p>
</body>
</html>
  `;

    // Create blob and download as HTML (user can print to PDF)
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    const filename = `correlation_report_${correlation.city}_${correlation.symbol}_${new Date().toISOString().split('T')[0]}`;
    link.setAttribute('href', url);
    link.setAttribute('download', `${filename}.html`);
    link.style.visibility = 'hidden';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Alert user to print to PDF
    setTimeout(() => {
        alert('Report downloaded as HTML. Open the file and use your browser\'s "Print to PDF" feature to create a PDF.');
    }, 500);
};
