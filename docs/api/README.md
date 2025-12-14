# API Documentation

## Overview

FastAPI-based REST API for support ticket triage. Automatic OpenAPI docs available at `/docs` when running.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

```
GET /health
```

**Response:**

```json
{
  "status": "healthy"
}
```

### Triage Ticket

```
POST /api/triage
```

Analyzes a support ticket and returns triage recommendations.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ticket_id | string | Yes | Unique ticket identifier |
| customer_id | string | Yes | Customer identifier |
| customer_info | object | Yes | Customer context |
| messages | array | Yes | Conversation messages |
| metadata | object | No | Additional metadata |

**CustomerInfo Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| plan | string | Yes | Customer plan: free/pro/enterprise |
| tenure_months | integer | Yes | Months as customer |
| region | string | No | Customer region |
| seats | integer | No | Enterprise seat count |
| previous_tickets | integer | No | Previous ticket count (default: 0) |

**Message Object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| role | string | Yes | Sender: 'customer' or 'agent' |
| content | string | Yes | Message text |
| timestamp | string | No | ISO 8601 timestamp |

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/triage \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "ticket_001",
    "customer_id": "customer_001",
    "customer_info": {
      "plan": "enterprise",
      "tenure_months": 24,
      "region": "APAC",
      "seats": 45,
      "previous_tickets": 5
    },
    "messages": [
      {
        "role": "customer",
        "content": "System is down for 2 hours, 45 users affected!",
        "timestamp": "2024-11-15T14:00:00Z"
      }
    ],
    "metadata": {
      "channel": "chat",
      "subject": "System Outage"
    }
  }'
```

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| urgency | string | critical/high/medium/low |
| extracted_info | object | Extracted ticket information |
| recommended_action | string | auto_respond/route_specialist/escalate_human |
| suggested_response | string | Suggested reply text (nullable) |
| relevant_articles | array | KB articles |
| reasoning | string | Explanation for triage decision |

**ExtractedInfo Object:**

| Field | Type | Description |
|-------|------|-------------|
| product_area | string | Affected product area (nullable) |
| issue_type | string | Type of issue |
| sentiment | string | Customer sentiment |
| language | string | Detected language |

**Example Response:**

```json
{
  "urgency": "critical",
  "extracted_info": {
    "product_area": "infrastructure",
    "issue_type": "outage",
    "sentiment": "urgent",
    "language": "en"
  },
  "recommended_action": "escalate_human",
  "suggested_response": null,
  "relevant_articles": [
    {
      "id": "kb_001",
      "title": "System Status Check",
      "relevance_score": 0.85
    }
  ],
  "reasoning": "Enterprise customer with 45 users experiencing system outage requires immediate escalation"
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 400 | Invalid request body |
| 500 | Triage processing failed |

## OpenAPI Schema

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
