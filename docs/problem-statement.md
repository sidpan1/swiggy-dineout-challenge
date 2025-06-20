# Swiggy Dineout GenAI Co-Pilot Challenge

## Introduction

One of our key focus areas is building Agentic AI tools that improve internal workflows at scale. This challenge is centered around our Dineout vertical, which enables table bookings and dine-in experiences at scale across India.

The use case here is real, critical, and immediately impactful — helping Sales Executives and Account Managers who manage restaurant (Rx) partners.

## Who is the End User?

The primary users are Sales Executives and Account Managers working on the ground with restaurant partners across the country. Their goals include:
- Driving adoption of Ads and discounting programs
- Improving restaurant performance through data-backed conversations
- Recommending visibility, pricing, and promotional strategies to maximize RoI

These are fast-paced, field-heavy roles, where data access and insight readiness can make or break a pitch.

### The key metrics of the persona are:

| Metric | What It Is | How It's Measured | Why It Matters | How Sales Uses It |
|--------|------------|-------------------|----------------|-------------------|
| OPD (Orders per day) | Total number of confirmed table reservations | Count of completed bookings at a day level | Direct signal of demand and partner engagement | Shows growth or decline, helps justify Ads/discounts, and benchmark vs peers |
| Revenue / GOV | Estimated revenue from Swiggy bookings | Covers × Avg. spend per cover (or directly aggregated) | Reflects quality of traffic and partner profitability | Identifies high-potential partners, justifies upselling or campaign adjustments |
| Ads ROI | Return on investment from paid Ads | Revenue attributed to Ads / Ad Spend | Validates Ads effectiveness; key to campaign renewals | Used to pitch or diagnose Ads, counter objections, and recommend next steps |

## Current Challenges

Today, before any restaurant interaction, Sales Executives manually gather performance metrics across multiple dashboards and reports — bookings, ad performance, campaign ROI, peer comparisons, and discount effectiveness. This preparation takes up valuable time (30mins to 3 hours per restaurant), varies in quality, and isn't scalable across hundreds of partners per city.

There is an opportunity here to build a GenAI-powered Co-Pilot that can generate these insights automatically, reliably, and in a way that's tailored to each restaurant partner.

## Your Challenge

Build a prototype of an AI-powered Co-Pilot that generates a structured, contextual performance summary for a restaurant partner, based on a given restaurant_id.

This should be the kind of 1-pager a Sales Executive would review before a meeting or even send directly to the partner.

## What Should the Output Contain?

The Co-Pilot should generate a clear, concise, and actionable briefing that includes (not the exhaustive list):

1. **Restaurant's Recent Performance**
   - Bookings, cancellations, revenue, and average rating over the last 30 days
   - Notable changes or trends

2. **Ad Campaign Effectiveness**
   - Spend, impressions, clicks, conversions, and ROI
   - Any inefficiencies or highlights

3. **Peer Benchmarking**
   - Comparison with average metrics of similar restaurants in the same locality and cuisine
   - Areas where the restaurant is overperforming or underperforming

4. **Recommended Next Steps (Optional)**
   - Suggestions to improve performance (e.g., increase ad spend, adjust discounting, revisit campaign timing)

The final output should be structured in markdown or a simple narrative format — similar to how a human analyst might summarize the account.

## Input Format

- A single restaurant_id as input
- Mock or sample data may be used for:
  - Restaurant-level performance data (restaurant_metrics)
  - Ad campaign performance data (ads_data)
  - Peer benchmarks (peer_benchmarks)

## Tech Stack and Scope

- You may use any LLM or open-source stack you prefer (OpenAI, Claude, Mistral, LangChain, etc.)
- Retrieval-Augmented Generation (RAG), prompt chaining, or structured prompt design is welcome
- Usability, clarity and structure of output is important

## What We're Looking For

We're evaluating this as a proxy for how you'd approach real-world AI product development at Swiggy.

| Evaluation Criteria | What We're Looking For |
|-------------------|----------------------|
| Problem Solving | How well you structure the problem and define your approach |
| Quality of insights | 1. How useful and actionable are the insights generated<br>2. What is the level of abstraction of the insights |
| Tech | • Overall solution design and approach<br>• Ability to reason over data<br>• Potential Scalability of the solution<br>• Reusability of the modules as a capability |
| Product Thinking | Does this save the user time? Would they use this before every call? |
| Data Handling | Realism and quality of your sample data and metrics |
| Creativity and Craftsmanship | Attention to detail, clarity of output, and optional touches like highlighting anomalies or visual summaries |

## Deliverables

- A working prototype
- GitHub link with code, mocked datasets, and README
- 2–3 example outputs for different restaurants to showcase variation
- Notes on assumptions, prompt structure, and limitations
- (Optional) A 3–5 min video walkthrough

## Frequently Asked Questions (FAQ)

### 1. Do I need to use real data from Swiggy?
No. You are free to use mock data or generate synthetic datasets based on reasonable assumptions. We recommend creating 2–3 sample restaurants with variations in performance so your solution can demonstrate adaptability.

### 2. Which LLMs can I use?
You can use any model you prefer — OpenAI (GPT-4, GPT-3.5), Claude, Mistral, or open-source models like LLaMA 3. You are free to use hosted APIs or local inference, as long as it works with your environment and you document the setup.

