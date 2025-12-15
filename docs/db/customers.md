# customers Table

The `customers` table stores customer master data for the support ticket triage system.

## Schema

```sql
CREATE TABLE IF NOT EXISTS customers (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    plan VARCHAR(50) NOT NULL,
    tenure_months INTEGER NOT NULL,
    region VARCHAR(50),
    seats INTEGER DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_plan CHECK (plan IN ('free', 'pro', 'enterprise'))
);
```

## Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | VARCHAR(255) | NO | Primary key, unique customer identifier |
| `name` | VARCHAR(255) | NO | Customer's full name |
| `email` | VARCHAR(255) | NO | Customer's email address |
| `plan` | VARCHAR(50) | NO | Subscription plan (free/pro/enterprise) |
| `tenure_months` | INTEGER | NO | Number of months as a customer |
| `region` | VARCHAR(50) | YES | Geographic region (e.g., US, EU, APAC) |
| `seats` | INTEGER | YES | Number of seats/licenses (default: 1) |
| `notes` | TEXT | YES | Account notes for support context |
| `created_at` | TIMESTAMP | NO | Record creation timestamp |

## Indexes

| Index Name | Column(s) | Purpose |
|------------|-----------|---------|
| `idx_customers_email` | `email` | Fast lookup by email |
| `idx_customers_plan` | `plan` | Filter queries by subscription plan |

## Constraints

- **Primary Key**: `id`
- **Check Constraint**: `plan` must be one of: `free`, `pro`, `enterprise`

## Usage

### Tool: CustomerLookupTool

The `CustomerLookupTool` queries this table to provide customer context to the SupervisorAgent.

**File**: `src/modules/agents/supervisor/tools/customer_lookup.py`

```python
result = self.db_client.fetch_one(
    """
    SELECT id, name, email, plan, tenure_months, region, seats, notes
    FROM customers
    WHERE id = %s
    """,
    (customer_id,)
)
```

### Example Query

```sql
-- Look up customer by ID
SELECT * FROM customers WHERE id = 'cust_123';

-- Find all enterprise customers
SELECT * FROM customers WHERE plan = 'enterprise';

-- Find customers with high tenure
SELECT * FROM customers WHERE tenure_months > 24 ORDER BY tenure_months DESC;
```

## Sample Data

```sql
INSERT INTO customers (id, name, email, plan, tenure_months, region, seats, notes)
VALUES
    ('cust_001', 'John Doe', 'john@example.com', 'pro', 18, 'US', 5, 'VIP customer'),
    ('cust_002', 'Jane Smith', 'jane@example.com', 'enterprise', 36, 'EU', 50, NULL);
```
