/**
 * Result type for functional error handling
 * Inspired by Rust's Result<T, E> pattern
 */

export type Result<T, E = Error> = Success<T> | Failure<E>;

export interface Success<T> {
  ok: true;
  value: T;
}

export interface Failure<E> {
  ok: false;
  error: E;
}

/**
 * Create a successful result
 */
export function Ok<T>(value: T): Success<T> {
  return { ok: true, value };
}

/**
 * Create a failed result
 */
export function Err<E>(error: E): Failure<E> {
  return { ok: false, error };
}

/**
 * Type guard for success
 */
export function isOk<T, E>(result: Result<T, E>): result is Success<T> {
  return result.ok === true;
}

/**
 * Type guard for failure
 */
export function isErr<T, E>(result: Result<T, E>): result is Failure<E> {
  return result.ok === false;
}

/**
 * Map the value if success
 */
export function map<T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> {
  return isOk(result) ? Ok(fn(result.value)) : result;
}

/**
 * Map the error if failure
 */
export function mapErr<T, E, F>(result: Result<T, E>, fn: (error: E) => F): Result<T, F> {
  return isErr(result) ? Err(fn(result.error)) : (result as Result<T, F>);
}

/**
 * Chain operations that return Results
 */
export function andThen<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  return isOk(result) ? fn(result.value) : result;
}

/**
 * Unwrap value or throw
 */
export function unwrap<T, E>(result: Result<T, E>): T {
  if (isOk(result)) {
    return result.value;
  }
  throw result.error;
}

/**
 * Unwrap value or return default
 */
export function unwrapOr<T, E>(result: Result<T, E>, defaultValue: T): T {
  return isOk(result) ? result.value : defaultValue;
}

/**
 * Unwrap value or compute default from error
 */
export function unwrapOrElse<T, E>(result: Result<T, E>, fn: (error: E) => T): T {
  return isOk(result) ? result.value : fn(result.error);
}

/**
 * Convert a promise to a Result
 */
export async function fromPromise<T>(promise: Promise<T>): Promise<Result<T, Error>> {
  try {
    const value = await promise;
    return Ok(value);
  } catch (error) {
    return Err(error instanceof Error ? error : new Error(String(error)));
  }
}

/**
 * Wrap a function that might throw into a Result-returning function
 */
export function tryCatch<T, A extends unknown[]>(
  fn: (...args: A) => T
): (...args: A) => Result<T, Error> {
  return (...args: A) => {
    try {
      return Ok(fn(...args));
    } catch (error) {
      return Err(error instanceof Error ? error : new Error(String(error)));
    }
  };
}