### 3. Should the output be 100% accurate?
We're not judging this on perfect analytics accuracy. We're more interested in how well you model the problem, design the architecture, structure your data, and generate meaningful, context-rich summaries using LLMs. Bonus if you simulate uncertainty handling or low-confidence outputs.

### 4. What kind of recommendations should I include?
Recommendations should be data-informed. For example:
- "Increase ad spend by ₹1,000 to match peer average and improve visibility"
- "Optimize discount slab — peer ROI is 3.2x vs your 2.5x"

### 5. How much time should I spend on this?
We expect about 6–8 hours of effort, though you're free to spend more if you're enjoying it. Please don't over-engineer — we're not looking for production code, but rather problem clarity, creativity, and potential. The case study needs to be reverted in 2 days overall.

### 6. Can I include additional features?
Absolutely. If you have time and interest, feel free to add:
- Charts or visual summaries
- Interactive filters
- Slack-ready summaries
- Multi-restaurant batch generation

We love creativity — just be sure to clearly separate core requirements from bonus features.

### 7. How do I submit my solution?
- Share a GitHub repo link with your code, data, and instructions
- Include a few sample outputs
- (Optional) Add a Loom/YouTube walkthrough video (under 5 mins)
- Please ensure your repo is public or access-enabled

### 8. Can I ask questions during the challenge?
Yes — feel free to reach out via email if you hit blockers or need clarifications. We encourage curiosity and thoughtful questions.

## Sample Dataset

Here's a comprehensive list of datasets you would need to simulate and solve the Swiggy Dineout GenAI Co-Pilot challenge. These cover all core components: performance tracking, Ads campaigns, benchmarking, and optional discount analysis.

### Required Datasets for the Challenge

1. Each dataset can be created as a mock. Column-level suggestions are included.
2. Feel free to create synthetic data around the schemas shared
3. Please assume any other data required and create synthetic

### 1. restaurant_metrics

**Purpose:** Track restaurant-level performance over time  
**Granularity:** 1 row per restaurant per day

| Column Name | Description | Example |
|-------------|-------------|---------|
| restaurant_id | Unique identifier for the restaurant | R001 |
| restaurant_name | Display name of the restaurant | Spice Garden |
| locality | Area or neighborhood | Koramangala |
| cuisine | Cuisine category | Indian |
| date | Observation date | 2024-06-01 |
| bookings | Number of confirmed reservations | 12 |
| cancellations | Number of cancellations | 2 |
| covers | Total number of people who dined | 34 |
| avg_spend_per_cover | Avg ₹ value spent per customer | 500 |
| revenue | Total revenue (covers × spend) | 17,000 |
| avg_rating | Average user rating on platform | 4.3 |

### 2. ads_data

**Purpose:** Capture campaign performance metrics  
**Granularity:** 1 row per campaign per restaurant

| Column Name | Description | Example |
|-------------|-------------|---------|
| restaurant_id | Foreign key to identify restaurant | R001 |
| campaign_id | Unique campaign identifier | C101 |
| campaign_start | Start date of the ad campaign | 2024-05-01 |
| campaign_end | End date of the campaign | 2024-05-30 |
| impressions | Number of ad impressions | 30,000 |
| clicks | Number of clicks on the ad | 2,500 |
| conversions | Bookings attributed to ad | 210 |
| spend | Total ad spend (in ₹) | 5,000 |
| revenue_generated | Revenue from ad-attributed bookings | 18,500 |

### 3. peer_benchmarks

**Purpose:** Define average benchmarks by locality and cuisine  
**Granularity:** 1 row per locality + cuisine combination

| Column Name | Description | Example |
|-------------|-------------|---------|
| locality | Area name | Koramangala |
| cuisine | Cuisine category | Indian |
| avg_bookings | Avg bookings across peer restaurants | 150 |
| avg_conversion_rate | Avg booking rate from clicks | 8.0% |
| avg_ads_spend | Avg spend on ads | 5,500 |
| avg_roi | Avg ads ROI across peers | 2.8x |
| avg_revenue | Avg revenue per restaurant | ₹1,80,000 |
| avg_rating | Average user rating across peers | 4.1 |

## Optional (Advanced) Datasets

### 4. discount_history

**Purpose:** Track discount configurations and their impact  
**Granularity:** 1 row per restaurant per config duration

| Column Name | Description | Example |
|-------------|-------------|---------|
| restaurant_id | Foreign key to identify restaurant | R001 |
| start_date | Discount configuration start date | 2024-05-01 |
| end_date | End date for that config | 2024-05-31 |
| discount_type | Flat / tiered / combo | Tiered |
| discount_percent | Avg effective discount (%) | 10% |
| roi_from_discount | Estimated ROI from this config | 3.2x |

### 5. restaurant_master

**Purpose:** A master table for metadata joining (optional)  
**Granularity:** 1 row per restaurant

| Column Name | Description | Example |
|-------------|-------------|---------|
| restaurant_id | Unique ID | R001 |
| restaurant_name | Name | Spice Garden |
| city | City | Bangalore |
| onboarded_date | Date when restaurant joined | 2023-11-15 |