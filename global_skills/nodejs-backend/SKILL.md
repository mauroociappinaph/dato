---
name: nodejs-backend
description: Node.js backend architecture, NestJS patterns, and API design. 2026 Edition.
inherited_from: [gemini-skill-creator, typescript-pro, infrastructure-core]
---

# Node.js Backend (Compressed)

## Purpose
Build scalable, maintainable, and secure Node.js backends with NestJS.

## Core Capabilities
- **NestJS**: Modules, guards, interceptors, pipes, decorators
- **API Design**: REST, GraphQL, tRPC, OpenAPI documentation
- **Database**: Prisma ORM, migrations, transactions
- **Authentication**: JWT, OAuth2, Supabase Auth integration
- **Real-time**: WebSockets, Server-Sent Events, Socket.io

## Architecture Patterns
```
src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.module.ts
│   │   └── dto/
│   ├── users/
│   └── claims/
├── common/
│   ├── decorators/
│   ├── guards/
│   ├── interceptors/
│   └── filters/
└── config/
```

## NestJS Best Practices
- Dependency injection throughout
- Modular architecture
- Request validation with class-validator
- Response transformation with interceptors
- Error handling with exception filters

## Security Checklist
- [ ] Helmet middleware
- [ ] Rate limiting
- [ ] CORS configured
- [ ] Input validation
- [ ] SQL injection prevention (Prisma)
- [ ] XSS protection

## Performance
- Connection pooling
- Query optimization
- Caching with Redis
- Queue-based processing (Bull)

## Related Skills
- `typescript-pro/`: Type safety
- `infrastructure-core/`: Supabase, Redis
- `api-endpoint-tester/`: Contract validation
- `security-auditor/`: Security review
