# OtterStax Agent Capabilities

<p align="center">
  <img src="docs/assets/logo.png" alt="OtterStax" width="200"/>
</p>

<p align="center">
  <strong>A public registry of skills and MCP specifications for OtterStax</strong><br>
  <em>Designed for AI agents and runtimes</em>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#commands">Commands</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#examples">Examples</a> •
  <a href="#contributing">Contributing</a>
</p>

---

> **EXPERIMENTAL PROJECT**
> 
> This is an experimental project designed for **Data Analysts**, **Data Engineers**, and **Database Administrators (DBAs)** who want to leverage Claude Code for working with federated SQL queries. The project is under active development - APIs and commands may change.
>
> **Target Audience:**
> - **Data Analysts** - ad-hoc queries across multiple data sources
> - **Data Engineers** - building data pipelines, ETL workflows, data integration  
> - **DBAs** - managing distributed database infrastructure
> - Anyone who needs to query across MySQL/MariaDB/PostgreSQL databases

---

## What is OtterStax?

OtterStax is a federated SQL query engine that allows you to:
- Query multiple databases with a single SQL statement
- JOIN data across MySQL, MariaDB, and PostgreSQL sources
- Use MySQL/PostgreSQL wire protocols for connectivity
- Deploy locally, in Docker, or on Kubernetes

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/otterstax/agent-capabilities.git

# Run the installer
cd agent-capabilities
./install.sh
```

### Manual Install

Copy commands to your Claude Code configuration:

```bash
# Copy all commands
cp -r commands/* ~/.claude/commands/

# Copy skills (for auto-activation)
cp -r skills/* ~/.claude/skills/

# Copy examples (optional)
cp -r examples/* ~/.claude/examples/
```

## Commands

### Data Commands (`/data:*`)

| Command | Description |
|---------|-------------|
| `/data:query` | Execute SQL queries against OtterStax |
| `/data:schema` | Explore database schema and table structures |
| `/data:analyze` | Analyze data with statistics and insights |
| `/data:federated` | Cross-database federated queries |

### Infrastructure Commands (`/infra:*`)

| Command | Description |
|---------|-------------|
| `/infra:connect` | Connect to OtterStax (local/Docker/K8s) |
| `/infra:deploy` | Deploy OtterStax to Docker or Kubernetes |
| `/infra:status` | Check server and data source status |
| `/infra:add-source` | Add new data source connection |

### Development Commands (`/dev:*`)

| Command | Description |
|---------|-------------|
| `/dev:init` | Initialize OtterStax project structure |
| `/dev:test-connection` | Test database connectivity |

## Quick Start

### 1. Connect to OtterStax

```
/infra:connect local
```

### 2. Explore Schema

```
/data:schema campaigns
```

### 3. Run a Query

```
/data:query SELECT * FROM campaigns.db1.schema.campaigns LIMIT 5
```

### 4. Federated Query

```
/data:federated join campaigns with impressions on campaign_id
```

## Project Structure

```
otterstax-skills/
├── commands/
│   ├── data/           # Data operations
│   │   ├── query.md
│   │   ├── schema.md
│   │   ├── analyze.md
│   │   └── federated.md
│   ├── infra/          # Infrastructure operations
│   │   ├── connect.md
│   │   ├── deploy.md
│   │   ├── status.md
│   │   └── add-source.md
│   └── dev/            # Development utilities
│       ├── init.md
│       └── test-connection.md
├── skills/
│   └── otterstax/
│       └── SKILL.md    # Auto-activation skill
├── examples/
│   ├── basic-queries.md
│   ├── federated-joins.md
│   └── data-analysis.md
├── deploy/
│   ├── docker/
│   │   └── docker-compose.yml
│   └── k8s/
│       └── *.yaml
├── scripts/
│   └── otterstax_client.py
├── docs/
│   ├── getting-started.md
│   ├── query-syntax.md
│   └── deployment.md
├── install.sh
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Examples

### Simple Query

```sql
SELECT campaign_name, budget 
FROM campaigns.db1.schema.campaigns 
WHERE budget > 50000
ORDER BY budget DESC;
```

### Federated JOIN

```sql
SELECT 
    c.campaign_name,
    SUM(i.clicks) as total_clicks,
    SUM(i.revenue) as total_revenue
FROM campaigns.db1.schema.campaigns c
JOIN impressions.db2.schema.impressions i 
ON c.campaign_id = i.campaign_id
GROUP BY c.campaign_id, c.campaign_name
ORDER BY total_revenue DESC;
```

## Environments

| Environment | MySQL Port | PostgreSQL Port | HTTP Port | Notes |
|-------------|------------|-----------------|-----------|-------|
| Local | 8816 | 5432 | 8085 | Direct connection |
| Docker | 8816 | 5432 | 8085 | Container name: `otterstax` |
| Kubernetes | 8816 | 5432 | 8085 | Namespace: `otterstax` |

## Configuration

Config file: `~/.otterstax/config.json`

```json
{
  "environments": {
    "local": {
      "host": "0.0.0.0",
      "mysql_port": 8816,
      "postgres_port": 5432,
      "http_port": 8085
    }
  },
  "current_environment": "local",
  "protocol": "mysql"
}
```

## Requirements

- Claude Code CLI
- Python 3.8+ (for client scripts)
- `pymysql` or `mysql-connector-python`
- Docker (for container deployment)
- kubectl (for Kubernetes deployment)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [OtterStax Documentation](https://otterstax.io/docs)
- [GitHub Repository](https://github.com/otterstax/agent-capabilities)
- [Issue Tracker](https://github.com/otterstax/agent-capabilities/issues)

---

<p align="center">
  Made with ❤️ by the OtterStax Team
</p>
