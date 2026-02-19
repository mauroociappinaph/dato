# Database Schemas - DATO

> Ver también: [TypeScript Types](types.md)

## 1. Database Schemas

### 1.1 Users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
  plan TEXT NOT NULL DEFAULT 'free' CHECK (plan IN ('free', 'premium', 'professional')),
  plan_started_at TIMESTAMP WITH TIME ZONE,
  plan_ends_at TIMESTAMP WITH TIME ZONE,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  verifications_used_today INT DEFAULT 0,
  last_verification_reset DATE DEFAULT CURRENT_DATE,
  preferences JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_stripe_customer ON users(stripe_customer_id);
CREATE INDEX idx_users_plan ON users(plan);
CREATE INDEX idx_users_role ON users(role);
```

### 1.2 Claims

```sql
CREATE TABLE claims (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_text TEXT NOT NULL,
  normalized_text TEXT, -- Para búsqueda
  speaker TEXT NOT NULL,
  speaker_normalized TEXT, -- Para agrupar
  speaker_party TEXT,
  speaker_role TEXT,
  source_type TEXT NOT NULL CHECK (source_type IN ('speech', 'interview', 'social_media', 'news', 'official')),
  source_url TEXT,
  source_title TEXT,
  context TEXT,
  category TEXT NOT NULL CHECK (category IN ('economy', 'politics', 'social', 'international', 'other')),
  date_said DATE NOT NULL,
  date_extracted TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  extraction_confidence DECIMAL(3,2),
  extraction_agent TEXT DEFAULT 'agent-2',
  status TEXT DEFAULT 'pending' CHECK (status IN ('created', 'pending', 'verifying', 'verified', 'published', 'failed')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_claims_speaker ON claims(speaker_normalized);
CREATE INDEX idx_claims_category ON claims(category);
CREATE INDEX idx_claims_date ON claims(date_said);
CREATE INDEX idx_claims_status ON claims(status);
CREATE INDEX idx_claims_text ON claims USING gin(to_tsvector('spanish', normalized_text));
```

### 1.3 Verifications

```sql
CREATE TABLE verifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
  verdict TEXT NOT NULL CHECK (verdict IN ('VERDADERO', 'FALSO', 'PARCIALMENTE_VERDADERO', 'SIN_DATOS')),
  confidence DECIMAL(3,2) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  explanation TEXT NOT NULL,
  simple_explanation TEXT NOT NULL,
  sources JSONB NOT NULL DEFAULT '[]',
  -- sources format: [{"name": "INDEC", "url": "...", "data": {...}}]
  llm_provider TEXT NOT NULL,
  llm_model TEXT NOT NULL,
  llm_tokens_input INT,
  llm_tokens_output INT,
  llm_latency_ms INT,
  verification_agent TEXT DEFAULT 'agent-3',
  verified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  verified_by TEXT, -- 'auto' o user_id si revisión manual
  published BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMP WITH TIME ZONE,
  published_channels JSONB DEFAULT '[]',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_verifications_claim ON verifications(claim_id);
CREATE INDEX idx_verifications_verdict ON verifications(verdict);
CREATE INDEX idx_verifications_published ON verifications(published);
```

### 1.4 Economic Data

```sql
CREATE TABLE economic_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  indicator TEXT NOT NULL CHECK (indicator IN ('inflation_monthly', 'inflation_yearly', 'poverty', 'employment', 'unemployment', 'dollar_official_buy', 'dollar_official_sell', 'dollar_blue_buy', 'dollar_blue_sell', 'reserves', 'interest_rate', 'gdp', 'trade_balance')),
  value DECIMAL(12,4) NOT NULL,
  previous_value DECIMAL(12,4),
  period DATE NOT NULL, -- YYYY-MM-01 para mensual, YYYY-01-01 para anual
  period_type TEXT NOT NULL CHECK (period_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'yearly')),
  source TEXT NOT NULL CHECK (source IN ('INDEC', 'BCRA', 'BOLETIN_OFICIAL', 'MIN_ECONOMIA', 'WORLD_BANK')),
  source_url TEXT,
  unit TEXT, -- '%', 'USD', 'millones', etc.
  notes TEXT,
  collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  collection_agent TEXT DEFAULT 'agent-1',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_economic_indicator ON economic_data(indicator, period DESC);
CREATE INDEX idx_economic_source ON economic_data(source);
CREATE UNIQUE INDEX idx_economic_unique ON economic_data(indicator, period, source);
```

### 1.5 News Items

```sql
CREATE TABLE news_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  content TEXT,
  source TEXT NOT NULL,
  source_url TEXT UNIQUE,
  category TEXT NOT NULL,
  published_at TIMESTAMP WITH TIME ZONE,
  collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  relevance_score DECIMAL(3,2),
  processed BOOLEAN DEFAULT FALSE,
  claims_extracted INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_news_date ON news_items(published_at DESC);
CREATE INDEX idx_news_category ON news_items(category);
CREATE INDEX idx_news_processed ON news_items(processed);
```

### 1.6 LLM Usage

```sql
CREATE TABLE llm_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider TEXT NOT NULL CHECK (provider IN ('groq', 'nvidia', 'mistral', 'openrouter')),
  model TEXT NOT NULL,
  agent TEXT NOT NULL CHECK (agent IN ('agent-1', 'agent-2', 'agent-3', 'agent-4', 'agent-5', 'agent-6', 'agent-7')),
  operation TEXT NOT NULL,
  tokens_input INT NOT NULL,
  tokens_output INT NOT NULL,
  cost_usd DECIMAL(10,6) NOT NULL,
  latency_ms INT NOT NULL,
  success BOOLEAN NOT NULL,
  error_message TEXT,
  request_id TEXT,
  user_id UUID REFERENCES users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_llm_usage_date ON llm_usage(created_at DESC);
CREATE INDEX idx_llm_usage_agent ON llm_usage(agent);
CREATE INDEX idx_llm_usage_provider ON llm_usage(provider);
```

### 1.7 Subscriptions

```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  stripe_subscription_id TEXT UNIQUE NOT NULL,
  stripe_customer_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('active', 'past_due', 'canceled', 'incomplete', 'trialing')),
  plan TEXT NOT NULL CHECK (plan IN ('premium', 'professional')),
  current_period_start TIMESTAMP WITH TIME ZONE,
  current_period_end TIMESTAMP WITH TIME ZONE,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  canceled_at TIMESTAMP WITH TIME ZONE,
  trial_start TIMESTAMP WITH TIME ZONE,
  trial_end TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

### 1.8 Alerts

```sql
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('speaker', 'topic', 'category', 'indicator')),
  value TEXT NOT NULL,
  channels JSONB NOT NULL DEFAULT '["push"]',
  active BOOLEAN DEFAULT TRUE,
  last_triggered_at TIMESTAMP WITH TIME ZONE,
  trigger_count INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_alerts_user ON alerts(user_id);
CREATE INDEX idx_alerts_type_value ON alerts(type, value);
```

### 1.9 Row Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- Users can only read their own data
CREATE POLICY users_self ON users
  FOR ALL USING (auth.uid() = id);

-- Claims are public read
CREATE POLICY claims_read ON claims
  FOR SELECT USING (true);

-- Verifications are public read
CREATE POLICY verifications_read ON verifications
  FOR SELECT USING (true);

-- Alerts are user-specific
CREATE POLICY alerts_self ON alerts
  FOR ALL USING (auth.uid() = user_id);
```

---

