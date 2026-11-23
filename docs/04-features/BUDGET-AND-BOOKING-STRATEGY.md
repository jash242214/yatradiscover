# YatraDiscover AI - Budget & Booking Strategy

## Overview

YatraDiscover AI focuses on providing **best value recommendations** to travelers without managing direct bookings. The platform acts as a smart discovery and comparison engine that directs users to trusted external booking partners.

## 1. Budget Optimization Strategy

### 1.1 Hotel Budget Recommendations

#### Best Value Algorithm
```
Value Score = (Overall Rating / Average Price) × 100

Example:
- Hotel A: Rating 4.5, Price $80/night → Score = (4.5/80) × 100 = 5.625
- Hotel B: Rating 4.0, Price $50/night → Score = (4.0/50) × 100 = 8.0 (Best Value)
```

#### Budget Categories
| Category | Price Range | Target Users |
|----------|------------|--------------|
| Economy | $0-50 | Budget travelers |
| Budget | $50-100 | Value-conscious |
| Midrange | $100-250 | Comfort seekers |
| Upscale | $250-500 | Premium experience |
| Luxury | $500+ | High-end travelers |

#### Key Features
- **Minimum Rating Filter**: Only show hotels ≥3.5 stars (quality assurance)
- **Price Filtering**: User can set min/max budget
- **Amenities Filter**: Include/exclude desired facilities
- **Star Rating Filter**: 1-5 star properties

### 1.2 Restaurant Budget Recommendations

#### Value Scoring
```
Value Score = Overall Rating / Price Level Numeric

Price Level Mapping:
- "$" = 1   (Budget)
- "$$" = 2  (Moderate)
- "$$$" = 3 (Upscale)
- "$$$$" = 4 (Fine Dining)

Example:
- Restaurant A: Rating 4.5, Price "$$$$" → Score = 4.5/4 = 1.125
- Restaurant B: Rating 4.0, Price "$$" → Score = 4.0/2 = 2.0 (Best Value)
```

#### Dining Occasion Profiles
| Occasion | Price Levels | Atmosphere | Example |
|----------|-------------|-----------|---------|
| Casual | $, $$ | Relaxed | Street food, cafes |
| Date Night | $$$, $$$$ | Romantic | Fine dining, wine bars |
| Business | $$, $$$, $$$$ | Professional | Upscale restaurants |
| Family | $, $$, $$$ | Family-friendly | Diverse menus |

### 1.3 Attraction Budget Recommendations

#### Cost-Benefit Model
```
Priority:
1. Free attractions (highest value)
2. Low-cost attractions (<max_price) with high ratings
3. Skip high-cost attractions if user budget-conscious
```

#### Duration-Based Recommendations
```
Available Time  | Suggested Attractions
1-2 hours       | Quick-visit spots, nearby attractions
2-4 hours       | Half-day activities
4-8 hours       | Full-day experiences
8+ hours        | All-day tours and activities
```

---

## 2. Booking & Partnership Strategy

### 2.1 No Direct Booking Management

**Policy**: YatraDiscover never manages bookings, payments, or cancellations.

**Why**:
- Reduces liability and compliance complexity
- Users book directly with trusted providers
- Better for user trust (direct relationships)
- Simpler tech stack and operations
- Aligns with discovery-focused model

### 2.2 Affiliate & Partner Links

#### Hotel Booking Partners
| Partner | Coverage | Link Format |
|---------|----------|-------------|
| Booking.com | Global | `https://www.booking.com/hotel/{booking_id}.html` |
| Google Hotels | Global | `https://www.google.com/travel/hotels/{google_id}` |
| OTA Local* | Regional | Country-specific booking sites |
| Hotel Direct | Premium | Official hotel website |

*Regional OTA Examples:
- **India**: MMT (MakeMyTrip), Goibibo, Cleartrip
- **Southeast Asia**: Agoda, Traveloka
- **Europe**: Expedia, Trivago
- **China**: Ctrip, Elong

#### Restaurant Booking Partners
| Partner | Link Type | Format |
|---------|----------|--------|
| Reservation Sites | Dining reservation | Resy, OpenTable, TripAdvisor |
| Maps Integration | Direct search | Google Maps, Apple Maps |
| Restaurant Direct | Official booking | Restaurant website |

#### Attraction Booking Partners
| Partner | Link Type | Coverage |
|---------|----------|----------|
| Official Sites | Direct booking | Most attractions |
| Ticketing Platforms | Online tickets | GetYourGuide, Klook, Viator |
| Local Partners | Regional tickets | Local city guides |

### 2.3 Booking Link Structure

