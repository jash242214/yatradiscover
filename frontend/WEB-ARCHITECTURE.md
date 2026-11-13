# Website Architecture - Next.js Implementation

## Tech Stack

```
Frontend Framework: Next.js 14+ (App Router)
Language: TypeScript
Styling: Tailwind CSS + CSS Modules
UI Components: Shadcn/ui (customized)
State Management: Zustand + TanStack Query
Forms: React Hook Form + Zod validation
Icons: Lucide React / Heroicons
Animation: Framer Motion
Maps: Mapbox GL / Google Maps
Testing: Vitest + React Testing Library
Linting: ESLint + Prettier
Package Manager: npm / pnpm
```

## Project Structure

```
frontend/web/
├── public/
│   ├── images/
│   │   ├── hero/
│   │   ├── destinations/
│   │   ├── logos/
│   │   └── icons/
│   ├── fonts/
│   └── favicon.ico
│
├── src/
│   ├── app/
│   │   ├── (public)/
│   │   │   ├── page.tsx (Landing)
│   │   │   ├── pricing/page.tsx
│   │   │   ├── features/page.tsx
│   │   │   ├── blog/page.tsx
│   │   │   ├── blog/[slug]/page.tsx
│   │   │   ├── contact/page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── (auth)/
│   │   │   ├── signup/page.tsx
│   │   │   ├── login/page.tsx
│   │   │   ├── forgot-password/page.tsx
│   │   │   ├── reset-password/[token]/page.tsx
│   │   │   ├── verify-email/page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── (dashboard)/
│   │   │   ├── dashboard/page.tsx
│   │   │   ├── itineraries/page.tsx
│   │   │   ├── itineraries/create/page.tsx
│   │   │   ├── itineraries/[id]/page.tsx
│   │   │   ├── itineraries/[id]/edit/page.tsx
│   │   │   ├── bookings/page.tsx
│   │   │   ├── saved/page.tsx
│   │   │   ├── settings/profile/page.tsx
│   │   │   ├── settings/account/page.tsx
│   │   │   ├── settings/preferences/page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── api/
│   │   │   ├── auth/[...nextauth]/route.ts
│   │   │   ├── itineraries/route.ts
│   │   │   ├── bookings/route.ts
│   │   │   ├── user/route.ts
│   │   │   └── webhook/stripe/route.ts
│   │   │
│   │   ├── layout.tsx (Root)
│   │   ├── page.tsx (Server Component Redirect)
│   │   └── globals.css
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Loading.tsx
│   │   │   ├── Error.tsx
│   │   │   └── NotFound.tsx
│   │   │
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Toast.tsx
│   │   │   ├── Dropdown.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Tabs.tsx
│   │   │   ├── Checkbox.tsx
│   │   │   ├── Toggle.tsx
│   │   │   ├── Slider.tsx
│   │   │   ├── Tooltip.tsx
│   │   │   └── Skeleton.tsx
│   │   │
│   │   ├── landing/
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── CTA.tsx
│   │   │   ├── Pricing.tsx
│   │   │   └── FAQ.tsx
│   │   │
│   │   ├── auth/
│   │   │   ├── SignupForm.tsx
│   │   │   ├── LoginForm.tsx
│   │   │   ├── PasswordReset.tsx
│   │   │   └── EmailVerification.tsx
│   │   │
│   │   ├── itinerary/
│   │   │   ├── ItineraryCard.tsx
│   │   │   ├── ItineraryList.tsx
│   │   │   ├── ItineraryDetail.tsx
│   │   │   ├── ItineraryEditor.tsx
│   │   │   ├── DayPlanner.tsx
│   │   │   ├── ActivityItem.tsx
│   │   │   └── Map.tsx
│   │   │
│   │   ├── ai/
│   │   │   ├── AIChat.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   ├── SuggestionCard.tsx
│   │   │   └── LoadingAnimation.tsx
│   │   │
│   │   └── dashboard/
│   │       ├── StatsCard.tsx
│   │       ├── RecentItineraries.tsx
│   │       ├── UpcomingTrips.tsx
│   │       └── Analytics.tsx
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useItinerary.ts
│   │   ├── useAI.ts
│   │   ├── useBooking.ts
│   │   ├── useDarkMode.ts
│   │   ├── useGeolocation.ts
│   │   └── useWindowSize.ts
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── auth.ts
│   │   │   ├── itineraries.ts
│   │   │   ├── bookings.ts
│   │   │   └── ai.ts
│   │   │
│   │   ├── utils/
│   │   │   ├── cn.ts (classname merger)
│   │   │   ├── format.ts (date, currency formatting)
│   │   │   ├── validation.ts
│   │   │   ├── storage.ts (localStorage wrapper)
│   │   │   └── constants.ts
│   │   │
│   │   ├── db/
│   │   │   ├── supabase.ts
│   │   │   └── queries.ts (pre-built queries)
│   │   │
│   │   └── types/
│   │       ├── index.ts
│   │       ├── user.ts
│   │       ├── itinerary.ts
│   │       ├── booking.ts
│   │       ├── activity.ts
│   │       └── api.ts
│   │
│   ├── styles/
│   │   ├── globals.css
│   │   ├── variables.css
│   │   ├── tailwind.config.ts
│   │   └── theme/
│   │       ├── dark.css
│   │       └── light.css
│   │
│   ├── context/
│   │   ├── AuthContext.tsx
│   │   ├── ThemeContext.tsx
│   │   └── NotificationContext.tsx
│   │
│   ├── store/
│   │   ├── authStore.ts (Zustand)
│   │   ├── itineraryStore.ts
│   │   ├── bookingStore.ts
│   │   └── uiStore.ts
│   │
│   ├── middleware.ts (NextAuth, redirects)
│   │
│   └── env.ts (Environment validation)
│
├── .env.local.example
├── next.config.js
├── tsconfig.json
├── tailwind.config.ts
├── eslint.config.js
├── prettier.config.js
├── package.json
├── pnpm-lock.yaml
└── README.md
```

