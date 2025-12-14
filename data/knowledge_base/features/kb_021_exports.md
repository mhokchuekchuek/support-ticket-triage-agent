---
id: kb_021
title: Exporting Your Data
category: features
keywords:
  - export
  - download
  - backup
  - CSV
  - JSON
  - PDF
  - data export
  - bulk export
---

## Export Options

### Available Formats

| Format | Best For | Plans |
|--------|----------|-------|
| CSV | Spreadsheets, analysis | All plans |
| JSON | Developers, integrations | Pro, Enterprise |
| PDF | Reports, sharing | All plans |
| XLSX | Excel users | Pro, Enterprise |

### Single Item Export

1. Open the item you want to export
2. Click **More** (⋯) menu
3. Select **Export**
4. Choose format
5. Download begins automatically

### Bulk Export

For multiple items:
1. Go to the main list view
2. Select items using checkboxes
3. Click **Export Selected** in toolbar
4. Choose format and options
5. Receive download link via email (large exports)

## Full Account Export

Export all your data for backup or migration:

1. Go to **Settings > Account > Data Export**
2. Click **Request Full Export**
3. Choose what to include:
   - Projects and workspaces
   - Files and attachments
   - Comments and history
   - User data and settings
4. Receive download link via email (within 24 hours)

**Note**: Full exports are available once per 30 days.

## API Export

For developers:
- Use our REST API for programmatic exports
- Pagination supported for large datasets
- Rate limits apply (see API docs)
- Webhook notifications for async exports

```
GET /api/v1/export?format=json&include=all
```

## Export Limits

| Plan | Single Export | Bulk Export | Full Export |
|------|---------------|-------------|-------------|
| Free | 100 items | 500 items | 1 GB |
| Pro | 1,000 items | 10,000 items | 10 GB |
| Enterprise | Unlimited | Unlimited | Unlimited |

## Scheduled Exports

Enterprise plan feature:
- Set up recurring exports (daily, weekly, monthly)
- Automatic delivery to email or cloud storage
- Configure in Settings > Integrations > Scheduled Exports

## Data Portability

Your data belongs to you:
- Export anytime without restrictions
- Standard formats ensure compatibility
- No lock-in to our platform
- GDPR-compliant data access

## Troubleshooting

### Export Taking Too Long

- Large exports are processed in background
- Check email for download link
- Links expire after 7 days

### Missing Data in Export

- Check date range filters
- Verify you have access to all items
- Archived items must be explicitly included
