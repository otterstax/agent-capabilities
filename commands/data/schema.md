# Explore Database Schema

Explore database schema, tables, and column definitions in OtterStax.

## Arguments
- `$ARGUMENTS` - Optional: database name, table name, or "all"

## Instructions

Explore the structure of connected data sources.

### Schema Hierarchy
```
Data Source (alias) → Database → Schema → Table → Columns
```

### Commands

**List all databases:**
```sql
SHOW DATABASES;
```

**List tables:**
```sql
SHOW TABLES FROM <alias>.<database>.<schema>;
```

**Describe table:**
```sql
DESCRIBE <alias>.<database>.<schema>.<table>;
```

### Execution

```python
import pymysql

conn = pymysql.connect(host='0.0.0.0', port=8816, user='testuser', password='testpass')
cursor = conn.cursor()

# Based on $ARGUMENTS:
# - No args: SHOW DATABASES
# - Database: SHOW TABLES FROM <db>
# - Table: DESCRIBE <table>

cursor.execute("SHOW DATABASES")
for db in cursor.fetchall():
    print(f"- {db[0]}")

conn.close()
```

### Output Format

**For tables:**
```
Table: campaigns.db1.schema.campaigns

| Column          | Type         | Nullable | Key     |
|-----------------|--------------|----------|---------|
| campaign_id     | INT          | NO       | PRIMARY |
| campaign_name   | VARCHAR(255) | NO       |         |
```

### Examples
```
/data:schema
/data:schema campaigns
/data:schema campaigns.db1.schema.campaigns
```
