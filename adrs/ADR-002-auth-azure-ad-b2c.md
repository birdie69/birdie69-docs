# ADR-002: Authentication — Azure AD B2C (Externalized Identity)

**Date:** 2026-02-14  
**Status:** Accepted  
**Deciders:** Instructor, SA Agent  
**Category:** Security / Identity

---

## Context

birdie69 supports multiple authentication providers: Apple Sign-In, Google Sign-In, and Email Magic Link (passwordless).  
Managing these providers in-house requires implementing OAuth 2.0 flows for each provider, handling token exchange, managing user sessions, and ensuring security compliance — a significant engineering burden that distracts from core product development.

---

## Decision

Use **Azure AD B2C** as the externalized identity provider.

The application stores only the **B2C Object ID** (`externalId`) to identify users — no passwords, no provider tokens are stored in the application database.

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Azure AD B2C (chosen)** | Multi-provider support, PKCE, enterprise-grade, no passwords in app DB | Azure dependency, B2C pricing, learning curve |
| Custom JWT (previous blog project pattern) | Full control, no external dependency | Must implement each provider separately, security risk, maintenance burden |
| Auth0 | Excellent DX, multi-provider | Higher cost at scale, not Azure-native |
| Supabase Auth | Simple, PostgreSQL-native | Fewer providers, not enterprise-grade |
| Firebase Auth | Easy mobile setup | Google dependency, limited customization |

---

## External ID Pattern

```
B2C Object ID (externalId)
    ↓
Application User table
    ↓
All application entities reference User.id (internal UUID)
```

- B2C manages: provider federation, token issuance, MFA (optional)
- Application manages: business identity (display name, preferences, couple link)
- No sync issues: externalId is immutable, users are created on first login

---

## Token Flow

```
Mobile/Web → B2C (OAuth 2.0 Authorization Code + PKCE)
           ← ID Token (profile claims) + Access Token (JWT)
           → .NET 8 API (Bearer token)
           → API validates JWT signature against B2C JWKS endpoint
           → Extracts externalId from `sub` claim
```

---

## Consequences

### Positive
- Zero password management in the application
- All 3 providers (Apple, Google, Magic Link) handled by B2C
- PKCE enforced by default (secure for mobile)
- Token validation is stateless (no DB call on each request)
- Easy to add new providers (e.g., Facebook) via B2C configuration
- Compliance (GDPR, SOC2) easier with externalized identity

### Negative
- Azure vendor lock-in for identity
- B2C custom user flows require some configuration
- B2C has a free tier (50K MAUs/month), then pricing applies
- Local development requires B2C tenant or mock token service

### Mitigation for Local Dev
- Use a lightweight JWT mock service or `dotnet-auth-mock` for local development
- Keep the B2C integration behind an interface for easy swap in tests

---

## References

- [Azure AD B2C documentation](https://docs.microsoft.com/en-us/azure/active-directory-b2c/)
- [Microsoft.Identity.Web for ASP.NET Core](https://github.com/AzureAD/microsoft-identity-web)
- `ARCHITECTURE_OVERVIEW.md` — Authentication Flow section