#### Database Schema
```sql
sources JSONB = {
  "booking": "hotel_id_12345",
  "google": "google_place_id_xyz",
  "agoda": "agoda_id_98765",
  "hotel_direct": "https://www.hotelwebsite.com"
}

booking_url VARCHAR = "https://www.booking.com/hotel/..."
```

#### Response Format
```json
{
  "hotel_id": "uuid",
  "name": "Hotel Paradise",
  "city": "Bali",
  "booking_links": {
    "booking.com": "https://www.booking.com/hotel/...",
    "google_hotels": "https://www.google.com/travel/hotels/...",
    "agoda": "https://www.agoda.com/...",
    "hotel_direct": "https://hotelparadise.com/booking"
  }
}
```

### 2.4 User Journey - No Direct Booking

```
1. User searches for hotels in Mumbai
   ↓
2. YatraDiscover returns recommendations
   - Top 5 best value hotels (smart ranking)
   - Hotel details, reviews, ratings, photos
   - Booking links to external sites
   ↓
3. User clicks "Book on Booking.com" (external link)
   ↓
4. User completes booking on Booking.com
   - YatraDiscover is NOT involved in booking
   - User directly manages reservation
   - User confirms/cancels/modifies on booking site
   ↓
5. User travels and stays at hotel
   - Direct relationship with hotel/booking site
   - YatraDiscover can still serve post-trip (reviews, tips)
```

---

## 3. Revenue Model (Optional Future)

### 3.1 Affiliate Commission
```
Partner Sites (Current):
- Booking.com: ~5-15% commission
- Agoda: ~8-12% commission
- Google Hotels: Variable
- Viator/GetYourGuide: 5-20% commission

Model: YatraDiscover gets commission when user books through affiliate link
```

### 3.2 Premium Features (No Impact on Bookings)
```
Free Tier:
- Basic search
- Public reviews
- Standard recommendations

Premium Tier:
- Advanced filters
- Price alerts
- Saved trips
- Personalized recommendations
- Exclusive deals
```

---

## 4. Technical Implementation

### 4.1 API Response with Booking Links

```python
# HotelSearchResponse
{
  "id": "uuid",
  "name": "Hotel Paradise",
  "city": "Bali",
  "country": "Indonesia",
  "overall_rating": 4.5,
  "avg_price": 150,
  "lowest_price": 120,
  "currency": "USD",
  "booking_url": "https://booking.com/...",
  "booking_links": {
    "booking.com": "https://www.booking.com/...",
    "agoda": "https://www.agoda.com/...",
    "google_hotels": "https://www.google.com/...",
    "hotel_direct": "https://hotelparadise.com/"
  }
}
```

### 4.2 Service Layer Integration

```python
# HotelSearchService
def get_best_value_hotels(city, country, limit=10):
    # 1. Find hotels matching criteria
    hotels = db.query(Hotel).filter(...).all()
    
    # 2. Calculate value scores (rating/price ratio)
    scored_hotels = [(h, score(h)) for h in hotels]
    
    # 3. Sort by score descending
    scored_hotels.sort(key=lambda x: x[1], reverse=True)
    
    # 4. Get top N and add booking links
    results = []
    for hotel, score in scored_hotels[:limit]:
        response = HotelSearchResponse.from_orm(hotel)
        response.booking_links = _get_booking_links(hotel)
        results.append(response)
    
    return results

def _get_booking_links(hotel):
    # Build links from sources JSONB and booking_url
    links = {}
    if hotel.booking_url:
        links["booking.com"] = hotel.booking_url
    # ... add other partner links
    return links
```

### 4.3 Frontend Integration

```typescript
// React Component
function HotelCard({ hotel }) {
  return (
    <div className="hotel-card">
      <h3>{hotel.name}</h3>
      <p>Rating: {hotel.overall_rating}/5</p>
      <p>Price: ${hotel.avg_price}/night</p>
      
      {/* NO booking form here! */}
      
      {/* Instead, external links */}
      <div className="booking-links">
        {Object.entries(hotel.booking_links).map(([site, url]) => (
          <a 
            key={site}
            href={url}
            target="_blank"
            rel="noopener noreferrer"
          >
            Book on {site}
          </a>
        ))}
      </div>
    </div>
  );
}
```

---

## 5. Best Value Recommendations Examples

### 5.1 Hotel Example - Mumbai

#### Search Parameters
- City: Mumbai
- Budget: $0-150/night
- Min Rating: 3.5 stars
- Check-in: 2024-02-15
- Check-out: 2024-02-17

#### Best Value Hotels (Ranked by Value Score)

