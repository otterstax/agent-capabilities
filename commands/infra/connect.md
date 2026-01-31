# Connect to OtterStax

Connect to OtterStax server and verify connectivity.

## Arguments
- `$ARGUMENTS` - Environment and protocol: [local|docker|k8s] [--protocol=mysql|postgres]

## Instructions

Establish connection to OtterStax server via MySQL or PostgreSQL wire protocol.

### Protocols

| Protocol | Port | Driver | Use Case |
|----------|------|--------|----------|
| MySQL | 8816 | pymysql | Default, compatible with MySQL clients |
| PostgreSQL | 5432 | psycopg2 | For PostgreSQL-native tools (psql, pgcli) |

### Environments

| Environment | Host | MySQL Port | PostgreSQL Port | HTTP Port |
|-------------|------|------------|-----------------|-----------|
| local | 0.0.0.0 | 8816 | 5432 | 8085 |
| docker | localhost | 8816 | 5432 | 8085 |
| k8s | via port-forward | 8816 | 5432 | 8085 |

### Connection Steps

**1. Check HTTP API:**
```bash
curl -s http://0.0.0.0:8085/health
```

**2. Test MySQL Protocol:**
```python
import pymysql

try:
    conn = pymysql.connect(
        host='0.0.0.0', 
        port=8816, 
        user='testuser', 
        password='testpass'
    )
    print("MySQL connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

**3. Test PostgreSQL Protocol:**
```python
import psycopg2

try:
    conn = psycopg2.connect(
        host='0.0.0.0',
        port=5432,
        user='testuser',
        password='testpass',
        dbname='postgres'
    )
    print("PostgreSQL connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

**4. Using psql CLI:**
```bash
psql -h 0.0.0.0 -p 5432 -U testuser -d postgres
```

**5. For Docker:**
```bash
docker ps --filter name=otterstax
# If not running:
docker-compose up -d
```

**6. For Kubernetes:**
```bash
kubectl get pods -n otterstax
kubectl port-forward -n otterstax svc/otterstax-server 8816:8816 5432:5432 8085:8085 &
```

### Output

Report:
- Environment type
- Protocol used (MySQL/PostgreSQL)
- Host and ports
- Connection status
- Server version
- Available data sources

### Examples
```
/infra:connect
/infra:connect local
/infra:connect local --protocol=postgres
/infra:connect docker --protocol=mysql
/infra:connect k8s --protocol=postgres
```
