import { DatoError } from './base.error';

/**
 * Error for validation failures
 */
export class ValidationError extends DatoError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, details);
  }
}

/**
 * Error for missing required fields
 */
export class RequiredFieldError extends ValidationError {
  constructor(field: string) {
    super(`Field '${field}' is required`, { field });
  }
}

/**
 * Error for invalid field format
 */
export class InvalidFormatError extends ValidationError {
  constructor(field: string, expectedFormat: string) {
    super(`Field '${field}' has invalid format. Expected: ${expectedFormat}`, {
      field,
      expectedFormat,
    });
  }
}
