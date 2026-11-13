# YatraDiscover AI - Complete End-to-End Design

## Project Overview

**YatraDiscover AI** is a premium AI-powered travel planning platform with a luxury, modern aesthetic.

- **Domain:** yatradiscover.com
- **Target Users:** Travel enthusiasts, adventure seekers, luxury travelers
- **Platforms:** Website (Next.js), iOS (SwiftUI), Android (Jetpack Compose)
- **Backend:** Python FastAPI + Supabase PostgreSQL
- **AI:** OpenAI GPT-4 for itinerary generation

## Design Philosophy

**Core Principles:**
1. **Luxury & Elegance** – Clean, sophisticated UI with premium spacing
2. **Intuitive Navigation** – Minimal friction, clear hierarchy
3. **AI-First Experience** – Conversational, intelligent suggestions
4. **Mobile-First** – Optimized for on-the-go travel planning
5. **Fast & Responsive** – Sub-second interactions
6. **Accessibility** – WCAG 2.1 AA compliant

## Brand Identity

### Color Palette

| Purpose | Color | Hex | Usage |
|---------|-------|-----|-------|
| Primary | Sapphire Blue | #1E3A8A | Buttons, Headers, CTAs |
| Secondary | Emerald Green | #065F46 | Accents, Success states |
| Accent | Golden Orange | #EA580C | Highlights, Premium features |
| Neutral Light | Off-White | #F8FAFC | Backgrounds, Cards |
| Neutral Dark | Charcoal | #0F172A | Text, Dark mode |
| Success | Green | #10B981 | Success messages |
| Warning | Amber | #F59E0B | Warnings |
| Error | Red | #EF4444 | Errors |

### Typography

| Style | Font | Weight | Size | Line Height |
|-------|------|--------|------|-------------|
| Display | Inter | Bold (700) | 32-48px | 1.2 |
| Heading 1 | Inter | Bold (600) | 28px | 1.3 |
| Heading 2 | Inter | SemiBold (600) | 22px | 1.3 |
| Heading 3 | Inter | SemiBold (600) | 18px | 1.4 |
| Body Large | Inter | Regular (400) | 16px | 1.6 |
| Body | Inter | Regular (400) | 14px | 1.6 |
| Caption | Inter | Regular (400) | 12px | 1.5 |
| Monospace | IBM Plex Mono | Regular (400) | 13px | 1.6 |

### Spacing Scale

```
xs: 4px
sm: 8px
md: 12px
lg: 16px
xl: 24px
2xl: 32px
3xl: 48px
4xl: 64px
```

### Shadows

```
sm: 0 1px 2px 0 rgba(0,0,0,0.05)
md: 0 4px 6px -1px rgba(0,0,0,0.1)
lg: 0 10px 15px -3px rgba(0,0,0,0.1)
xl: 0 20px 25px -5px rgba(0,0,0,0.1)
2xl: 0 25px 50px -12px rgba(0,0,0,0.25)
```

### Border Radius

```
none: 0px
sm: 4px
md: 8px
lg: 12px
xl: 16px
full: 9999px
```

## Project Structure

```
yatradiscover/
├── design/
│   ├── DESIGN-SYSTEM.md (this file)
│   ├── colors.json
│   ├── typography.json
│   ├── components/
│   │   ├── BUTTONS.md
│   │   ├── FORMS.md
│   │   ├── CARDS.md
│   │   ├── MODALS.md
│   │   ├── NAVIGATION.md
│   │   └── ICONS.md
│   └── screens/
│       ├── WEB_SCREENS.md
│       ├── IOS_SCREENS.md
│       └── ANDROID_SCREENS.md
│
├── frontend/
│   ├── web/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── styles/
│   │   │   └── hooks/
│   │   ├── package.json
│   │   └── next.config.js
│   │
├── mobile/
│   ├── ios/
│   │   ├── YatraDiscover.xcodeproj
│   │   ├── YatraDiscover/
│   │   │   ├── App.swift
│   │   │   ├── Views/
│   │   │   ├── ViewModels/
│   │   │   └── Models/
│   │   └── Podfile
│   │
│   └── android/
│       ├── build.gradle.kts
│       ├── app/
│       │   ├── src/
│       │   │   ├── main/
│       │   │   │   ├── java/com/yatradiscover/
│       │   │   │   │   ├── ui/
│       │   │   │   │   ├── viewmodel/
│       │   │   │   │   └── model/
│       │   │   │   └── res/
│       │   │   └── test/
│       │   └── build.gradle.kts
│       └── settings.gradle.kts
│
└── backend/
    ├── app/
    │   ├── main.py
    │   ├── models/
    │   ├── routes/
    │   ├── services/
    │   └── db/
    ├── requirements.txt
    └── .env.example
```

## Design System Components

### Button Variants

