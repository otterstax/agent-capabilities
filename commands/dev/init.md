# Initialize OtterStax Project

Initialize a new OtterStax project with recommended structure.

## Arguments
- `$ARGUMENTS` - Optional: project name or directory

## Instructions

Set up a new project configured for OtterStax.

### Project Structure

```
my-project/
├── .otterstax/
│   └── config.json         # Local configuration
├── data-sources/
│   ├── source1.json        # Data source configs
│   └── source2.json
├── queries/
│   ├── reports/            # Report queries
│   └── migrations/         # Schema migrations
├── docker-compose.yml      # Local development
└── README.md
```

### Initialization Steps

**1. Create directories:**
```bash
mkdir -p .otterstax data-sources queries/reports queries/migrations
```

**2. Create config:**
```bash
cat > .otterstax/config.json << 'EOF'
{
  "environment": "local",
  "host": "0.0.0.0",
  "mysql_port": 8816,
  "http_port": 8085
}
EOF
```

**3. Create docker-compose.yml:**
```yaml
version: '3.8'
services:
  otterstax:
    image: otterstax/server:latest
    ports:
      - "8816:8816"
      - "8085:8085"
```

**4. Create sample data source:**
```bash
cat > data-sources/example.json << 'EOF'
{
  "alias": "example",
  "host": "localhost",
  "port": "3306",
  "username": "user",
  "password": "password",
  "database": "mydb"
}
EOF
```

### Examples
```
/dev:init
/dev:init my-analytics-project
/dev:init --with-samples
```
