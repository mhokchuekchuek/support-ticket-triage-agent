# Health Endpoint

Health check endpoint to verify API availability.

## Location

`src/api/routes/health.py`

## Endpoint

```
GET /health
```

## Request

No request body required.

### Example Request

```bash
curl http://localhost:8000/health
```

## Response

### Response Body

| Field | Type | Description |
|-------|------|-------------|
| status | string | Health status ("healthy") |

### Example Response

```json
{
  "status": "healthy"
}
```

## Use Cases

- **Load balancer health checks**: Verify service is running
- **Kubernetes liveness probe**: Container health monitoring
- **Monitoring systems**: Service availability checks

## See Also

- [Triage Endpoint](triage.md)
- [Answer Endpoint](answer.md)
