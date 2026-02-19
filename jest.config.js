/** @type {import('jest').Config} */
module.exports = {
  projects: [
    {
      displayName: 'shared',
      testMatch: ['<rootDir>/packages/shared/**/*.test.ts'],
      transform: {
        '^.+\\.ts$': ['ts-jest', { useESM: true }],
      },
      moduleNameMapper: {
        '^(\\.{1,2}/.*)\\.js$': '$1',
      },
      extensionsToTreatAsEsm: ['.ts'],
    },
    {
      displayName: 'agents',
      testMatch: ['<rootDir>/packages/agents/**/*.test.ts'],
      transform: {
        '^.+\\.ts$': ['ts-jest', { useESM: true }],
      },
      moduleNameMapper: {
        '^(\\.{1,2}/.*)\\.js$': '$1',
        '@dato/shared': '<rootDir>/packages/shared/src',
      },
      extensionsToTreatAsEsm: ['.ts'],
    },
    {
      displayName: 'database',
      testMatch: ['<rootDir>/packages/database/**/*.test.ts'],
      transform: {
        '^.+\\.ts$': ['ts-jest', { useESM: true }],
      },
      moduleNameMapper: {
        '^(\\.{1,2}/.*)\\.js$': '$1',
        '@dato/shared': '<rootDir>/packages/shared/src',
      },
      extensionsToTreatAsEsm: ['.ts'],
    },
    {
      displayName: 'web',
      testEnvironment: 'jsdom',
      testMatch: ['<rootDir>/apps/web/**/*.test.{ts,tsx}'],
      transform: {
        '^.+\\.(ts|tsx)$': ['ts-jest', { useESM: true, tsconfig: 'apps/web/tsconfig.json' }],
      },
      moduleNameMapper: {
        '^(\\.{1,2}/.*)\\.js$': '$1',
        '^@/(.*)$': '<rootDir>/apps/web/src/$1',
        '@dato/shared': '<rootDir>/packages/shared/src',
      },
      extensionsToTreatAsEsm: ['.ts', '.tsx'],
    },
    {
      displayName: 'api',
      testEnvironment: 'node',
      testMatch: ['<rootDir>/apps/api/**/*.test.ts'],
      transform: {
        '^.+\\.ts$': ['ts-jest', { useESM: true, tsconfig: 'apps/api/tsconfig.json' }],
      },
      moduleNameMapper: {
        '^(\\.{1,2}/.*)\\.js$': '$1',
        '^@/(.*)$': '<rootDir>/apps/api/src/$1',
        '@dato/shared': '<rootDir>/packages/shared/src',
        '@dato/database': '<rootDir>/packages/database/src',
      },
      extensionsToTreatAsEsm: ['.ts'],
    },
  ],
  coverageDirectory: 'coverage',
  collectCoverageFrom: ['**/src/**/*.{ts,tsx}', '!**/*.d.ts', '!**/node_modules/**'],
};
