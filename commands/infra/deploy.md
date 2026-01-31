# Deploy OtterStax

Deploy OtterStax server to Docker or Kubernetes.

## Arguments
- `$ARGUMENTS` - Target: docker | docker-compose | k8s | helm

## Instructions

Deploy OtterStax to container environments.

### Docker Compose

```yaml
version: '3.8'
services:
  otterstax:
    image: otterstax/server:latest
    ports:
      - "8816:8816"
      - "8085:8085"
    depends_on:
      - mariadb1
      - mariadb2

  mariadb1:
    image: mariadb:10.11
    environment:
      MYSQL_DATABASE: db1
      MYSQL_USER: user1
      MYSQL_PASSWORD: password1
    ports:
      - "3101:3306"

  mariadb2:
    image: mariadb:10.11
    environment:
      MYSQL_DATABASE: db2
      MYSQL_USER: user2
      MYSQL_PASSWORD: password2
    ports:
      - "3102:3306"
```

**Deploy:**
```bash
docker-compose up -d
docker-compose ps
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deploy/k8s/

# Or with kustomize
kubectl apply -k deploy/k8s/

# Check status
kubectl get pods -n otterstax
kubectl get svc -n otterstax

# Port forward
kubectl port-forward -n otterstax svc/otterstax-server 8816:8816 8085:8085
```

### Post-Deployment

1. Verify health: `curl http://localhost:8085/health`
2. Add sources: `/infra:add-source`
3. Test connection: `/infra:connect`

### Examples
```
/infra:deploy docker
/infra:deploy docker-compose
/infra:deploy k8s
/infra:deploy k8s --namespace=production
```
