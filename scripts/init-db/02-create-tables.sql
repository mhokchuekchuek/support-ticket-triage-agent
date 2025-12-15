-- Create tables for support ticket triage system
-- Run after 01-create-databases.sh

\c support_triage;

-- Tickets table: stores ticket records and triage results
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    urgency VARCHAR(50),
    ticket_type VARCHAR(50),
    triage_result JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMP,

    CONSTRAINT chk_status CHECK (status IN ('open', 'closed', 'pending')),
    CONSTRAINT chk_urgency CHECK (urgency IN ('critical', 'high', 'medium', 'low'))
);

CREATE INDEX IF NOT EXISTS idx_tickets_customer_id ON tickets(customer_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);

-- Customers table: stores customer master data
-- Replaces data/customers.json with SQL-based storage
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

CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_plan ON customers(plan);

-- Chat messages table: stores conversation history
-- No foreign key to tickets table (tickets table removed)
CREATE TABLE IF NOT EXISTS chat_messages (
    ticket_id VARCHAR(255) NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY (ticket_id, created_at),

    CONSTRAINT chk_role CHECK (role IN ('human', 'ai', 'system'))
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_customer_id ON chat_messages(customer_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_ticket_id ON chat_messages(ticket_id);
