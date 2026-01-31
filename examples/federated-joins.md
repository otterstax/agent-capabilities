# Federated JOIN Examples

Cross-database queries combining data from multiple sources.

## Basic Federated JOIN

```sql
SELECT 
    c.campaign_name,
    i.clicks,
    i.revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id;
```

## JOIN with Aggregation

```sql
SELECT 
    c.campaign_name,
    COUNT(i.impression_id) as total_impressions,
    SUM(i.clicks) as total_clicks,
    SUM(i.revenue) as total_revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name
ORDER BY total_revenue DESC;
```

## JOIN with Filters

```sql
SELECT 
    c.campaign_name,
    c.budget,
    i.clicks,
    i.revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
WHERE c.budget > 50000 
  AND i.clicks > 100
ORDER BY i.revenue DESC
LIMIT 20;
```

## Multi-Condition JOIN

```sql
SELECT *
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id 
   AND c.campaign_length > 30 
   AND i.clicks > 200;
```

## Calculated Fields

```sql
SELECT 
    c.campaign_name,
    c.budget,
    SUM(i.revenue) as total_revenue,
    SUM(i.revenue) / c.budget * 100 as roi_percent
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name, c.budget
HAVING SUM(i.revenue) > 100
ORDER BY roi_percent DESC;
```

## LEFT JOIN (if supported)

```sql
SELECT 
    c.campaign_name,
    COALESCE(SUM(i.clicks), 0) as total_clicks
FROM campaigns.db1.schema.campaigns c
LEFT JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name;
```

## Performance Tips

1. **Filter early**: Add WHERE clauses to reduce data
2. **Use LIMIT**: When exploring, limit results
3. **Index JOIN columns**: Ensure campaign_id is indexed
4. **Select specific columns**: Avoid `SELECT *` for large tables
