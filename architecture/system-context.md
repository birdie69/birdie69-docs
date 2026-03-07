# System Context — birdie69

**Version:** 1.0  
**Date:** 2026-02-14  
**Author:** SA Agent

---

## System Context Diagram

```mermaid
graph TB
    subgraph Users
        UA[User A - Partner 1<br/>iOS / Android / Web]
        UB[User B - Partner 2<br/>iOS / Android / Web]
        CE[Content Editor<br/>Strapi Admin UI]
    end

    subgraph birdie69 System
        WEB[birdie69 Web/Mobile<br/>Next.js 14+ + Capacitor]
        API[birdie69 API<br/>.NET 8 ASP.NET Core]
        CMS[birdie69 CMS<br/>Strapi v5]
    end

    subgraph Azure
        B2C[Azure AD B2C<br/>Identity Provider]
        DB[(PostgreSQL 15+<br/>Azure Flexible Server)]
        REDIS[(Redis Cache<br/>Azure Cache for Redis)]
        BLOB[Azure Blob Storage<br/>Profile images]
        KV[Azure Key Vault<br/>Secrets]
    end

    subgraph External Services
        STRIPE[Stripe<br/>Payments]
        FCM[Firebase FCM<br/>Push Notifications]
        SG[SendGrid<br/>Transactional Email]
        CF[Cloudflare<br/>CDN + WAF]
        MX[Mixpanel<br/>Product Analytics]
    end

    UA -->|HTTPS| CF
    UB -->|HTTPS| CF
    CF --> WEB
    WEB -->|JWT Bearer| API
    WEB -->|PKCE OAuth2| B2C
    B2C -->|JWT tokens| WEB
    API -->|Validate JWT| B2C
    API --- DB
    API --- REDIS
    API --- BLOB
    API --- KV
    API -->|Charge / Webhook| STRIPE
    API -->|Push message| FCM
    API -->|Send email| SG
    API -->|Read questions| CMS
    CE -->|Manage content| CMS
    CMS --- DB
    FCM -->|Push notification| UA
    FCM -->|Push notification| UB
    UA -->|Events| MX
    UB -->|Events| MX
```

---

## Key Interactions

### User Authentication
1. User opens app → MSAL redirects to Azure AD B2C
2. User signs in (Apple / Google / Magic Link)
3. B2C issues ID Token + Access Token (JWT)
4. App stores tokens securely (Capacitor Secure Storage)
5. All API calls include `Authorization: Bearer <access_token>`
6. API validates token against B2C JWKS endpoint on every request

### Daily Question Flow
1. Content editor creates question in Strapi CMS (scheduled for a date)
2. At midnight UTC, `birdie69-api` fetches the new question from Strapi
3. Question is cached in Redis (TTL = seconds until next midnight)
4. FCM sends push notification to all registered users
5. User opens app → GET /v1/questions/today → receives cached question

### Answer Reveal Flow
1. User A submits answer → POST /v1/answers → stored, flagged as "not revealed"
2. User A sees "Waiting for [Partner]..."
3. User B submits answer → POST /v1/answers
4. API detects both partners answered → sets `revealed = true`
5. FCM push: "Your partner answered! See their response."
6. Both GET /v1/answers/{questionId} → both answers visible

---

## Deployment Architecture

```mermaid
graph TB
    subgraph Azure Container Apps Environment
        API_APP[Container App<br/>birdie69-api<br/>0.5 CPU / 1Gi RAM<br/>Scale: 1–10 replicas]
        CMS_APP[Container App<br/>birdie69-cms<br/>0.5 CPU / 1Gi RAM<br/>Scale: 1–3 replicas]
    end

    subgraph Data Layer
        PG[(PostgreSQL<br/>Flexible Server<br/>B1ms dev / GP_Standard prod)]
        RD[(Redis Cache<br/>C0 dev / C1 prod)]
    end

    subgraph Security
        KV[Key Vault]
        B2C[Azure AD B2C]
        ACR[Azure Container Registry]
    end

    CF[Cloudflare] --> API_APP
    CF --> CMS_APP
    API_APP --- PG
    API_APP --- RD
    API_APP -->|Secret refs| KV
    CMS_APP --- PG
    ACR -->|Image pull| API_APP
    ACR -->|Image pull| CMS_APP
```
