---
name: otterstax
description: OtterStax federated SQL query engine - automatically activates when working with cross-database queries, data federation, or OtterStax deployments
---

# OtterStax Skill

You are an expert in OtterStax, a federated SQL query engine that enables querying multiple databases with a single SQL statement.

## When to Activate

Activate this skill when the user:
- Mentions OtterStax, federated queries, or cross-database joins
- Wants to query multiple databases simultaneously
- Needs to deploy or manage OtterStax infrastructure
- Works with data sources across MySQL, MariaDB, or PostgreSQL

## Core Capabilities

### Table Naming Convention
```
<alias>.<database>.<schema>.<table>
```

Example: `campaigns.db1.schema.campaigns`

### Connection Details

| Protocol | Port | Driver |
|----------|------|--------|
| MySQL | 8816 | pymysql, mysql-connector-python |
| PostgreSQL | 5432 | psycopg2, psql CLI |
| HTTP API | 8085 | curl, requests |

Default credentials: `testuser` / `testpass`

### Federated Query Example
```sql
SELECT c.campaign_name, SUM(i.revenue) as total_revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id
ORDER BY total_revenue DESC;
```

## Available Commands

| Command | Purpose |
|---------|---------|
| `/data:query` | Execute SQL queries |
| `/data:schema` | Explore database schema |
| `/data:analyze` | Data analysis and profiling |
| `/data:federated` | Cross-database queries |
| `/infra:connect` | Connect to OtterStax |
| `/infra:deploy` | Deploy to Docker/K8s |
| `/infra:status` | Check health status |
| `/infra:add-source` | Add data source |

## Python Client - MySQL Protocol

```python
import pymysql

conn = pymysql.connect(
    host='0.0.0.0',
    port=8816,
    user='testuser',
    password='testpass'
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM campaigns.db1.schema.campaigns")
results = cursor.fetchall()
conn.close()
```

## Python Client - PostgreSQL Protocol

```python
import psycopg2

conn = psycopg2.connect(
    host='0.0.0.0',
    port=5432,
    user='testuser',
    password='testpass',
    dbname='postgres'
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM campaigns.db1.schema.campaigns")
results = cursor.fetchall()
conn.close()
```

## Using psql CLI

```bash
psql -h 0.0.0.0 -p 5432 -U testuser -d postgres
```

## Environment Support

- **Local**: Direct connection to 0.0.0.0
- **Docker**: Container name `otterstax`
- **Kubernetes**: Namespace `otterstax`, service `otterstax-server`

## Key Features

1. **Federated JOINs** - Query across multiple database instances
2. **MySQL/PostgreSQL Protocol** - Standard client compatibility (pymysql, psycopg2, psql)
3. **Custom Functions** - User-defined filter functions
4. **HTTP Management API** - Add/remove data sources dynamically
