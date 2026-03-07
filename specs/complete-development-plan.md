# birdie69 - Complete Development Plan

**App Name:** birdie69  
**Domain:** birdie69.com  
**Timeline:** 16 weeks to MVP launch  
**Last Updated:** January 2025

---

## Table of Contents

1. [Technology Stack](#1-technology-stack)
2. [Architecture Overview](#2-architecture-overview)
3. [Repository Structure](#3-repository-structure)
4. [Week-by-Week Development Plan](#4-week-by-week-development-plan)
5. [Database Schema](#5-database-schema)
6. [API Endpoints](#6-api-endpoints)
7. [DevOps & Infrastructure](#7-devops--infrastructure)
8. [Cost Estimation](#8-cost-estimation)
9. [Success Metrics](#9-success-metrics)
10. [Go-to-Market Strategy](#10-go-to-market-strategy)

---

## 1. Technology Stack

### Backend Services
- **Core API**: C# ASP.NET Core (.NET 8)
- **Content Management**: Strapi (self-hosted on Azure App Service)
- **Authentication**: Azure AD B2C (External ID)
- **Database**: PostgreSQL 15+ (Azure Database for PostgreSQL)
- **Cache**: Redis (Azure Cache for Redis)
- **File Storage**: Azure Blob Storage
- **Background Jobs**: Hangfire

### Frontend
- **Web**: Next.js 14+ (React with TypeScript)
- **Mobile**: iOS 15+, Android 8.0+
- **UI Framework**: Tailwind CSS + shadcn/ui

### Infrastructure & DevOps
- **Cloud Provider**: Microsoft Azure (100% Terraform managed)
- **DNS & CDN**: Cloudflare (free tier + Pro)
- **CI/CD**: GitHub Actions
- **Monitoring**: Azure Application Insights + Cloudflare Analytics
- **Version Control**: GitHub

### Third-Party Services
- **Payments**: Stripe (subscriptions + one-time)
- **Push Notifications**: Firebase Cloud Messaging
- **Email**: SendGrid or Azure Communication Services
- **Analytics**: Mixpanel

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloudflare Layer                         │
│  - DNS + CDN + WAF + DDoS Protection                        │
│  - Global edge network (200+ cities)                        │
│  - SSL/TLS termination                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                      Azure Tenant                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            Azure AD B2C (Authentication)              │  │
│  │ - Social Login (Google, Facebook, Apple, Instagram)  │  │
│  │ - Passwordless Email (Magic Links)                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                  │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │        Azure Application Gateway (WAF)                │  │
│  └───────────────────────────────────────────────────────┘  │
│           │                      │                  │       │
│  ┌────────▼────────┐  ┌─────────▼──────┐  ┌──────▼──────┐ │
│  │  Next.js Web    │  │                │  │  Strapi CMS │ │
│  │  (App Service)  │  │    iOS/Android │  │ (App Service│ │
│  └─────────────────┘  └────────────────┘  └─────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    C# ASP.NET Core API (Application Logic)           │  │
│  │    Azure App Service (Linux Container)               │  │
│  │  - Question Management & Scheduling                  │  │
│  │  - Relationship Management                           │  │
│  │  - Subscription & Payments (Stripe)                  │  │
│  │  - Notification Service (FCM)                        │  │
│  │  - Analytics & Events                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │         Data Layer (Terraform Managed)               │   │
│  │  ┌─────────────────┐  ┌────────────────────────┐   │   │
│  │  │   PostgreSQL    │  │   Redis Cache          │   │   │
│  │  │ Flexible Server │  │   (Sessions/Cache)     │   │   │
│  │  │ (Shared DB)     │  └────────────────────────┘   │   │
│  │  └─────────────────┘                                │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │   Azure Blob Storage (Media/Backups)        │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │   Azure Key Vault (Secrets Management)      │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Monitoring & Observability                    │  │
│  │  - Application Insights (Logs, Metrics, Traces)      │  │
│  │  - Azure Monitor (Alerts)                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

External Services:
  ├─ Stripe (Payments API)
  ├─ Firebase Cloud Messaging (Push Notifications)
  ├─ SendGrid (Transactional Email)
  └─ Mixpanel (Product Analytics)
```

---

## 3. Repository Structure

```
birdie69/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       ├── strapi-ci.yml
│       ├── web-ci.yml
│       ├── mobile-ios-ci.yml
│       ├── mobile-android-ci.yml
│       └── terraform-ci.yml
│
├── backend/
│   ├── src/
│   │   ├── Core/
│   │   │   ├── Models/
│   │   │   ├── Services/
│   │   │   └── Repositories/
│   │   ├── Features/
│   │   │   ├── Authentication/
│   │   │   ├── Relationships/
│   │   │   ├── Questions/
│   │   │   ├── Answers/
│   │   │   ├── Subscriptions/
│   │   │   └── Notifications/
│   │   ├── Infrastructure/
│   │   ├── Middleware/
│   │   ├── Controllers/
│   │   ├── Program.cs
│   │   └── appsettings.json
│   ├── tests/
│   ├── Dockerfile
│   └── birdie69-api.csproj
│
├── strapi/
│   ├── src/
│   │   └── api/
│   │       └── question/
│   │           ├── content-types/
│   │           ├── controllers/
│   │           └── services/
│   ├── config/
│   ├── Dockerfile
│   └── package.json
│
├── web/
│   ├── app/
│   │   ├── (auth)/
│   │   ├── (dashboard)/
│   │   ├── api/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   ├── lib/
│   ├── capacitor.config.ts
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── package.json
│
├── mobile/
│   ├── android/
│   ├── ios/
│   └── README.md
│
├── infrastructure/
│   ├── terraform/
│   │   ├── modules/
│   │   │   ├── networking/
│   │   │   ├── database/
│   │   │   ├── app-services/
│   │   │   ├── storage/
│   │   │   ├── redis/
│   │   │   └── monitoring/
│   │   ├── environments/
│   │   │   ├── dev/
│   │   │   └── prod/
│   │   └── cloudflare/
│   ├── docker-compose.yml
│   └── scripts/
│
└── docs/
    ├── API.md
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

---

## 4. Week-by-Week Development Plan

### **Week 1: Foundation & Infrastructure**

**Days 1-2: Azure & Cloudflare Setup**
- [ ] Create Azure subscription and resource groups
- [ ] Set up Azure AD B2C tenant
- [ ] Configure social login providers (Google, Facebook, Apple)
- [ ] Purchase and configure domain in Cloudflare
- [ ] Set up GitHub organization and repositories
- [ ] Configure GitHub secrets for Azure credentials

**Days 3-5: Local Development Environment**
- [ ] Create docker-compose.yml for all services
- [ ] Set up PostgreSQL with initial schema
- [ ] Set up Redis
- [ ] Configure C# backend project structure
- [ ] Set up Strapi locally
- [ ] Document local setup process

**Deliverables:**
- ✅ Azure infrastructure provisioned
- ✅ Local development environment running
- ✅ Documentation complete

---

### **Week 2: Authentication & Core Backend**

**Days 1-3: Azure AD B2C Integration**
- [ ] Configure custom user flows
- [ ] Implement JWT token validation in C#
- [ ] Create user context middleware
- [ ] Build user service and repository
- [ ] Test social login flows

**Days 4-5: Core API Structure**
- [ ] Create User entity and repository
- [ ] Build authentication endpoints
- [ ] Implement user profile management
- [ ] Set up Strapi user extension
- [ ] Create API documentation (Swagger)

**Deliverables:**
- ✅ Authentication fully working
- ✅ User management complete
- ✅ API documented

---

### **Week 3: Relationships & Question Management**

**Days 1-3: Relationship System**
- [ ] Create Relationship and RelationshipMember entities
- [ ] Build relationship creation/invitation endpoints
- [ ] Implement partner acceptance flow
- [ ] Add authorization middleware
- [ ] Test multi-partner scenarios

**Days 4-5: Question Management**
- [ ] Create Question content type in Strapi
- [ ] Populate 500+ questions across categories
- [ ] Build C# service to fetch questions from Strapi
- [ ] Implement daily question scheduling logic
- [ ] Create background job for question delivery

**Deliverables:**
- ✅ Relationships CRUD working
- ✅ Strapi with 500+ questions
- ✅ Daily scheduling tested

---

### **Week 4: Answer System & Web Frontend Auth**

**Days 1-3: Answer System**
- [ ] Create Answer entity and repository
- [ ] Build submit answer endpoint
- [ ] Implement answer reveal logic (WebSocket/SignalR)
- [ ] Create answer history endpoints
- [ ] Test real-time synchronization

**Days 4-5: Next.js Authentication**
- [ ] Set up Next.js project
- [ ] Create login/register pages
- [ ] Implement Azure AD B2C integration (NextAuth.js)
- [ ] Build protected route middleware
- [ ] Set up token storage (HTTP-only cookies)

**Deliverables:**
- ✅ Answer system complete
- ✅ Web authentication working
- ✅ Protected routes functional

---

### **Week 5-6: Web Dashboard**

**Week 5: Dashboard UI**
- [ ] Create dashboard layout
- [ ] Build relationship card component
- [ ] Implement partner connection flow
- [ ] Add relationship status views
- [ ] Create navigation structure

**Week 6: Question Interface**
- [ ] Build question display component
- [ ] Create answer input with auto-save
- [ ] Implement answer reveal animation
- [ ] Build question history page
- [ ] Add anonymous question feature

**Deliverables:**
- ✅ Web dashboard complete
- ✅ Question/answer flow working
- ✅ History and anonymous questions functional

---

### **Week 7-8: Mobile Apps with Capacitor**

**Week 7: Capacitor Setup**
- [ ] Install and configure Capacitor
- [ ] Set up iOS project in Xcode
- [ ] Set up Android project in Android Studio
- [ ] Configure platform detection
- [ ] Implement mobile-specific routing
- [ ] Add native plugins (Camera, Biometrics, Push)

**Week 8: Mobile Features & Polish**
- [ ] Implement bottom navigation
- [ ] Add mobile-optimized components
- [ ] Configure deep linking
- [ ] Test on iOS simulator and Android emulator
- [ ] Build for TestFlight and Play Store Beta
- [ ] Create app store assets

**Deliverables:**
- ✅ Mobile apps functional
- ✅ 80% code reuse achieved
- ✅ Ready for beta testing

---

### **Week 9: Infrastructure as Code**

**Days 1-2: Core Infrastructure (Terraform)**
- [ ] Create Terraform modules for all Azure resources
- [ ] Set up PostgreSQL Flexible Server
- [ ] Configure Redis Cache
- [ ] Set up Azure Key Vault
- [ ] Create Storage Account and Blob containers

**Days 3-4: App Services**
- [ ] Deploy C# API to App Service
- [ ] Deploy Strapi to App Service
- [ ] Deploy Next.js web to App Service
- [ ] Configure environment variables
- [ ] Set up custom domains

**Day 5: Cloudflare Configuration**
- [ ] Configure DNS records
- [ ] Set up WAF rules
- [ ] Configure rate limiting
- [ ] Add security headers
- [ ] Enable caching

**Deliverables:**
- ✅ 100% infrastructure as code
- ✅ All services deployed to Azure
- ✅ Cloudflare configured

---

### **Week 10: Subscriptions & Payments**

**Days 1-3: Stripe Integration**
- [ ] Create Subscription entity
- [ ] Build Stripe customer creation
- [ ] Implement checkout session creation
- [ ] Set up webhook handling
- [ ] Test trial management

**Days 4-5: Payment UI**
- [ ] Build subscription plans page (web)
- [ ] Implement payment form
- [ ] Configure iOS In-App Purchase
- [ ] Configure Android In-App Billing
- [ ] Test full payment flows

**Deliverables:**
- ✅ Stripe fully integrated
- ✅ Subscriptions working
- ✅ All payment methods tested

---

### **Week 11: Notifications & Real-Time**

**Days 1-3: Push Notifications**
- [ ] Set up Firebase Cloud Messaging
- [ ] Create notification service in C#
- [ ] Implement device token management
- [ ] Build notification templates
- [ ] Test on iOS and Android devices

**Days 4-5: Real-Time Features**
- [ ] Implement SignalR for answer sync
- [ ] Create notification hub
- [ ] Build real-time partner status
- [ ] Test WebSocket connections
- [ ] Optimize for mobile networks

**Deliverables:**
- ✅ Push notifications working
- ✅ Real-time sync functional
- ✅ Tested on all platforms

---

### **Week 12: Testing & Quality Assurance**

**Days 1-3: Automated Testing**
- [ ] Write unit tests for C# services (80% coverage)
- [ ] Create integration tests for API endpoints
- [ ] Build E2E tests (Playwright for web)
- [ ] Test authentication flows thoroughly
- [ ] Performance testing (load tests)

**Days 4-5: Manual Testing**
- [ ] Complete user flow testing
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile device testing (iOS + Android)
- [ ] Edge case testing
- [ ] Bug fixing sprint

**Deliverables:**
- ✅ 80%+ test coverage
- ✅ All critical flows tested
- ✅ Bug list prioritized and fixed

---

### **Week 13: DevOps & CI/CD**

**Days 1-3: GitHub Actions Pipelines**
- [ ] Create backend CI/CD workflow
- [ ] Create Strapi deployment pipeline
- [ ] Create web frontend pipeline
- [ ] Create mobile build pipeline (iOS/Android)
- [ ] Set up automated testing in CI

**Days 4-5: Monitoring & Alerts**
- [ ] Configure Application Insights
- [ ] Set up error tracking (Sentry optional)
- [ ] Create monitoring dashboards
- [ ] Configure alert rules
- [ ] Test incident response

**Deliverables:**
- ✅ Automated deployments working
- ✅ Monitoring in place
- ✅ Alerts configured

---

### **Week 14: Security & Compliance**

**Days 1-3: Security Hardening**
- [ ] Implement rate limiting
- [ ] Configure CORS properly
- [ ] Add input validation everywhere
- [ ] Set up security headers
- [ ] Run security audit (OWASP)

**Days 4-5: Documentation & Compliance**
- [ ] Write API documentation
- [ ] Create deployment guide
- [ ] Write privacy policy
- [ ] Create terms of service
- [ ] GDPR compliance checklist

**Deliverables:**
- ✅ Security audit passed
- ✅ All documentation complete
- ✅ Legal documents ready

---

### **Week 15: Performance & Optimization**

**Days 1-3: Performance Tuning**
- [ ] Database query optimization
- [ ] Implement caching strategies
- [ ] Optimize images and assets
- [ ] Minify and bundle code
- [ ] Load testing with 10k users

**Days 4-5: Scaling Preparation**
- [ ] Set up auto-scaling rules
- [ ] Configure database read replicas
- [ ] Implement CDN for static assets
- [ ] Test failover scenarios
- [ ] Document scaling procedures

**Deliverables:**
- ✅ Performance optimized
- ✅ Can handle 10k+ concurrent users
- ✅ Scaling strategy documented

---

### **Week 16: Beta Launch**

**Days 1-3: App Store Submission**
- [ ] Create App Store Connect listing
- [ ] Create Google Play Console listing
- [ ] Prepare screenshots and videos
- [ ] Write app descriptions
- [ ] Submit for review

**Days 4-5: Soft Launch**
- [ ] Deploy to production
- [ ] Invite 100-500 beta testers
- [ ] Monitor for critical issues
- [ ] Collect user feedback
- [ ] Final bug fixes

**Deliverables:**
- ✅ MVP live in production
- ✅ Apps submitted to stores
- ✅ Beta program running

---

## 5. Database Schema

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    azure_ad_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    avatar_url TEXT,
    bio TEXT,
    social_provider VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Relationships
CREATE TABLE relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    status VARCHAR(20) DEFAULT 'active',
    relationship_type VARCHAR(50) DEFAULT 'monogamous',
    started_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relationship Members
CREATE TABLE relationship_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    relationship_id UUID NOT NULL REFERENCES relationships(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(relationship_id, user_id)
);

-- Daily Questions
CREATE TABLE daily_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    relationship_id UUID NOT NULL REFERENCES relationships(id) ON DELETE CASCADE,
    question_content TEXT NOT NULL,
    question_category VARCHAR(50),
    difficulty_level INTEGER DEFAULT 1,
    scheduled_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(relationship_id, scheduled_date)
);

-- Answers
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    daily_question_id UUID NOT NULL REFERENCES daily_questions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_visible_to_partner BOOLEAN DEFAULT false,
    UNIQUE(daily_question_id, user_id)
);

-- Anonymous Questions
CREATE TABLE anonymous_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    relationship_id UUID NOT NULL REFERENCES relationships(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    answered_at TIMESTAMP,
    answer_content TEXT,
    is_revealed BOOLEAN DEFAULT false,
    is_purchased BOOLEAN DEFAULT false
);

-- Subscriptions
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    subscription_id UUID REFERENCES subscriptions(id),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20),
    stripe_transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Devices (Push Notifications)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_type VARCHAR(20),
    fcm_token TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, fcm_token)
);

-- Notification Logs
CREATE TABLE notification_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50),
    title VARCHAR(255),
    body TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);

-- Analytics Events
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_azure_ad_id ON users(azure_ad_id);
CREATE INDEX idx_relationship_members_user ON relationship_members(user_id);
CREATE INDEX idx_daily_questions_rel_date ON daily_questions(relationship_id, scheduled_date);
CREATE INDEX idx_answers_daily_q ON answers(daily_question_id);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_devices_user ON devices(user_id);
```

---

## 6. API Endpoints

### Authentication
```
POST   /api/v1/auth/callback          # Azure AD B2C callback
POST   /api/v1/auth/passwordless      # Send magic link
GET    /api/v1/auth/me                # Get current user
POST   /api/v1/auth/logout            # Logout
```

### Users
```
GET    /api/v1/users/profile
PUT    /api/v1/users/profile
PUT    /api/v1/users/settings
DELETE /api/v1/users/account
```

### Relationships
```
POST   /api/v1/relationships
POST   /api/v1/relationships/:id/invite
POST   /api/v1/relationships/:id/accept
GET    /api/v1/relationships
GET    /api/v1/relationships/:id
DELETE /api/v1/relationships/:id/leave
```

### Questions
```
GET    /api/v1/questions/today
GET    /api/v1/questions/history
POST   /api/v1/questions/:id/answer
GET    /api/v1/questions/:id/answers
POST   /api/v1/questions/anonymous
```

### Subscriptions
```
GET    /api/v1/subscriptions/plans
POST   /api/v1/subscriptions/start
GET    /api/v1/subscriptions/current
PUT    /api/v1/subscriptions/cancel
POST   /api/v1/webhooks/stripe
```

---

## 7. DevOps & Infrastructure

### Terraform Modules

**Database Module**
```hcl
resource "azurerm_postgresql_flexible_server" "main" {
  name                = "birdie69-db-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  
  administrator_login    = var.db_user
  administrator_password = var.db_password
  
  storage_mb            = 32768
  backup_retention_days = 30
  sku_name              = "B_Standard_B2s"
  version               = "15"
}
```

**App Service Module**
```hcl
resource "azurerm_linux_web_app" "api" {
  name                = "birdie69-api-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    always_on = true
    application_stack {
      docker_image     = "${var.acr_login_server}/birdie69-api"
      docker_image_tag = var.image_tag
    }
  }

  app_settings = {
    "ConnectionStrings__DefaultConnection" = var.database_connection_string
    "Redis__Host" = var.redis_host
    "AzureAdB2C__ClientId" = var.b2c_client_id
    "Stripe__SecretKey" = "@Microsoft.KeyVault(SecretUri=${var.stripe_secret_uri})"
  }
}
```

### GitHub Actions CI/CD

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main]
    paths: ['backend/**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup .NET
        uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '8.0.x'
      - name: Run tests
        run: dotnet test backend/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Build and push Docker image
        run: |
          docker build -t birdie69-api:${{ github.sha }} backend/
          docker push ${{ secrets.ACR_LOGIN_SERVER }}/birdie69-api:${{ github.sha }}
      
      - name: Deploy to App Service
        run: |
          az webapp update --resource-group birdie69-prod --name birdie69-api-prod --docker-custom-image-name birdie69-api:${{ github.sha }}
```

---

## 8. Cost Estimation

### Monthly Operating Costs (Production)

| Service | Tier | Cost |
|---------|------|------|
| App Service Plan (P1v3) | 3 apps | $146 |
| PostgreSQL (B2s) | 2 vCPU, 4GB | $73 |
| Redis Cache (C2) | 2.5GB | $75 |
| Blob Storage | 100GB | $20 |
| Key Vault | Standard | $5 |
| Application Insights | 5GB | $15 |
| Cloudflare Pro | DNS + WAF | $20 |
| SendGrid | 40k emails | $15 |
| Firebase | Push notifications | $0 |
| Stripe | 2.9% + $0.30 | Variable |
| **Total Base** | | **~$369/month** |

**First Year Estimate:**
- Infrastructure: ~$4,428
- Development: Time investment
- Third-party: ~$1,200
- **Total: ~$5,628 + Dev time**

---

## 9. Success Metrics

### User Acquisition
- Month 1-3: 1,000 signups
- Month 4-6: 3,000 cumulative
- Month 7-12: 15,000 cumulative

### Engagement
- Daily Active Users: 40%+
- Daily Question Completion: 50%+
- 7-Day Retention: 60%+
- 30-Day Retention: 40%+

### Monetization
- Trial-to-Paid Conversion: 15-25%
- Month 1-3 MRR: $600
- Month 12 MRR: $15,000
- Year 1 ARR: $180,000

---

## 10. Go-to-Market Strategy

### Pre-Launch (Weeks 14-16)
- Create landing page (birdie69.com)
- Build waitlist (target: 500-1000)
- Content marketing (10 blog posts)
- Social media presence
- Beta user recruitment

### Launch Week (Week 17)
- Product Hunt launch
- Press releases
- Influencer partnerships
- Reddit AMAs
- Email waitlist

### Growth Channels
- **Organic**: SEO, content, social media, ASO
- **Paid**: Google Ads, Facebook/Instagram Ads
- **Partnerships**: Therapists, dating apps, wedding industry
- **Referral**: Both users get 1 month free

---

## 11. Daily Development Workflow

### Morning Routine
1. Pull latest changes
2. Review tasks for the day
3. Check CI/CD status

### Development Cycle
```bash
# Create feature branch
git checkout -b feature/question-scheduling

# Develop locally
docker-compose up -d

# Test
dotnet test backend/
npm test --prefix web/

# Commit
git commit -m "feat: add question scheduling"

# Push and create PR
git push origin feature/question-scheduling
```

### Evening Review
1. Commit all work
2. Update progress
3. Plan next day

---

## 12. Risk Mitigation

### Technical Risks
- **Azure outage**: Multi-region deployment
- **Data breach**: Encryption + audits
- **Scalability**: Auto-scaling + load testing

### Business Risks
- **Low acquisition**: Multiple channels + referral program
- **Poor conversion**: Onboarding optimization
- **High churn**: Engagement features + email campaigns

---

## 13. Conclusion

This development plan provides:

✅ **Clear 16-week timeline** to MVP launch  
✅ **Complete technology stack** with modern tools  
✅ **Detailed architecture** with Azure + Cloudflare  
✅ **Week-by-week tasks** with deliverables  
✅ **Database schema** ready to implement  
✅ **API specification** documented  
✅ **DevOps strategy** with Terraform + GitHub Actions  
✅ **Cost estimates** and revenue projections  
✅ **Success metrics** to track progress  
✅ **Go-to-market strategy** for launch  

**Ready to build birdie69 and change relationships! 🚀**

---

*Let's start Day 1 development!*