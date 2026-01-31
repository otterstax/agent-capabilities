-- OtterStax Demo: Campaigns Database
-- This script initializes the campaigns table with sample data

CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INT PRIMARY KEY,
    campaign_name VARCHAR(255) NOT NULL,
    campaign_length INT NOT NULL,
    budget FLOAT NOT NULL
);

-- Sample data
INSERT INTO campaigns (campaign_id, campaign_name, campaign_length, budget) VALUES
(1, 'Campaign Education Training', 43, 71560.16),
(2, 'Campaign Front Point', 43, 91168.80),
(3, 'Campaign Digital Marketing', 30, 45000.00),
(4, 'Campaign Social Media', 60, 82500.50),
(5, 'Campaign Brand Awareness', 90, 120000.00),
(6, 'Campaign Product Launch', 45, 95000.00),
(7, 'Campaign Holiday Special', 30, 55000.00),
(8, 'Campaign Year End Sale', 15, 35000.00),
(9, 'Campaign Spring Collection', 60, 78000.00),
(10, 'Campaign Summer Promo', 45, 62000.00);

-- Index for common queries
CREATE INDEX idx_campaign_length ON campaigns(campaign_length);
CREATE INDEX idx_budget ON campaigns(budget);
