# Test Database Connection

Test connectivity to a database before adding it as a data source.

## Arguments
- `$ARGUMENTS` - Connection parameters: host port user password database

## Instructions

Verify database connectivity before configuring OtterStax.

### Test Connection

```python
import pymysql

# Parse arguments: host port user password database
params = "$ARGUMENTS".split()

try:
    conn = pymysql.connect(
        host=params[0],
        port=int(params[1]),
        user=params[2],
        password=params[3],
        database=params[4] if len(params) > 4 else None
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    
    print(f"✓ Connection successful!")
    print(f"  Server version: {version}")
    
    # List databases
    cursor.execute("SHOW DATABASES")
    print(f"  Available databases:")
    for db in cursor.fetchall():
        print(f"    - {db[0]}")
    
    conn.close()

except Exception as e:
    print(f"✗ Connection failed: {e}")
```

### Common Issues

| Error | Solution |
|-------|----------|
| Connection refused | Check host/port, firewall |
| Access denied | Verify credentials |
| Unknown database | Check database name |
| Timeout | Network connectivity issue |

### Examples
```
/dev:test-connection localhost 3306 root password mydb
/dev:test-connection mariadb1 3306 user1 password1
/dev:test-connection 192.168.1.100 5432 postgres secret
```