| # | Hotel | Rating | Price | Value Score | Booking Links |
|---|-------|--------|-------|-------------|---|
| 1 | Budget Inn Mumbai | 4.2 | $65 | 6.46 | [Booking.com] [Google] |
| 2 | Star Hotel | 4.5 | $120 | 3.75 | [Booking.com] [Agoda] |
| 3 | Grand Central | 4.0 | $145 | 2.76 | [Booking.com] [Direct] |

**Recommendation**: Budget Inn Mumbai offers the best value for money.

### 5.2 Restaurant Example - Barcelona

#### Search Parameters
- City: Barcelona
- Occasion: Date Night
- Budget: $$$ (mid-to-upscale)
- Cuisine: Spanish
- Dietary: None

#### Recommendations

| # | Restaurant | Cuisine | Price | Rating | Value Score | Link |
|---|-----------|---------|-------|--------|-------------|------|
| 1 | Casa Batlló | Spanish | $$$ | 4.6 | 1.53 | [Resy] [Direct] |
| 2 | Michelin Star | Spanish | $$$$ | 4.8 | 1.20 | [OpenTable] [Direct] |
| 3 | Tapas Bar | Spanish | $$ | 4.3 | 2.15 | [TripAdvisor] |

**Recommendation**: Tapas Bar offers excellent Spanish cuisine with best value at moderate price.

### 5.3 Attraction Example - Paris

#### Search Parameters
- City: Paris
- Duration: 4 hours
- Budget: $0-50
- Wheelchair Accessible: Yes

#### Recommendations

| # | Attraction | Type | Entry Fee | Rating | Duration |
|---|-----------|------|----------|--------|----------|
| 1 | Eiffel Tower | Monument | $20 | 4.4 | 2-3h | [GetYourGuide] |
| 2 | Louvre Museum | Museum | $17 | 4.5 | 3-4h | [Official] |
| 3 | Seine River Walk | Park | Free | 4.2 | 1-2h | [Maps] |

**Recommendation**: Free Seine walk + affordable Louvre entry provides full 4-hour experience.

---

## 6. Quality Assurance

### 6.1 Data Validation
- Minimum rating threshold (3.5+ stars)
- Verified reviews from trusted sources
- Active/current listings only
- Valid contact information

### 6.2 Partner Verification
- Only list established, trustworthy booking partners
- Regular link validation (no broken links)
- Monitor partner performance and user satisfaction

### 6.3 User Feedback
- Allow rating of recommendations
- Track booking completion rates
- Gather feedback on accuracy
- Iterate algorithm based on feedback

---

## 7. Regulatory Compliance

### 7.1 Affiliate Disclosures
- Clear disclosure when links are affiliate links
- Transparent about commission model (if applicable)
- User consent for data usage

### 7.2 User Data Protection
- GDPR compliant for EU users
- Data privacy for India and other regions
- Secure handling of user preferences
- No sharing of user data with booking partners

### 7.3 Fraud Prevention
- Monitor for suspicious patterns
- Validate user identity when needed
- Track and report fraudulent bookings to partners

---

## 8. Implementation Roadmap

### Phase 2A (Weeks 3-4): Core Discovery
- ✅ Hotel models and migrations
- ✅ Hotel service with best value algorithm
- ✅ Hotel API endpoints with booking links
- API testing with sample data

### Phase 2B (Week 5): Restaurants & Attractions
- Restaurant search service
- Attraction discovery service
- Restaurant and attraction API endpoints

### Phase 3 (Week 6+): Advanced Features
- Recommendation scoring engine
- User preference personalization
- Price trend analysis and alerts
- Seasonal recommendations

---

## Appendix: API Examples

### Search Hotels with Budget Filter
```bash
curl -X POST http://localhost:8000/api/v2/hotels/search \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Mumbai",
    "country": "India",
    "min_price": 50,
    "max_price": 150,
    "min_rating": 3.5,
    "sort_by": "value_score",
    "limit": 10
  }'
```

### Get Best Value Hotels
```bash
curl http://localhost:8000/api/v2/hotels/best-value?city=Mumbai&country=India&limit=5
```

### Get Hotel Details with Booking Links
```bash
curl http://localhost:8000/api/v2/hotels/uuid/details
```

Response includes `booking_links` field with all partner URLs.

---

## Conclusion

YatraDiscover's budget recommendation strategy focuses on:

1. **Smart Algorithms**: Best value scores based on rating/price ratios
2. **Quality Assurance**: Minimum ratings and verified reviews
3. **User-Centric**: Personalization based on preferences and budgets
4. **Partner Integration**: External booking links, no direct booking
5. **Transparency**: Clear pricing, ratings, and recommendations

This approach provides maximum value to travelers while maintaining simplicity and trust.
