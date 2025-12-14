---
id: kb_051
title: Enterprise SLA and Uptime Guarantees
category: support
keywords:
  - SLA
  - service level agreement
  - uptime
  - guarantee
  - enterprise
  - reliability
  - availability
---

## Service Level Agreement Overview

Enterprise customers receive contractual uptime guarantees and support commitments.

## Uptime Guarantee

### Standard Enterprise SLA
- **99.9% monthly uptime** guarantee
- Measured per calendar month
- Excludes scheduled maintenance

### Premium Enterprise SLA
- **99.99% monthly uptime** (available upon request)
- Higher commitment, premium pricing
- Contact sales for details

## Uptime Calculation

```
Uptime % = (Total Minutes - Downtime Minutes) / Total Minutes × 100
```

### What Counts as Downtime
- Complete service unavailability
- Core features inaccessible
- API returning 5xx errors consistently

### What Doesn't Count
- Scheduled maintenance (with 72-hour notice)
- Customer's network issues
- Force majeure events
- Degraded performance (non-outage)

## Service Credits

If we miss our uptime target, you receive service credits:

| Monthly Uptime | Service Credit |
|----------------|----------------|
| 99.0% - 99.9% | 10% of monthly fee |
| 95.0% - 99.0% | 25% of monthly fee |
| < 95.0% | 50% of monthly fee |

### Claiming Credits
1. Submit claim within 30 days of incident
2. Email enterprise-support@example.com
3. Include dates and times affected
4. Credit applied to next billing cycle

## Support SLA

### Response Time Commitments

| Severity | First Response | Resolution Target |
|----------|----------------|-------------------|
| Critical (P1) | 15 minutes | 4 hours |
| High (P2) | 1 hour | 24 hours |
| Medium (P3) | 4 hours | 72 hours |
| Low (P4) | 24 hours | Best effort |

### Severity Definitions

**Critical (P1)**
- Complete service outage
- Data loss or corruption
- Security breach
- All users affected

**High (P2)**
- Major feature unavailable
- Significant performance degradation
- Workaround not available
- Many users affected

**Medium (P3)**
- Feature partially impaired
- Workaround available
- Limited user impact

**Low (P4)**
- Minor issues
- Questions and guidance
- Feature requests

## Scheduled Maintenance

### Maintenance Windows
- Standard: Sundays 2:00-6:00 AM PT
- Emergency: As needed with max notice
- Zero-downtime deployments when possible

### Maintenance Notifications
- 72 hours advance notice (standard)
- 24 hours notice (urgent)
- Email to designated contacts
- Status page updates

## Status Page

Real-time system status:
- URL: status.example.com
- Component-level status
- Historical uptime data
- Incident reports

### Subscribing to Updates
- Email notifications
- SMS alerts
- RSS feed
- Slack integration

## Dedicated Support

Enterprise customers receive:
- **Named Account Manager**: Your primary contact
- **Technical Account Manager**: For complex issues
- **24/7 Support Line**: Direct phone access
- **Quarterly Business Reviews**: Performance discussions

## Incident Management

### How We Handle Incidents
1. **Detection**: Automated monitoring + customer reports
2. **Triage**: Severity assessment
3. **Communication**: Status page update, email to affected
4. **Resolution**: Engineering team response
5. **Post-mortem**: Root cause analysis (provided upon request)

### Post-Incident Reports
Available for P1/P2 incidents:
- Timeline of events
- Root cause analysis
- Remediation steps
- Prevention measures

## Custom SLA Terms

Enterprise agreements can include:
- Higher uptime guarantees
- Faster response times
- Custom maintenance windows
- Dedicated infrastructure
- Data residency requirements

Contact your account manager to discuss custom terms.
