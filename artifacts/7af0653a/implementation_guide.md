# 🚀 Spice Garden Advertising Implementation Guide

## Immediate Actions (Next 24 Hours)

### 1. Campaign Optimization
```
✅ PAUSE these time slots immediately:
   - 11:00 PM - 11:00 AM (save ₹40/day)
   - All campaigns on Monday (lowest performer)

✅ INCREASE bids by 50% for:
   - 1:00 PM - 3:00 PM slot
   - 7:00 PM - 9:00 PM slot
   - Wednesday campaigns (best day)

✅ ADD negative keywords:
   - "free food"
   - "discount coupon"
   - "job vacancy"
   - "recipe"
```

### 2. Creative Updates

**Lunch Deals - New Copy:**
```
🔥 Only 3 tables left for 1 PM!
Spice Garden's Business Lunch Thali - ₹299
⭐ 4.2 rating | 1000+ happy diners
[Book Now - 2 min confirmation]
```

**Peak Hour Push - New Copy:**
```
🍴 Last Table Alert - 8 PM Tonight
Authentic Indian Fine Dining in Koramangala
Chef's Special: Paneer Makhani + Naan
[Reserve Now - Filling Fast]
```

### 3. Tracking Setup
```javascript
// Add to booking confirmation page
gtag('event', 'conversion', {
  'send_to': 'AW-XXXXXX/XXXXXX',
  'value': order_value,
  'currency': 'INR',
  'transaction_id': booking_id,
  'channel': utm_source,
  'time_slot': booking_time
});
```

## Week 1 Implementation

### Monday - Day 1
- [ ] Pause underperforming slots
- [ ] Create 3 ad variants for A/B testing
- [ ] Set up conversion tracking
- [ ] Implement bid adjustments

### Tuesday - Day 2
- [ ] Launch Peak Hour Push campaign
- [ ] Budget: ₹100/day test
- [ ] Monitor hourly performance
- [ ] Collect baseline metrics

### Wednesday - Day 3
- [ ] Analyze A/B test results
- [ ] Scale winning creative to 70%
- [ ] Increase Wednesday budget by 30%
- [ ] Setup retargeting audiences

### Thursday - Day 4
- [ ] Launch retargeting campaign
- [ ] Upload customer list (hash emails)
- [ ] Create lookalike audiences
- [ ] Test cart abandonment ads

### Friday - Day 5
- [ ] Prepare weekend special creatives
- [ ] Set up family package offers
- [ ] Schedule weekend bid increases
- [ ] Review week 1 performance

## Detailed Campaign Setups

### 1. Peak Hour Push Campaign

**Platform**: Google Ads + Facebook

**Targeting**:
```
📦 Demographics:
- Age: 25-45
- Income: Top 30%
- Interests: Fine dining, Indian cuisine

📍 Location:
- Primary: 2km radius of Koramangala
- Secondary: Indiranagar, Jayanagar
- Workplace: Electronic City, Whitefield (lunch only)

⏰ Schedule:
- Mon-Fri: 12:30-2:30 PM, 6:30-9:30 PM
- Sat-Sun: 12:00-3:00 PM, 6:00-10:00 PM
```

**Bidding Strategy**:
```
Target CPA: ₹6
Max bid: ₹12
Bid adjustments:
- Peak hours: +50%
- Mobile: +20%
- Previous visitors: +30%
```

### 2. Weekend Specials Campaign

**Offer Structure**:
```
🎉 Friday Night Special:
- 20% off for groups of 4+
- Complimentary dessert
- Priority seating

🌅 Weekend Brunch:
- Unlimited thali @ ₹499
- Kids eat free (under 10)
- 11 AM - 3 PM only

🌃 Saturday Date Night:
- Couple's special menu
- Candlelight ambiance
- 15% off total bill
```

### 3. Smart Retargeting Setup

**Audience Segments**:

1. **High-Value Abandoners** (Bid: +50%)
   - Viewed menu > 3 pages
   - Time on site > 2 minutes
   - Didn't complete booking

2. **Recent Diners** (Bid: +30%)
   - Visited in last 30 days
   - Rated 4+ stars
   - Exclude last 7 days

