import { DatoError } from './base.error';

/**
 * Error for external service failures
 */
export class ExternalServiceError extends DatoError {
  constructor(service: string, message: string, details?: Record<string, unknown>) {
    super(`External service '${service}' error: ${message}`, 'EXTERNAL_SERVICE_ERROR', 503, {
      service,
      ...details,
    });
  }
}

/**
 * Error for AI/LLM service failures
 */
export class AIServiceError extends ExternalServiceError {
  constructor(message: string, details?: Record<string, unknown>) {
    super('AI Service', message, details);
  }
}

/**
 * Error for database failures
 */
export class DatabaseError extends DatoError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'DATABASE_ERROR', 500, details);
  }
}
