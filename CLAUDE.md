# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OtterStax Skills is an experimental Claude Code extension for Data Analysts, Data Engineers, and DBAs. It provides slash commands for working with OtterStax - a federated SQL query engine supporting cross-database queries across MySQL, MariaDB, and PostgreSQL.

## Installation & Testing

```bash
# Install skills to ~/.claude/
./install.sh

# Uninstall
./install.sh --uninstall

# Test with Docker environment
cd deploy/docker
docker-compose up -d
./add-connections.sh

# Deploy to Kubernetes
kubectl apply -k deploy/k8s/
```

## Architecture

### Command Namespaces

Commands are organized by namespace in `commands/`:

- **`/data:*`** - Data operations (query, schema, analyze, federated)
- **`/infra:*`** - Infrastructure (connect, deploy, status, add-source)  
- **`/dev:*`** - Development utilities (init, test-connection)

Each command is a markdown file with `## Arguments` and `## Instructions` sections that Claude interprets.

### Auto-Activation Skill

`skills/otterstax/SKILL.md` contains frontmatter with `name` and `description` fields. Claude automatically loads this skill when users work with federated queries or OtterStax-related tasks.

### OtterStax Connection

| Protocol | Port | Driver |
|----------|------|--------|
| MySQL | 8816 | pymysql, mysql-connector-python |
| PostgreSQL | 5432 | psycopg2, psql CLI |
| HTTP API | 8085 | curl, requests |

Default credentials: `testuser` / `testpass`

### Table Naming Convention

OtterStax uses fully qualified names: `<alias>.<database>.<schema>.<table>`

Example: `campaigns.db1.schema.campaigns`

### Python Client

`scripts/otterstax_client.py` provides CLI access:
- `connect` - Test connection
- `query <sql>` - Execute SQL
- `schema` - Show schema
- `add-source` - Register data source
- `env list|set|show` - Manage environments
- `protocol show|set` - Switch between mysql/postgres

## Key Patterns

### MySQL Protocol

```python
import pymysql

conn = pymysql.connect(host='0.0.0.0', port=8816, user='testuser', password='testpass')
cursor = conn.cursor()
cursor.execute("SELECT * FROM campaigns.db1.schema.campaigns")
results = cursor.fetchall()
conn.close()
```

### PostgreSQL Protocol

```python
import psycopg2

conn = psycopg2.connect(host='0.0.0.0', port=5432, user='testuser', password='testpass', dbname='postgres')
cursor = conn.cursor()
cursor.execute("SELECT * FROM campaigns.db1.schema.campaigns")
results = cursor.fetchall()
conn.close()
```

### Using psql CLI

```bash
psql -h 0.0.0.0 -p 5432 -U testuser -d postgres -c "SELECT * FROM campaigns.db1.schema.campaigns"
```

### Adding Data Source via HTTP API

```bash
curl -X POST "http://0.0.0.0:8085/add_connection" \
  -H "Content-Type: application/json" \
  -d '{"alias":"mydb","host":"localhost","port":"3306","username":"user","password":"pass","database":"db","table":""}'
```

### Federated JOIN

```sql
SELECT c.campaign_name, SUM(i.revenue) as total
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id;
```
