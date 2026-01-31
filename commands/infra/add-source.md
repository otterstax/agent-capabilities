# Add Data Source

Add a new data source to OtterStax for federated queries.

## Arguments
- `$ARGUMENTS` - Connection parameters or JSON config

## Instructions

Register a new database as a data source.

### Required Parameters

- **alias**: Unique identifier (used in queries)
- **host**: Database server hostname
- **port**: Database port
- **username**: Database user
- **password**: Database password
- **database**: Default database name

### Add via HTTP API

```bash
curl -X POST "http://0.0.0.0:8085/add_connection" \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "mydata",
    "host": "192.168.1.100",
    "port": "3306",
    "username": "dbuser",
    "password": "dbpass",
    "database": "mydb",
    "table": ""
  }'
```

### Add via Python

```python
import urllib.request
import json

data = {
    "alias": "mydata",
    "host": "192.168.1.100",
    "port": "3306",
    "username": "dbuser",
    "password": "dbpass",
    "database": "mydb",
    "table": ""
}

req = urllib.request.Request(
    "http://0.0.0.0:8085/add_connection",
    data=json.dumps(data).encode(),
    headers={'Content-Type': 'application/json'}
)
response = urllib.request.urlopen(req)
print(f"Status: {response.status}")
```

### Environment-Specific Hosts

| Environment | Host Example |
|-------------|--------------|
| Local | 0.0.0.0, localhost |
| Docker | mariadb1, postgres1 |
| K8s | mariadb.database.svc.cluster.local |

### After Adding

Query the new source:
```sql
SELECT * FROM mydata.mydb.public.users LIMIT 10;
```

### Examples
```
/infra:add-source --alias=customers --host=mysql.local --port=3306 --user=app --password=secret --database=customers_db
/infra:add-source from file connection.json
```
