-- Data Weaver Dashboard Database Schema
-- PostgreSQL 15+

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Weather Data Table
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    city VARCHAR(100) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    humidity INTEGER NOT NULL CHECK (humidity >= 0 AND humidity <= 100),
    precipitation DECIMAL(6,2) DEFAULT 0 CHECK (precipitation >= 0),
    wind_speed DECIMAL(5,2) NOT NULL CHECK (wind_speed >= 0),
    condition VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for weather_data
CREATE INDEX IF NOT EXISTS idx_weather_city_timestamp ON weather_data(city, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_weather_timestamp ON weather_data(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_data(city);

-- Stock Data Table
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    open_price DECIMAL(12,4) NOT NULL CHECK (open_price > 0),
    close_price DECIMAL(12,4) NOT NULL CHECK (close_price > 0),
    high_price DECIMAL(12,4) NOT NULL CHECK (high_price > 0),
    low_price DECIMAL(12,4) NOT NULL CHECK (low_price > 0),
    volume BIGINT NOT NULL CHECK (volume >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT valid_price_range CHECK (
        low_price <= open_price AND
        low_price <= close_price AND
        open_price <= high_price AND
        close_price <= high_price
    )
);

-- Indexes for stock_data
CREATE INDEX IF NOT EXISTS idx_stock_symbol_timestamp ON stock_data(symbol, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_stock_timestamp ON stock_data(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_stock_symbol ON stock_data(symbol);

-- Correlation Results Table
CREATE TABLE IF NOT EXISTS correlation_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    city VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    period_days INTEGER NOT NULL CHECK (period_days > 0),
    correlation_value DECIMAL(8,6) NOT NULL CHECK (correlation_value >= -1.0 AND correlation_value <= 1.0),
    p_value DECIMAL(10,8) NOT NULL CHECK (p_value >= 0 AND p_value <= 1),
    sample_size INTEGER NOT NULL CHECK (sample_size > 0),
    weather_variable VARCHAR(50) NOT NULL,
    stock_variable VARCHAR(50) NOT NULL,
    significance_level VARCHAR(20),
    analysis_notes TEXT,
    anomalies_detected INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for correlation_results
CREATE INDEX IF NOT EXISTS idx_correlation_city_symbol ON correlation_results(city, symbol);
CREATE INDEX IF NOT EXISTS idx_correlation_calculated_at ON correlation_results(calculated_at DESC);
CREATE INDEX IF NOT EXISTS idx_correlation_values ON correlation_results(correlation_value, p_value);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_weather_data_updated_at
    BEFORE UPDATE ON weather_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stock_data_updated_at
    BEFORE UPDATE ON stock_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_correlation_results_updated_at
    BEFORE UPDATE ON correlation_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create view for recent correlations
CREATE OR REPLACE VIEW recent_correlations AS
SELECT 
    id,
    calculated_at,
    city,
    symbol,
    period_days,
    correlation_value,
    p_value,
    sample_size,
    significance_level,
    anomalies_detected
FROM correlation_results
ORDER BY calculated_at DESC
LIMIT 100;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dataweaver_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dataweaver_user;