## Key Features Implementation

### 1. Authentication Flow
- NextAuth.js with email + OAuth (Google, GitHub)
- JWT tokens stored in secure HTTP-only cookies
- Refresh token rotation
- Role-based access control (User, Admin, Partner)

### 2. Itinerary Management
- Create, read, update, delete operations
- Real-time collaboration with WebSockets
- Version history and undo/redo
- Export to PDF/CSV

### 3. AI Integration
- Streaming responses from OpenAI API
- Context-aware suggestions
- Real-time typing indicator
- Message history persistence

### 4. Booking System
- Integration with payment provider (Stripe)
- Multi-currency support
- Refund handling
- Email confirmations

### 5. Maps & Geolocation
- Interactive map view
- Route optimization
- Distance calculation
- Location search with autocomplete

### 6. Performance Optimization
- Image optimization with Next.js Image
- Code splitting with dynamic imports
- Route prefetching
- Server-side rendering for public pages
- Static generation for blog posts

### 7. Search & Filtering
- Full-text search on destinations
- Advanced filters (budget, duration, activity type)
- Search history
- Saved searches

## Component Library

### Common Components

**Header**
- Logo with link to home
- Navigation menu (desktop)
- Hamburger menu (mobile)
- User menu with dropdown
- Dark mode toggle

**Footer**
- Company info
- Quick links
- Social media icons
- Newsletter signup
- Copyright

**Navbar (Dashboard)**
- Breadcrumb navigation
- Search bar
- Notifications bell
- User avatar

**Sidebar (Dashboard)**
- Menu items with icons
- Collapse animation
- Active state indicator
- Logout button

### Form Components

**Input Field**
- Label with optional required indicator
- Placeholder text
- Error message display
- Helper text
- Icon support (prefix/suffix)

**Select Field**
- Searchable dropdown
- Multi-select option
- Group support
- Async loading

**Date Picker**
- Calendar modal
- Date range selection
- Time picker (optional)
- Keyboard navigation

**File Upload**
- Drag and drop
- File preview
- Progress bar
- Multiple file support

### Data Display

**Table**
- Sortable columns
- Row selection (checkbox)
- Pagination
- Responsive scroll on mobile

**List**
- Infinite scroll option
- Skeleton loading states
- Empty state UI
- Dividers between items

## Styling Strategy

### Tailwind CSS + CSS Modules

```typescript
// Component with utility classes
export const Button = ({ variant = 'primary' }) => (
  <button className={cn(
    'px-4 py-2 rounded-lg font-medium transition-colors',
    variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
    variant === 'secondary' && 'border border-blue-600 text-blue-600'
  )}>
    Click me
  </button>
)
```

### Dark Mode

```typescript
// In Tailwind config
darkMode: 'class',

// Usage
export const Card = () => (
  <div className="bg-white dark:bg-slate-900">
    Content
  </div>
)
```

## API Integration

### Base Configuration

```typescript
// lib/api/client.ts
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptors for auth token refresh
```

### Endpoints Map

```
Authentication:
  POST /api/auth/signup
  POST /api/auth/login
  POST /api/auth/logout
  POST /api/auth/refresh
  
Itineraries:
  GET /api/itineraries
  POST /api/itineraries
  GET /api/itineraries/:id
  PUT /api/itineraries/:id
  DELETE /api/itineraries/:id
  
AI:
  POST /api/ai/suggest
  POST /api/ai/chat
  GET /api/ai/suggestions/:itineraryId
  
Bookings:
  GET /api/bookings
  POST /api/bookings
  GET /api/bookings/:id
  PUT /api/bookings/:id/cancel
  
User:
  GET /api/user/profile
  PUT /api/user/profile
  GET /api/user/preferences
  PUT /api/user/preferences
```

## Testing Strategy

### Unit Tests (Vitest)
```typescript
// components/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react'
import { Button } from '../Button'

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
})
```

### Integration Tests
- API route testing
- Form submission flows
- Authentication workflows

### E2E Tests (Cypress/Playwright)
- User registration flow
- Itinerary creation
- Booking process
- Payment flow

## Deployment Configuration

### Environment Variables

```env
NEXT_PUBLIC_API_URL=https://api.yatradiscover.com
NEXT_PUBLIC_MAPBOX_TOKEN=pk_...
NEXTAUTH_SECRET=<generated>
NEXTAUTH_URL=https://yatradiscover.com
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk_...
STRIPE_PUBLIC_KEY=pk_...
STRIPE_SECRET_KEY=sk_...
```

### Build & Deploy

```bash
# Build
npm run build

# Test
npm run test

# Deploy (Vercel)
vercel deploy --prod
```

---

**Last Updated:** 2026-11-13
**Status:** Ready for development
