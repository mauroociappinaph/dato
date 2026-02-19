# Contributing to DATO

Thank you for your interest in contributing to DATO! This document provides guidelines and instructions for contributing.

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. Please be considerate of others and follow standard open-source community guidelines.

---

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/dato-arg/dato/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear title prefixed with `[Feature]`
   - Detailed description of the feature
   - Use case and benefits
   - Possible implementation (optional)

### Submitting Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit with conventional commits
6. Push to your fork
7. Open a Pull Request

---

## Development Setup

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed setup instructions.

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/dato.git
cd dato

# Install dependencies
pnpm install

# Copy environment variables
cp .env.example .env

# Start development
pnpm dev
```

---

## Coding Standards

### TypeScript

- Use strict mode
- Define types for all functions
- Avoid `any` when possible
- Use interfaces for objects

### Code Style

- ESLint + Prettier configured
- Run `pnpm lint` before committing
- Run `pnpm format` to auto-format

### Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new fact-check verification
fix: resolve claim extraction bug
docs: update API documentation
test: add unit tests for simplifier
refactor: restructure agent modules
```

---

## Project Structure

```
dato/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # NestJS backend
├── packages/
│   ├── ui/           # Shared components
│   ├── agents/       # AI agents
│   └── types/        # TypeScript types
├── docs/             # Documentation
└── tests/            # E2E tests
```

---

## Pull Request Process

1. **Create PR** with clear title and description
2. **Link Issues** that the PR addresses
3. **Run Tests** - All tests must pass
4. **Code Review** - Wait for maintainer review
5. **Address Feedback** - Make requested changes
6. **Merge** - Maintainer will merge when approved

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] Commit messages follow convention
- [ ] PR links to relevant issues

---

## Areas for Contribution

### High Priority
- Agent improvements
- Data source integrations
- Performance optimizations

### Medium Priority
- UI/UX improvements
- Documentation
- Test coverage

### Welcome Contributions
- Translations
- Bug fixes
- Feature requests

---

## Testing

### Running Tests

```bash
# Unit tests
pnpm test

# E2E tests
pnpm test:e2e

# Coverage
pnpm test:coverage
```

### Writing Tests

- Unit tests for utilities and services
- Integration tests for API endpoints
- E2E tests for critical user flows

---

## Documentation

### Updating Docs

- Update README.md for project changes
- Update API.md for endpoint changes
- Update ARCHITECTURE.md for structural changes

### Style Guide

- Use clear, concise language
- Include code examples
- Keep tables and lists formatted

---

## Getting Help

- Open a [Discussion](https://github.com/dato-arg/dato/discussions)
- Join our community (link coming soon)
- Email: dev@dato.ar

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to DATO! 🎉
