# Federated Query

Execute cross-database federated queries joining multiple data sources.

## Arguments
- `$ARGUMENTS` - Query description or SQL with multiple sources

## Instructions

OtterStax's core capability: query multiple databases as one.

### Federated Query Concept

```sql
-- Data from MariaDB instance 1 (campaigns)
-- JOINed with MariaDB instance 2 (impressions)
SELECT c.campaign_name, i.clicks, i.revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id;
```

### Common Patterns

**Simple JOIN:**
```sql
SELECT a.*, b.*
FROM source1.db1.schema.table1 a
JOIN source2.db2.schema.table2 b ON a.id = b.foreign_id;
```

**Aggregated JOIN:**
```sql
SELECT 
    c.campaign_name,
    COUNT(i.impression_id) as impressions,
    SUM(i.revenue) as total_revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name
ORDER BY total_revenue DESC;
```

**Multi-condition JOIN:**
```sql
SELECT *
FROM campaigns.db1.schema.campaigns
JOIN impressions.db2.schema.impressions 
ON campaigns.campaign_id = impressions.campaign_id 
   AND campaign_length > 30 
   AND clicks > 200;
```

### Execution

```python
import pymysql

conn = pymysql.connect(host='0.0.0.0', port=8816, user='testuser', password='testpass')
cursor = conn.cursor()

# Convert natural language to SQL if needed
# Execute federated query
cursor.execute("""
    SELECT c.campaign_name, SUM(i.revenue) as revenue
    FROM campaigns.db1.schema.campaigns c
    JOIN impressions.db2.schema.impressions i 
    ON c.campaign_id = i.campaign_id
    GROUP BY c.campaign_id
    ORDER BY revenue DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

conn.close()
```

### Natural Language Examples
- "join campaigns with impressions" → JOIN on campaign_id
- "compare sales across regions" → UNION or regional JOINs
- "match products with inventory" → JOIN products + inventory

### Examples
```
/data:federated join campaigns with impressions on campaign_id
/data:federated SELECT c.*, i.clicks FROM campaigns c JOIN impressions i ON c.campaign_id = i.campaign_id
/data:federated "top 10 campaigns by total revenue across all impressions"
```
