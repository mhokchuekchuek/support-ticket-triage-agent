---
id: kb_032
title: Plan Limits and Quotas
category: plans
keywords:
  - limits
  - quota
  - storage
  - users
  - API calls
  - rate limit
  - restrictions
---

## Storage Limits

| Plan | Storage Quota | File Size Limit |
|------|---------------|-----------------|
| Free | 1 GB total | 25 MB per file |
| Pro | 50 GB per workspace | 100 MB per file |
| Enterprise | Unlimited | 500 MB per file |

### Storage Calculation
- Total size of all uploaded files
- Includes attachments, images, documents
- Previous versions count toward quota
- Deleted files freed after 30-day trash period

### Approaching Storage Limit
When at 80% capacity:
- Warning notification displayed
- Email alert sent to admins
- Uploads still allowed until 100%

### At Storage Limit
- New uploads blocked
- Existing files accessible
- Options: Delete files or upgrade plan

## User Limits

| Plan | User Limit | Guest Users |
|------|------------|-------------|
| Free | 5 users | Not available |
| Pro | Unlimited | 10 per workspace |
| Enterprise | Unlimited | Unlimited |

### User Types
- **Members**: Full access, count toward limit
- **Guests**: Limited access, separate limit
- **Viewers**: Read-only, count as members

## Project Limits

| Plan | Active Projects | Archived Projects |
|------|-----------------|-------------------|
| Free | 3 | Unlimited |
| Pro | Unlimited | Unlimited |
| Enterprise | Unlimited | Unlimited |

**Note**: Archive projects to free up slots on Free plan.

## API Rate Limits

| Plan | Requests/Minute | Requests/Day |
|------|-----------------|--------------|
| Free | No API access | - |
| Pro | 100 | 10,000 |
| Enterprise | 1,000 | 100,000 |

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

### Exceeding Rate Limits
- HTTP 429 response returned
- Retry after `X-RateLimit-Reset` timestamp
- Implement exponential backoff
- Contact support for limit increases

## Feature Limits

### Integrations

| Plan | Native Integrations | Custom Webhooks |
|------|---------------------|-----------------|
| Free | 3 | 1 |
| Pro | Unlimited | 10 |
| Enterprise | Unlimited | Unlimited |

### Automation

| Plan | Automated Rules | Scheduled Actions |
|------|-----------------|-------------------|
| Free | 3 | Not available |
| Pro | 50 | 20 |
| Enterprise | Unlimited | Unlimited |

### History Retention

| Plan | Activity History | Audit Logs |
|------|------------------|------------|
| Free | 7 days | Not available |
| Pro | 1 year | 90 days |
| Enterprise | Unlimited | Unlimited |

## Export Limits

| Plan | Single Export | Bulk Export |
|------|---------------|-------------|
| Free | 100 items | 500 items |
| Pro | 1,000 items | 10,000 items |
| Enterprise | Unlimited | Unlimited |

## Checking Your Usage

### Current Usage Dashboard
1. Go to **Settings > Usage**
2. View real-time metrics:
   - Storage used/remaining
   - User count
   - API calls this period
   - Project count

### Usage Alerts
Configure alerts in Settings > Notifications:
- Storage at 80%, 90%, 100%
- API usage thresholds
- User limit approaching

## Increasing Limits

### Upgrade Plan
Most straightforward option—higher plans have higher limits.

### Enterprise Custom Limits
Enterprise customers can negotiate custom limits:
- Higher API rate limits
- Increased file size limits
- Custom storage quotas
- Contact your account manager

### Temporary Increases
For special circumstances (data migration, events):
- Contact support in advance
- Temporary limit increases available
- Must be scheduled ahead of time
