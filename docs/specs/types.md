# TypeScript Types - DATO

> Ver también: [Database Schemas](database.md)

## 2. TypeScript Types

### 2.1 Core Types

```typescript
// packages/types/src/index.ts

// ============================================================================
// USER TYPES
// ============================================================================

export type Plan = 'free' | 'premium' | 'professional';

export type UserRole = 'user' | 'admin';

export interface User {
  id: string;
  email: string;
  fullName: string | null;
  avatarUrl: string | null;
  role: UserRole;
  plan: Plan;
  planStartedAt: Date | null;
  planEndsAt: Date | null;
  stripeCustomerId: string | null;
  stripeSubscriptionId: string | null;
  verificationsUsedToday: number;
  lastVerificationReset: Date;
  preferences: UserPreferences;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserPreferences {
  notificationTime: string; // "09:00"
  notificationChannels: NotificationChannel[];
  language: 'es-AR';
  theme: 'light' | 'dark' | 'system';
}

export type NotificationChannel = 'push' | 'email' | 'telegram';

// ============================================================================
// CLAIM TYPES
// ============================================================================

export type ClaimCategory = 'economy' | 'politics' | 'social' | 'international' | 'other';
export type ClaimSourceType = 'speech' | 'interview' | 'social_media' | 'news' | 'official';
export type ClaimStatus = 'created' | 'pending' | 'verifying' | 'verified' | 'published' | 'failed';

export interface Claim {
  id: string;
  claimText: string;
  normalizedText: string;
  speaker: string;
  speakerNormalized: string;
  speakerParty: string | null;
  speakerRole: string | null;
  sourceType: ClaimSourceType;
  sourceUrl: string | null;
  sourceTitle: string | null;
  context: string | null;
  category: ClaimCategory;
  dateSaid: Date;
  dateExtracted: Date;
  extractionConfidence: number;
  extractionAgent: string;
  status: ClaimStatus;
  verification: Verification | null;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateClaimInput {
  claimText: string;
  speaker: string;
  speakerParty?: string;
  speakerRole?: string;
  sourceType: ClaimSourceType;
  sourceUrl?: string;
  sourceTitle?: string;
  context?: string;
  category: ClaimCategory;
  dateSaid: Date;
}

// ============================================================================
// VERIFICATION TYPES
// ============================================================================

export type Verdict = 'VERDADERO' | 'FALSO' | 'PARCIALMENTE_VERDADERO' | 'SIN_DATOS';

export interface Verification {
  id: string;
  claimId: string;
  claim: Claim;
  verdict: Verdict;
  confidence: number;
  explanation: string;
  simpleExplanation: string;
  sources: VerificationSource[];
  llmProvider: string;
  llmModel: string;
  llmTokensInput: number;
  llmTokensOutput: number;
  llmLatencyMs: number;
  verificationAgent: string;
  verifiedAt: Date;
  verifiedBy: string | null;
  published: boolean;
  publishedAt: Date | null;
  publishedChannels: string[];
  createdAt: Date;
}

export interface VerificationSource {
  name: string;
  url: string;
  data: Record<string, unknown>;
}

export interface VerifyClaimInput {
  claimId: string;
}

export interface VerifyClaimOutput {
  verdict: Verdict;
  confidence: number;
  explanation: string;
  simpleExplanation: string;
  sources: VerificationSource[];
}

// ============================================================================
// ECONOMIC DATA TYPES
// ============================================================================

export type EconomicIndicator = 
  | 'inflation_monthly'
  | 'inflation_yearly'
  | 'poverty'
  | 'employment'
  | 'unemployment'
  | 'dollar_official_buy'
  | 'dollar_official_sell'
  | 'dollar_blue_buy'
  | 'dollar_blue_sell'
  | 'reserves'
  | 'interest_rate'
  | 'gdp'
  | 'trade_balance';

export type EconomicDataSource = 'INDEC' | 'BCRA' | 'BOLETIN_OFICIAL' | 'MIN_ECONOMIA' | 'WORLD_BANK';
export type PeriodType = 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly';

export interface EconomicData {
  id: string;
  indicator: EconomicIndicator;
  value: number;
  previousValue: number | null;
  period: Date;
  periodType: PeriodType;
  source: EconomicDataSource;
  sourceUrl: string | null;
  unit: string | null;
  notes: string | null;
  collectedAt: Date;
  collectionAgent: string;
  createdAt: Date;
}

export interface IndicatorSummary {
  indicator: EconomicIndicator;
  currentValue: number;
  previousValue: number | null;
  change: number | null;
  changePercent: number | null;
  period: Date;
  source: EconomicDataSource;
  unit: string;
}

// ============================================================================
// AGENT TYPES
// ============================================================================

export type AgentId = 'agent-1' | 'agent-2' | 'agent-3' | 'agent-4' | 'agent-5' | 'agent-6' | 'agent-7';

export interface AgentResult<T> {
  success: boolean;
  data: T | null;
  error: AgentError | null;
  metadata: AgentMetadata;
}

export interface AgentError {
  code: string;
  message: string;
  retryable: boolean;
}

export interface AgentMetadata {
  agentId: AgentId;
  llmProvider: string;
  llmModel: string;
  tokensInput: number;
  tokensOutput: number;
  latencyMs: number;
  confidence?: number;
}

// Agent 1: Data Collector
export interface DataCollectorInput {
  sources: EconomicDataSource[];
  indicators: EconomicIndicator[];
}

export interface DataCollectorOutput {
  collected: EconomicData[];
  errors: { source: string; error: string }[];
}

// Agent 2: Claim Extractor
export interface ClaimExtractorInput {
  text: string;
  sourceType: ClaimSourceType;
  speaker?: string;
  date?: Date;
  context?: string;
}

export interface ClaimExtractorOutput {
  claims: ExtractedClaim[];
}

export interface ExtractedClaim {
  text: string;
  speaker: string;
  category: ClaimCategory;
  verifiable: boolean;
  confidence: number;
}

// Agent 3: Fact Checker
export interface FactCheckerInput {
  claimId: string;
  claimText: string;
  category: ClaimCategory;
}

export interface FactCheckerOutput extends VerifyClaimOutput {}

// Agent 4: Simplifier
export interface SimplifierInput {
  text: string;
  type: 'explanation' | 'indicator' | 'claim';
}

export interface SimplifierOutput {
  simpleText: string;
  examples: string[];
  terms: TermDefinition[];
}

export interface TermDefinition {
  term: string;
  definition: string;
}

// Agent 5: Publisher
export interface PublisherInput {
  verificationId: string;
  channels: PublishChannel[];
}

export interface PublisherOutput {
  published: PublishResult[];
}

export type PublishChannel = 'web' | 'twitter' | 'telegram' | 'newsletter' | 'api' | 'github_issue';

export interface PublishResult {
  channel: PublishChannel;
  success: boolean;
  url?: string;
  error?: string;
}

// Agent 6: Billing
export interface BillingInput {
  event: BillingEvent;
  data: BillingEventData;
}

export type BillingEvent = 
  | 'subscription.created'
  | 'subscription.updated'
  | 'subscription.deleted'
  | 'payment.succeeded'
  | 'payment.failed';

export interface BillingEventData {
  userId: string;
  stripeCustomerId?: string;
  stripeSubscriptionId?: string;
  plan?: Plan;
  amount?: number;
  currency?: string;
}

export interface BillingOutput {
  success: boolean;
  user: User;
  action: string;
}

// Agent 7: Learning
export interface LearningInput {
  type: 'daily_report' | 'weekly_analysis' | 'trend_detection';
  dateRange?: { start: Date; end: Date };
}

export interface LearningOutput {
  insights: LearningInsight[];
  recommendations: LearningRecommendation[];
}

export interface LearningInsight {
  type: 'trend' | 'anomaly' | 'opportunity';
  description: string;
  data: Record<string, unknown>;
}

export interface LearningRecommendation {
  priority: 'high' | 'medium' | 'low';
  action: string;
  expectedImpact: string;
}

// ============================================================================
// API TYPES
// ============================================================================

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: ApiError | null;
  meta: ApiMeta;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface ApiMeta {
  timestamp: Date;
  requestId: string;
  latencyMs: number;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
    hasMore: boolean;
  };
}

export interface FeedItem {
  id: string;
  type: 'verification' | 'indicator' | 'news';
  title: string;
  summary: string;
  category: ClaimCategory;
  source: string;
  timestamp: Date;
  url: string;
  badge?: {
    type: Verdict;
    color: string;
  };
}

export interface SearchResult {
  type: 'claim' | 'verification' | 'speaker';
  id: string;
  title: string;
  snippet: string;
  relevance: number;
  data: Claim | Verification;
}

// ============================================================================
// SUBSCRIPTION TYPES
// ============================================================================

export interface SubscriptionPlan {
  id: Plan;
  name: string;
  price: number;
  currency: string;
  interval: 'month';
  features: PlanFeature[];
  limits: PlanLimits;
}

export interface PlanFeature {
  id: string;
  name: string;
  included: boolean;
  limit?: number;
}

export interface PlanLimits {
  verificationsPerDay: number;
  alerts: number;
  history: number; // days
  apiAccess: boolean;
  reports: boolean;
  dashboard: boolean;
}

export const PLANS: SubscriptionPlan[] = [
  {
    id: 'free',
    name: 'Free',
    price: 0,
    currency: 'USD',
    interval: 'month',
    features: [
      { id: 'verifications', name: 'Verificaciones', included: true, limit: 3 },
      { id: 'feed', name: 'Feed diario', included: true },
      { id: 'search', name: 'Búsqueda', included: true },
      { id: 'alerts', name: 'Alertas', included: false },
      { id: 'history', name: 'Historial', included: false },
      { id: 'api', name: 'API Access', included: false },
    ],
    limits: {
      verificationsPerDay: 3,
      alerts: 0,
      history: 7,
      apiAccess: false,
      reports: false,
      dashboard: false,
    },
  },
  {
    id: 'premium',
    name: 'Premium',
    price: 5,
    currency: 'USD',
    interval: 'month',
    features: [
      { id: 'verifications', name: 'Verificaciones ilimitadas', included: true },
      { id: 'feed', name: 'Feed diario', included: true },
      { id: 'search', name: 'Búsqueda avanzada', included: true },
      { id: 'alerts', name: 'Alertas personalizadas', included: true, limit: 10 },
      { id: 'history', name: 'Historial completo', included: true },
      { id: 'newsletter', name: 'Newsletter exclusivo', included: true },
    ],
    limits: {
      verificationsPerDay: Infinity,
      alerts: 10,
      history: 365,
      apiAccess: false,
      reports: false,
      dashboard: false,
    },
  },
  {
    id: 'professional',
    name: 'Professional',
    price: 50,
    currency: 'USD',
    interval: 'month',
    features: [
      { id: 'verifications', name: 'Verificaciones ilimitadas', included: true },
      { id: 'feed', name: 'Feed diario', included: true },
      { id: 'search', name: 'Búsqueda avanzada', included: true },
      { id: 'alerts', name: 'Alertas ilimitadas', included: true },
      { id: 'history', name: 'Historial completo', included: true },
      { id: 'api', name: 'API Access', included: true },
      { id: 'reports', name: 'Reportes PDF', included: true },
      { id: 'dashboard', name: 'Dashboard B2B', included: true },
    ],
    limits: {
      verificationsPerDay: Infinity,
      alerts: Infinity,
      history: Infinity,
      apiAccess: true,
      reports: true,
      dashboard: true,
    },
  },
];
```

---