3. **Lapsed Customers** (Bid: +20%)
   - Visited 31-90 days ago
   - Special "We Miss You" offer

## Creative Templates

### 1. Carousel Ad Format
```
Slide 1: Hero dish image + logo
Slide 2: "Today's Special" + price
Slide 3: Interior ambiance shot
Slide 4: Customer testimonial
Slide 5: "Book Now" CTA + urgency
```

### 2. Video Ad Script (15 sec)
```
0-3s: Sizzling tandoor shot
3-6s: Chef plating signature dish
6-9s: Happy diners enjoying meal
9-12s: "Rated #1 Indian in Koramangala"
12-15s: "Book Now - Tables Filling Fast"
```

### 3. Stories Format
```
Frame 1: Question poll "Spicy or Mild?"
Frame 2: Behind-the-scenes kitchen
Frame 3: Today's special reveal
Frame 4: Swipe up to book
```

## Budget Tracking Dashboard

### Daily Metrics Template
```markdown
## Date: [DATE]

### Campaign Performance
| Campaign | Spend | Bookings | Revenue | ROI | CPA |
|----------|-------|----------|---------|-----|-----|
| Peak Hour | ₹XXX | XX | ₹X,XXX | XX.Xx | ₹XX |
| Lunch Deals | ₹XXX | XX | ₹X,XXX | XX.Xx | ₹XX |
| Weekend | ₹XXX | XX | ₹X,XXX | XX.Xx | ₹XX |
| Retarget | ₹XXX | XX | ₹X,XXX | XX.Xx | ₹XX |

### Hour-wise Performance
| Hour | Clicks | Bookings | Conv% | Avg Check |
|------|--------|----------|-------|----------|
| 12-1 | XXX | XX | XX% | ₹XXX |
| 1-2 | XXX | XX | XX% | ₹XXX |
| 7-8 | XXX | XX | XX% | ₹XXX |
| 8-9 | XXX | XX | XX% | ₹XXX |

### Action Items
- [ ] Winning creative: [NAME]
- [ ] Underperformer to pause: [NAME]
- [ ] Tomorrow's focus: [STRATEGY]
```

## Platform-Specific Settings

### Google Ads
```
Campaign Type: Search + Display
Bidding: Target CPA
Ad Rotation: Optimize for conversions
Frequency Cap: 3 per day
Exclusions: Competitor brand terms
```

### Facebook/Instagram
```
Objective: Conversions (Table Bookings)
Optimization: Booking Completions
Placement: Automatic (monitor performance)
Frequency Cap: 2 per 3 days
Exclude: Recent bookers (7 days)
```

### Swiggy Dineout Platform
```
Boost Type: Premium listing
Time Slots: Peak hours only
Offer Type: Time-based discounts
Visibility: Category + Search
Budget: 20% of total ad spend
```

## Success Checklist

### Daily Tasks
- [ ] Check ROI dashboard at 10 AM
- [ ] Adjust bids based on performance
- [ ] Pause underperforming keywords
- [ ] Update creative if CTR < 5%
- [ ] Monitor competitor activities

### Weekly Tasks
- [ ] Review search term report
- [ ] Update negative keyword list
- [ ] Refresh ad creatives
- [ ] Analyze conversion paths
- [ ] Plan next week's offers

### Monthly Tasks
- [ ] Full ROI analysis
- [ ] Customer LTV calculation
- [ ] Competitive analysis
- [ ] Budget reallocation
- [ ] Strategy presentation

## Troubleshooting Guide

### If ROI drops below 8x:
1. Check time-of-day performance
2. Review search terms for irrelevant clicks
3. Test new creative immediately
4. Reduce bids by 20% temporarily

### If conversions drop:
1. Verify tracking code
2. Check website speed
3. Review booking process
4. Test offer relevance

### If CPA increases:
1. Pause broad keywords
2. Tighten geographic targeting
3. Increase quality score focus
4. Review landing page experience

## Contact & Support

**Campaign Manager**: Swiggy Dineout Ads Team
**Slack Channel**: #spice-garden-advertising
**Weekly Review**: Every Monday 3 PM
**Emergency**: If ROI < 5x or spend > ₹500/day

---

*Last Updated: 2025-06-29*
*Next Review: Week 1 Performance*