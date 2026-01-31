# Basic OtterStax Queries

Common SQL queries for OtterStax.

## Table Naming

Format: `<alias>.<database>.<schema>.<table>`

```sql
-- Full path
SELECT * FROM campaigns.db1.schema.campaigns;
```

## SELECT Queries

### Simple SELECT
```sql
SELECT * FROM campaigns.db1.schema.campaigns;
```

### With WHERE
```sql
SELECT campaign_name, budget 
FROM campaigns.db1.schema.campaigns 
WHERE budget > 50000;
```

### With ORDER BY and LIMIT
```sql
SELECT campaign_name, budget 
FROM campaigns.db1.schema.campaigns 
ORDER BY budget DESC 
LIMIT 10;
```

## Aggregations

### COUNT
```sql
SELECT COUNT(*) as total 
FROM campaigns.db1.schema.campaigns;
```

### GROUP BY
```sql
SELECT campaign_length, COUNT(*) as count, AVG(budget) as avg_budget
FROM campaigns.db1.schema.campaigns
GROUP BY campaign_length
ORDER BY count DESC;
```

### SUM and AVG
```sql
SELECT 
    SUM(budget) as total_budget,
    AVG(budget) as avg_budget,
    MIN(budget) as min_budget,
    MAX(budget) as max_budget
FROM campaigns.db1.schema.campaigns;
```

## DML Operations

### INSERT
```sql
INSERT INTO campaigns.db1.schema.campaigns 
(campaign_id, campaign_name, campaign_length, budget)
VALUES (100, 'New Campaign', 30, 50000.00);
```

### UPDATE
```sql
UPDATE campaigns.db1.schema.campaigns 
SET budget = budget * 1.1 
WHERE campaign_length > 60;
```

### DELETE
```sql
DELETE FROM campaigns.db1.schema.campaigns 
WHERE budget < 10000;
```

## DDL Operations

### CREATE TABLE
```sql
CREATE TABLE campaigns.db1.schema.temp_results (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    value FLOAT
);
```

### CREATE INDEX
```sql
CREATE INDEX idx_budget 
ON campaigns.db1.schema.campaigns (budget);
```

### DROP TABLE
```sql
DROP TABLE campaigns.db1.schema.temp_results;
```
