# Analyze Data

Perform data analysis with statistics, profiling, and insights.

## Arguments
- `$ARGUMENTS` - Table name or analysis description

## Instructions

Generate comprehensive data analysis reports.

### Analysis Types

1. **Table Profiling** - Row counts, column stats, data distribution
2. **Statistical Analysis** - Min, max, avg, percentiles
3. **Data Quality** - Nulls, duplicates, anomalies
4. **Cross-Source Analysis** - Compare data across sources

### Profiling Queries

```python
import pymysql

conn = pymysql.connect(host='0.0.0.0', port=8816, user='testuser', password='testpass')
cursor = conn.cursor()

table = "$ARGUMENTS"  # e.g., campaigns.db1.schema.campaigns

# Row count
cursor.execute(f"SELECT COUNT(*) FROM {table}")
count = cursor.fetchone()[0]

# Numeric column stats
cursor.execute(f"""
    SELECT 
        MIN(budget), MAX(budget), AVG(budget),
        COUNT(DISTINCT budget)
    FROM {table}
""")
stats = cursor.fetchone()

print(f"Rows: {count}")
print(f"Budget: min={stats[0]}, max={stats[1]}, avg={stats[2]:.2f}")

conn.close()
```

### Output Format

```markdown
## Data Analysis Report

### Overview
- Table: campaigns.db1.schema.campaigns
- Total Rows: 243
- Columns: 4

### Column Statistics
| Column   | Min   | Max    | Avg     | Distinct |
|----------|-------|--------|---------|----------|
| budget   | 5000  | 99999  | 52340   | 243      |

### Key Insights
1. Budget distribution: $5K - $100K
2. Campaign length: 30-90 days
```

### Examples
```
/data:analyze campaigns.db1.schema.campaigns
/data:analyze "show ROI by campaign"
/data:analyze --quality-check users
```
