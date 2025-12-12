-- Email System Database Schema
-- PostgreSQL Database for MVP 1

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    unsubscribed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(500) NOT NULL,
    sender VARCHAR(255) NOT NULL,
    html TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaign sends table (track individual email sends)
CREATE TABLE IF NOT EXISTS campaign_sends (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    contact_email VARCHAR(255) REFERENCES contacts(email) ON DELETE CASCADE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered BOOLEAN DEFAULT FALSE,
    bounce_type VARCHAR(50), -- 'hard', 'soft', null
    complaint BOOLEAN DEFAULT FALSE,
    UNIQUE(campaign_id, contact_email)
);

-- Events table for tracking opens, clicks, etc.
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    contact_email VARCHAR(255) REFERENCES contacts(email) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- 'open', 'click', 'bounce', 'complaint'
    metadata JSONB, -- For storing click URLs, bounce reasons, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suppressions table for bounces and complaints
CREATE TABLE IF NOT EXISTS suppressions (
    email VARCHAR(255) PRIMARY KEY,
    reason VARCHAR(50) NOT NULL, -- 'bounce', 'complaint'
    bounce_type VARCHAR(50), -- 'hard', 'soft', null (for bounces)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Unsubscribe tokens table
CREATE TABLE IF NOT EXISTS unsubscribe_tokens (
    token VARCHAR(255) PRIMARY KEY,
    contact_email VARCHAR(255) REFERENCES contacts(email) ON DELETE CASCADE,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_campaign_sends_campaign_id ON campaign_sends(campaign_id);
CREATE INDEX IF NOT EXISTS idx_campaign_sends_contact_email ON campaign_sends(contact_email);
CREATE INDEX IF NOT EXISTS idx_events_campaign_id ON events(campaign_id);
CREATE INDEX IF NOT EXISTS idx_events_contact_email ON events(contact_email);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at);
CREATE INDEX IF NOT EXISTS idx_contacts_unsubscribed ON contacts(unsubscribed);
