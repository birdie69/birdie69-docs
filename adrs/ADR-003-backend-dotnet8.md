# ADR-003: Backend API — .NET 8 ASP.NET Core

**Date:** 2026-02-14  
**Status:** Accepted  
**Deciders:** Instructor, SA Agent  
**Category:** Backend Architecture

---

## Context

birdie69 needs a dedicated API layer that handles:
- Business logic (couple matching, answer reveal rules, streak calculation)
- Integration with multiple external services (Stripe, FCM, SendGrid, B2C, Strapi)
- Data access (PostgreSQL, Redis)
- Security enforcement (JWT validation, rate limiting)

The API must be strongly typed, scalable, and maintainable as the product grows.

---

## Decision

Use **C# ASP.NET Core (.NET 8)** with Clean Architecture and Domain-Driven Design.

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **.NET 8 ASP.NET Core (chosen)** | Strong typing, Clean Arch + DDD, excellent Azure integration, performance, NuGet ecosystem | Learning curve (if not familiar), more verbose than JS |
| Node.js / Express | Same stack as Strapi/Next.js, JS everywhere | Weaker typing, less structured for complex domains |
| Node.js / NestJS | Structured, decorators, similar to .NET | Still JS, less performant under load |
| Go | Excellent performance, simple | Smaller ecosystem for business apps, no DDD patterns established |
| Python / FastAPI | Simple, fast to write | Weak typing, not ideal for complex domains |

---

## Architecture Pattern

```
Birdie69.Domain        ← Core business logic, no dependencies
Birdie69.Application   ← Use cases (CQRS commands/queries via MediatR)
Birdie69.Infrastructure ← EF Core, Redis, Azure SDK, external clients
Birdie69.Api           ← ASP.NET Core controllers, middleware, DI
```

### Key Libraries

| Library | Purpose |
|---------|---------|
| MediatR | CQRS commands and queries |
| EF Core 8 | ORM for PostgreSQL |
| FluentValidation | Input validation |
| AutoMapper | DTO ↔ Domain mapping |
| Serilog | Structured logging |
| OpenTelemetry | Distributed tracing |
| xUnit + Moq | Unit and integration testing |
| Swagger / Scalar | OpenAPI documentation |
| Microsoft.Identity.Web | Azure AD B2C JWT validation |

---

## Consequences

### Positive
- Strong typing catches errors at compile time
- Clean Architecture enforces clear separation of concerns
- DDD aligns code with business language (ubiquitous language)
- CQRS makes reads and writes independently scalable
- .NET 8 is LTS (supported until November 2026)
- Excellent Azure-native support (Azure SDK for .NET)
- Container-friendly (lightweight Docker images with `mcr.microsoft.com/dotnet/aspnet`)

### Negative
- More boilerplate than Express/FastAPI for simple CRUD
- Requires understanding of Clean Architecture + DDD patterns
- EF Core migrations require careful management

### Mitigation
- Code generators (Rider / VS scaffolding) reduce boilerplate
- ADR-driven documentation ensures decisions are traceable
- Dev agent follows the SA agent's architecture spec strictly

---

## References

- [ASP.NET Core documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Clean Architecture by Jason Taylor](https://github.com/jasontaylordev/CleanArchitecture)
- [MediatR documentation](https://github.com/jbogard/MediatR)
- `ARCHITECTURE_OVERVIEW.md` — API Architecture section
