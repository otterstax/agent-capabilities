# Data Analysis Examples

Analysis patterns and queries for OtterStax.

## Table Profiling

### Row Count
```sql
SELECT COUNT(*) as total_rows 
FROM campaigns.db1.schema.campaigns;
```

### Column Statistics
```sql
SELECT 
    MIN(budget) as min_val,
    MAX(budget) as max_val,
    AVG(budget) as avg_val,
    COUNT(DISTINCT budget) as distinct_count
FROM campaigns.db1.schema.campaigns;
```

## Distribution Analysis

### Value Distribution
```sql
SELECT 
    campaign_length,
    COUNT(*) as count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
FROM campaigns.db1.schema.campaigns
GROUP BY campaign_length
ORDER BY count DESC;
```

### Budget Buckets
```sql
SELECT 
    CASE 
        WHEN budget < 25000 THEN 'Low (<25K)'
        WHEN budget < 50000 THEN 'Medium (25-50K)'
        WHEN budget < 75000 THEN 'High (50-75K)'
        ELSE 'Premium (75K+)'
    END as budget_tier,
    COUNT(*) as count
FROM campaigns.db1.schema.campaigns
GROUP BY budget_tier
ORDER BY count DESC;
```

## Cross-Source Analysis

### Campaign Performance
```sql
SELECT 
    c.campaign_name,
    c.budget,
    SUM(i.clicks) as total_clicks,
    SUM(i.conversions) as total_conversions,
    SUM(i.revenue) as total_revenue,
    SUM(i.revenue) - c.budget as profit,
    (SUM(i.revenue) / c.budget - 1) * 100 as roi_percent
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name, c.budget
ORDER BY roi_percent DESC;
```

### Daily Trends
```sql
SELECT 
    i.days_since_start,
    COUNT(*) as impressions,
    SUM(i.clicks) as clicks,
    SUM(i.revenue) as revenue,
    SUM(i.clicks) * 1.0 / COUNT(*) as click_rate
FROM impressions.db2.schema.impressions i
GROUP BY i.days_since_start
ORDER BY i.days_since_start;
```

## Data Quality Checks

### Null Values
```sql
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN campaign_name IS NULL THEN 1 ELSE 0 END) as null_names,
    SUM(CASE WHEN budget IS NULL THEN 1 ELSE 0 END) as null_budgets
FROM campaigns.db1.schema.campaigns;
```

### Duplicates
```sql
SELECT campaign_name, COUNT(*) as count
FROM campaigns.db1.schema.campaigns
GROUP BY campaign_name
HAVING COUNT(*) > 1;
```

### Orphan Records
```sql
SELECT i.*
FROM impressions.db2.schema.impressions i
LEFT JOIN campaigns.db1.schema.campaigns c 
ON i.campaign_id = c.campaign_id
WHERE c.campaign_id IS NULL;
```

## Top/Bottom Analysis

### Top Performers
```sql
SELECT 
    c.campaign_name,
    SUM(i.revenue) as total_revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name
ORDER BY total_revenue DESC
LIMIT 10;
```

### Underperformers
```sql
SELECT 
    c.campaign_name,
    c.budget,
    COALESCE(SUM(i.revenue), 0) as revenue
FROM campaigns.db1.schema.campaigns c
LEFT JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name, c.budget
HAVING COALESCE(SUM(i.revenue), 0) < c.budget * 0.5
ORDER BY revenue ASC;
```
