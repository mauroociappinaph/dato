/**
 * DATO Shared Types
 * This file exports all shared TypeScript types
 *
 * Re-exports from @dato/shared for convenience
 */

// Placeholder types - will be expanded in FASE 1
export type AgentName =
  | 'agent-0-orchestrator'
  | 'agent-1-collector'
  | 'agent-2-extractor'
  | 'agent-3-factchecker'
  | 'agent-4-simplifier'
  | 'agent-5-publisher'
  | 'agent-6-billing'
  | 'agent-7-learning'
  | 'agent-8-qa'
  | 'agent-9-growth';

export type VerificationBadge = 'verified' | 'warning' | 'false' | 'unverifiable';

export interface Claim {
  id: string;
  text: string;
  source: string;
  politician?: string;
  date: string;
  verificationStatus?: VerificationBadge;
}

export interface Verification {
  id: string;
  claimId: string;
  status: VerificationBadge;
  summary: string;
  sources: string[];
  createdAt: string;
}
