---
id: kb_022
title: Available Integrations
category: features
keywords:
  - integration
  - Slack
  - Zapier
  - API
  - webhook
  - connect
  - third-party
  - apps
---

## Native Integrations

### Communication

| Integration | Features | Plans |
|-------------|----------|-------|
| **Slack** | Notifications, commands, unfurling | All plans |
| **Microsoft Teams** | Notifications, tabs | Pro, Enterprise |
| **Discord** | Webhooks, bot notifications | All plans |

### Productivity

| Integration | Features | Plans |
|-------------|----------|-------|
| **Google Workspace** | SSO, Drive, Calendar | Pro, Enterprise |
| **Microsoft 365** | SSO, OneDrive, Outlook | Pro, Enterprise |
| **Notion** | Two-way sync | Pro, Enterprise |

### Development

| Integration | Features | Plans |
|-------------|----------|-------|
| **GitHub** | Issue sync, PR links | All plans |
| **GitLab** | Issue sync, MR links | All plans |
| **Jira** | Two-way issue sync | Pro, Enterprise |

## Setting Up Integrations

### General Steps

1. Go to **Settings > Integrations**
2. Find the integration you want
3. Click **Connect**
4. Authorize access (redirects to provider)
5. Configure options
6. Save settings

### Slack Setup

1. Click **Add to Slack** button
2. Select your Slack workspace
3. Choose channels for notifications
4. Configure notification preferences:
   - New items
   - Comments
   - Status changes
   - Mentions

### Zapier Integration

Connect to 5,000+ apps via Zapier:
1. Go to zapier.com and create account
2. Search for our app in Zapier
3. Create a "Zap" with triggers/actions:
   - **Triggers**: New item, updated item, new comment
   - **Actions**: Create item, update item, add comment

## Webhooks

For custom integrations:

### Outgoing Webhooks
Send data to your systems when events occur:
1. Go to **Settings > Integrations > Webhooks**
2. Click **Add Webhook**
3. Enter your endpoint URL
4. Select events to trigger webhook
5. Save and test

### Incoming Webhooks
Receive data from external systems:
1. Generate webhook URL in Settings
2. POST JSON data to the URL
3. Data creates/updates items automatically

## API Access

Build custom integrations:
- REST API with full CRUD operations
- OAuth 2.0 authentication
- Rate limits: 100 req/min (Free), 1000 req/min (Pro)
- API documentation: docs.example.com/api

### API Key Management
1. Go to **Settings > API**
2. Click **Generate New Key**
3. Name your key for reference
4. Copy and store securely (shown once)

## Enterprise Integrations

Additional integrations for Enterprise:
- SAML/SCIM for identity management
- Custom SSO providers
- Data warehouse exports (Snowflake, BigQuery)
- Audit log streaming
- Custom webhook transformations

## Troubleshooting

### Integration Not Working

1. Check if integration is still connected
2. Re-authorize if tokens expired
3. Verify webhook URLs are accessible
4. Check our status page for outages

### Sync Delays

- Most integrations sync within 5 minutes
- Large syncs may take up to 30 minutes
- Check integration logs in Settings
