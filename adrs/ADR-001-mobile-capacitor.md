# ADR-001: Mobile Strategy — Capacitor over Native (MVP)

**Date:** 2026-02-14  
**Status:** Accepted  
**Deciders:** Instructor, SA Agent  
**Category:** Mobile Architecture

---

## Context

birdie69 must deliver a mobile experience on both iOS and Android.  
The core product is identical on both platforms (same UI, same logic).  
We need to ship an MVP quickly, maintain a single codebase for web+mobile, and defer native investment until post-product-market-fit.

---

## Decision

Use **Capacitor** to wrap the Next.js 14+ web application into native iOS and Android app shells for MVP.

Native apps (SwiftUI / Kotlin) are planned as a **post-MVP phase** when user retention data justifies platform-specific investment.

---

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| **Capacitor (chosen)** | Single codebase, fast MVP, full web stack reuse, native plugins available | Not fully native UX, performance ceiling |
| Native iOS (SwiftUI) | Best iOS UX, full Apple ecosystem access | 2× codebase, slower delivery |
| Native Android (Kotlin) | Best Android UX | 2× codebase, slower delivery |
| React Native | Cross-platform native | Different stack than Next.js, not web-first |
| Flutter | Cross-platform native | Dart, separate codebase, not web-first |

---

## Consequences

### Positive
- Single Next.js codebase serves web, iOS, and Android
- Capacitor plugins provide access to Camera, Push Notifications, Haptics, etc.
- Faster MVP delivery (no native engineers needed initially)
- Easy to iterate on product without platform-specific constraints

### Negative
- Some UX nuances are not fully native (navigation gestures, platform conventions)
- Complex animations may have performance limits
- App Store review process applies to Capacitor apps

### Future
- After MVP validation (D7 retention > 40%, 1K+ couples), evaluate native rewrites for each platform
- iOS: SwiftUI (if iOS engagement justifies it)
- Android: Kotlin (if Android engagement justifies it)

---

## References

- [Capacitor documentation](https://capacitorjs.com/docs)
- `PROJECT_CHARTER.md` — Non-Goals section (native apps)
- `ARCHITECTURE_OVERVIEW.md` — Mobile/Web Architecture section
