-- OtterStax Demo: Impressions Database
-- This script initializes the impressions table with sample data

CREATE TABLE IF NOT EXISTS impressions (
    impression_id INT PRIMARY KEY,
    campaign_id INT NOT NULL,
    days_since_start INT NOT NULL,
    clicks INT NOT NULL,
    conversions INT NOT NULL,
    revenue FLOAT NOT NULL
);

-- Sample data linked to campaigns
INSERT INTO impressions (impression_id, campaign_id, days_since_start, clicks, conversions, revenue) VALUES
(1, 1, 0, 355, 23, 103.93),
(2, 1, 1, 420, 28, 125.50),
(3, 1, 2, 380, 25, 112.00),
(4, 2, 0, 520, 45, 180.00),
(5, 2, 1, 490, 42, 165.50),
(6, 3, 0, 280, 18, 72.00),
(7, 3, 1, 310, 21, 84.50),
(8, 4, 0, 650, 55, 220.00),
(9, 4, 1, 680, 58, 235.00),
(10, 5, 0, 890, 72, 350.00),
(11, 5, 1, 920, 78, 380.00),
(12, 6, 0, 450, 35, 140.00),
(13, 7, 0, 320, 22, 88.00),
(14, 8, 0, 180, 12, 48.00),
(15, 9, 0, 560, 48, 192.00),
(16, 10, 0, 420, 36, 144.00);

-- Indexes for common queries
CREATE INDEX idx_campaign_id ON impressions(campaign_id);
CREATE INDEX idx_clicks ON impressions(clicks);
CREATE INDEX idx_revenue ON impressions(revenue);
