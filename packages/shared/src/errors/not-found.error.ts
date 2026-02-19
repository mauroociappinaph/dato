import { DatoError } from './base.error';

/**
 * Error for resource not found
 */
export class NotFoundError extends DatoError {
  constructor(resource: string, identifier?: string | number) {
    const message = identifier
      ? `${resource} with identifier '${identifier}' not found`
      : `${resource} not found`;
    super(message, 'NOT_FOUND', 404, { resource, identifier });
  }
}

/**
 * Error for politician not found
 */
export class PoliticianNotFoundError extends NotFoundError {
  constructor(identifier: string | number) {
    super('Politician', identifier);
  }
}

/**
 * Error for statement not found
 */
export class StatementNotFoundError extends NotFoundError {
  constructor(identifier: string | number) {
    super('Statement', identifier);
  }
}
