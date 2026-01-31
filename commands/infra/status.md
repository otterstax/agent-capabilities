# Check OtterStax Status

Check health of OtterStax server and connected data sources.

## Arguments
- `$ARGUMENTS` - Optional: server | sources | all

## Instructions

Comprehensive status check for OtterStax deployment.

### Health Checks

**1. HTTP API:**
```bash
curl -s http://0.0.0.0:8085/health
```

**2. MySQL Protocol:**
```python
import pymysql

try:
    conn = pymysql.connect(host='0.0.0.0', port=8816, user='testuser', password='testpass')
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    print(f"Version: {cursor.fetchone()[0]}")
    conn.close()
except Exception as e:
    print(f"Failed: {e}")
```

**3. Data Sources:**
```python
conn = pymysql.connect(host='0.0.0.0', port=8816, user='testuser', password='testpass')
cursor = conn.cursor()
cursor.execute("SHOW DATABASES")
for db in cursor.fetchall():
    print(f"  - {db[0]}")
conn.close()
```

### Environment-Specific

**Docker:**
```bash
docker ps --filter name=otterstax
docker logs --tail 20 otterstax
```

**Kubernetes:**
```bash
kubectl get pods -n otterstax -l app=otterstax-server
kubectl logs -n otterstax -l app=otterstax-server --tail=20
```

### Output Format

```markdown
## OtterStax Status

### Server
- HTTP API: OK (8085)
- MySQL Protocol: OK (8816)
- Version: 9.5.0

### Data Sources (3)
| Alias       | Database | Status |
|-------------|----------|--------|
| campaigns   | db1      | OK     |
| impressions | db2      | OK     |
```

### Examples
```
/infra:status
/infra:status server
/infra:status sources
```
