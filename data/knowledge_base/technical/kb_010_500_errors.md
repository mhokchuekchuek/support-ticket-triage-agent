---
id: kb_010
title: Troubleshooting 500 Errors
category: technical
keywords:
  - 500 error
  - server error
  - internal error
  - error 500
  - crash
  - down
  - not working
---

## What is a 500 Error?

A 500 Internal Server Error indicates something went wrong on our servers. This is not caused by anything you did and is typically temporary.

## Immediate Steps

### 1. Wait and Retry
- Most 500 errors are temporary (under 5 minutes)
- Wait 30 seconds and try your action again
- Refresh the page (Ctrl+R or Cmd+R)

### 2. Check Service Status
- Visit our status page: status.example.com
- Check for ongoing incidents
- Subscribe to updates for real-time notifications

### 3. Clear Browser Cache
If the error persists:
1. Clear your browser cache and cookies
2. Try an incognito/private window
3. Try a different browser

## Common Causes

- **High traffic periods**: Temporary server overload
- **Scheduled maintenance**: Usually announced in advance
- **Infrastructure updates**: Brief disruptions during deployments
- **Third-party service issues**: Dependencies experiencing problems

## When to Contact Support

Contact support if:
- The error persists for more than 15 minutes
- You receive 500 errors consistently on the same action
- The error contains a specific error ID (include this in your report)

## Reporting a 500 Error

When reporting, please include:
1. **Error ID** (if displayed): Example: `ERR-500-abc123`
2. **What you were doing**: The action that triggered the error
3. **Timestamp**: When the error occurred
4. **Browser/Device**: Your browser version and device type
5. **Screenshot**: If possible, capture the error screen

## API Users

If you're using our API and receiving 500 errors:
- Implement exponential backoff retry logic
- Check API status at api.status.example.com
- Review rate limits (429 errors may precede 500s)
- Contact api-support@example.com for persistent issues

## Historical Incidents

Check our status page for:
- Past incidents and resolutions
- Scheduled maintenance windows
- Infrastructure updates