**Primary Button**
- Background: Sapphire Blue (#1E3A8A)
- Text: White
- Height: 44px (mobile), 40px (web)
- Padding: 12px 16px
- Border Radius: 8px
- Font: Inter 14px Bold
- Active State: Darker blue with 0.95 opacity
- Disabled: Gray with 0.5 opacity

**Secondary Button**
- Background: Transparent
- Border: 1px Sapphire Blue
- Text: Sapphire Blue
- Same sizing as Primary

**Tertiary Button**
- Background: Transparent
- Text: Sapphire Blue
- No border
- Hover: Light blue background (0.1 opacity)

**Icon Button**
- 40px × 40px square
- Center-aligned icon (24px)
- Background: Light gray on hover
- Border Radius: 8px

### Form Elements

**Input Field**
- Height: 40px
- Border: 1px solid #E2E8F0
- Border Radius: 8px
- Padding: 8px 12px
- Font: Inter 14px
- Focus: Blue border with shadow

**Dropdown/Select**
- Same styling as Input
- Chevron icon on right
- Dropdown menu: Light background, shadows

**Checkbox**
- 20px × 20px
- Sapphire Blue when checked
- Rounded corners

**Toggle Switch**
- 44px × 24px
- Green when ON
- Gray when OFF
- Smooth animation

**Text Area**
- Min height: 100px
- Resizable
- Same border styling as Input

### Cards

**Standard Card**
- Background: White (light mode), #1A202C (dark mode)
- Border: 1px #E2E8F0
- Border Radius: 12px
- Padding: 16px
- Shadow: md

**Elevated Card**
- Same as Standard
- Shadow: lg
- Used for interactive elements

**Image Card**
- Header image with 12px border radius top
- Content below image
- Overlay for images: Gradient overlay
- Text positioned absolutely over image (advanced variant)

## Navigation Patterns

### Web (Next.js)
- Top navbar: Fixed, 64px height
- Sidebar: Optional collapsible (dashboard)
- Breadcrumbs: For multi-level pages
- Footer: Full-width, dark background

### iOS (SwiftUI)
- Tab Bar: 5 tabs, icons + labels
- Navigation Stack: Smooth push/pop transitions
- Modals: Sheet presentations for secondary flows

### Android (Jetpack Compose)
- Bottom Navigation: 5 tabs
- Navigation Drawer: Hamburger menu
- Back Stack: Material Design transitions

## Page Hierarchy

### Public Pages (No Authentication Required)
1. Landing Page (`/`)
2. Pricing Page (`/pricing`)
3. Features Page (`/features`)
4. Blog (`/blog`, `/blog/:slug`)
5. Contact (`/contact`)
6. Privacy Policy (`/privacy`)
7. Terms of Service (`/terms`)

### Authentication Pages
- Sign Up (`/auth/signup`)
- Login (`/auth/login`)
- Forgot Password (`/auth/forgot-password`)
- Reset Password (`/auth/reset-password/:token`)
- Email Verification (`/auth/verify-email`)

### Authenticated Pages
- Dashboard (`/dashboard`)
- My Itineraries (`/itineraries`)
- Create Itinerary (`/itineraries/create`)
- View Itinerary (`/itineraries/:id`)
- Edit Itinerary (`/itineraries/:id/edit`)
- Bookings (`/bookings`)
- Saved Destinations (`/saved`)
- Profile Settings (`/settings/profile`)
- Account Settings (`/settings/account`)
- Preferences (`/settings/preferences`)

## Responsive Breakpoints

| Breakpoint | Width | Device | Usage |
|-----------|-------|--------|-------|
| xs | 320px | Mobile | Small phones |
| sm | 640px | Mobile | Standard phones |
| md | 768px | Tablet | Small tablets |
| lg | 1024px | Tablet/Desktop | Large tablets |
| xl | 1280px | Desktop | Desktop monitors |
| 2xl | 1536px | Desktop | Large monitors |

## Performance Targets

| Metric | Target |
|--------|--------|
| First Contentful Paint (FCP) | < 1.5s |
| Largest Contentful Paint (LCP) | < 2.5s |
| Cumulative Layout Shift (CLS) | < 0.1 |
| Time to Interactive (TTI) | < 3.5s |
| Mobile First Input Delay (FID) | < 100ms |
| Lighthouse Score | > 90 |

## Accessibility Standards

- **WCAG 2.1 Level AA** compliance
- Minimum contrast ratio: 4.5:1 for text
- All interactive elements: Keyboard accessible
- Screen reader support: Proper ARIA labels
- Focus indicators: Visible on all interactive elements
- Color not sole indicator: Icons + text for status

## Dark Mode Implementation

- System preference detection
- Toggle in settings
- Smooth transition animations
- Updated color palette:
  - Primary backgrounds: #0F172A
  - Secondary backgrounds: #1A202C
  - Text: #F8FAFC
  - Borders: #334155

---

**Last Updated:** 2026-11-13
**Version:** 1.0
