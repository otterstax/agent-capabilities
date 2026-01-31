# Execute SQL Query

Execute SQL queries against OtterStax federated query engine.

## Arguments
- `$ARGUMENTS` - SQL query [--protocol=mysql|postgres]

## Instructions

Execute SQL queries against OtterStax via MySQL or PostgreSQL wire protocol.

### Table Naming Convention
```
<alias>.<database>.<schema>.<table>
```

### Supported Operations

**SELECT queries:**
```sql
SELECT * FROM campaigns.db1.schema.campaigns WHERE budget > 50000;
SELECT campaign_name, budget FROM campaigns.db1.schema.campaigns ORDER BY budget DESC LIMIT 10;
```

**Aggregations:**
```sql
SELECT COUNT(*), SUM(budget) FROM campaigns.db1.schema.campaigns GROUP BY campaign_length;
```

**DML operations:**
```sql
INSERT INTO campaigns.db1.schema.temp (col1) VALUES (1);
UPDATE campaigns.db1.schema.temp SET col1 = 2 WHERE col1 = 1;
DELETE FROM campaigns.db1.schema.temp WHERE col1 > 100;
```

### Execution via MySQL Protocol

```python
import pymysql

conn = pymysql.connect(host='0.0.0.0', port=8816, user='testuser', password='testpass')
cursor = conn.cursor()
cursor.execute("""$ARGUMENTS""")

if cursor.description:
    columns = [d[0] for d in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        print(dict(zip(columns, row)))
else:
    print(f"Affected rows: {cursor.rowcount}")

conn.close()
```

### Execution via PostgreSQL Protocol

```python
import psycopg2

conn = psycopg2.connect(host='0.0.0.0', port=5432, user='testuser', password='testpass', dbname='postgres')
cursor = conn.cursor()
cursor.execute("""$ARGUMENTS""")

if cursor.description:
    columns = [d[0] for d in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        print(dict(zip(columns, row)))
else:
    print(f"Affected rows: {cursor.rowcount}")

conn.close()
```

### Using psql CLI

```bash
psql -h 0.0.0.0 -p 5432 -U testuser -d postgres -c "SELECT * FROM campaigns.db1.schema.campaigns LIMIT 5"
```

### Output
- For SELECT: table with columns and rows
- For DML: affected row count
- Include execution time if available

### Examples
```
/data:query SELECT * FROM campaigns.db1.schema.campaigns LIMIT 5
/data:query SELECT * FROM campaigns.db1.schema.campaigns --protocol=postgres
/data:query show top 10 campaigns by budget
/data:query count all impressions with clicks > 200
```
