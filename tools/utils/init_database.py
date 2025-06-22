#!/usr/bin/env python3
"""
Swiggy Dineout GenAI Co-Pilot Challenge - Database Initialization Script

This script initializes a SQLite database with 12 consolidated tables and 
comprehensive mock data for the restaurant performance analytics system.
Features strategic table consolidation with 4,180+ realistic records across
enhanced core tables and extended business intelligence tables.
"""

import sqlite3
import logging
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseInitializer:
    def __init__(self, db_path: str = "swiggy_dineout.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON")
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def create_tables(self):
        """Create all required tables based on the schema"""
        logger.info("Creating database tables...")
        
        # Restaurant Master Table (Enhanced with profile extensions)
        restaurant_master_sql = '''
        CREATE TABLE IF NOT EXISTS restaurant_master (
            restaurant_id TEXT PRIMARY KEY,
            restaurant_name TEXT NOT NULL,
            city TEXT NOT NULL,
            locality TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            onboarded_date DATE NOT NULL,
            veg_nonveg_type TEXT NOT NULL CHECK(veg_nonveg_type IN ('Veg', 'Non-Veg', 'Both')),
            online_order_enabled BOOLEAN NOT NULL DEFAULT 0,
            establishment_date DATE NOT NULL,
            exclusivity_status TEXT NOT NULL CHECK(exclusivity_status IN ('Exclusive', 'Non-Exclusive')),
            parent_type TEXT NOT NULL CHECK(parent_type IN ('Franchise', 'Brand-Owned', 'Independent')),
            seating_capacity INTEGER NOT NULL DEFAULT 0,
            nps_score REAL CHECK(nps_score >= -100 AND nps_score <= 100)
        )
        '''
        
        # Restaurant Metrics Table (Enhanced schema with business columns)
        restaurant_metrics_sql = '''
        CREATE TABLE IF NOT EXISTS restaurant_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id TEXT NOT NULL,
            restaurant_name TEXT NOT NULL,
            locality TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            date DATE NOT NULL,
            bookings INTEGER NOT NULL DEFAULT 0,
            cancellations INTEGER NOT NULL DEFAULT 0,
            covers INTEGER NOT NULL DEFAULT 0,
            avg_spend_per_cover REAL NOT NULL DEFAULT 0.0,
            revenue REAL NOT NULL DEFAULT 0.0,
            avg_rating REAL CHECK(avg_rating >= 1.0 AND avg_rating <= 5.0),
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id),
            UNIQUE(restaurant_id, date)
        )
        '''
        
        # Ads Data Table (Enhanced with financial details)
        ads_data_sql = '''
        CREATE TABLE IF NOT EXISTS ads_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id TEXT NOT NULL,
            campaign_id TEXT NOT NULL,
            campaign_start DATE NOT NULL,
            campaign_end DATE NOT NULL,
            impressions INTEGER NOT NULL DEFAULT 0,
            clicks INTEGER NOT NULL DEFAULT 0,
            conversions INTEGER NOT NULL DEFAULT 0,
            spend REAL NOT NULL DEFAULT 0.0,
            revenue_generated REAL NOT NULL DEFAULT 0.0,
            total_investment REAL NOT NULL DEFAULT 0.0,
            fund_consumption_rate REAL NOT NULL DEFAULT 0.0,
            yoy_funding_change REAL NOT NULL DEFAULT 0.0,
            mom_funding_change REAL NOT NULL DEFAULT 0.0,
            campaign_category TEXT NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id),
            UNIQUE(restaurant_id, campaign_id)
        )
        '''
        
        # Peer Benchmarks Table (Enhanced schema maintaining ID)
        peer_benchmarks_sql = '''
        CREATE TABLE IF NOT EXISTS peer_benchmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            locality TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            avg_bookings REAL NOT NULL DEFAULT 0.0,
            avg_conversion_rate REAL NOT NULL DEFAULT 0.0,
            avg_ads_spend REAL NOT NULL DEFAULT 0.0,
            avg_roi REAL NOT NULL DEFAULT 0.0,
            avg_revenue REAL NOT NULL DEFAULT 0.0,
            avg_rating REAL NOT NULL DEFAULT 0.0,
            UNIQUE(locality, cuisine)
        )
        '''
        
        # Discount History Table (Enhanced schema maintaining ID)
        discount_history_sql = '''
        CREATE TABLE IF NOT EXISTS discount_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            discount_type TEXT NOT NULL,
            discount_percent REAL NOT NULL,
            roi_from_discount REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id)
        )
        '''
        
        # EXTENDED TABLES - Advanced Business Intelligence Requirements
        
        # Operational Metrics Table
        operational_metrics_sql = '''
        CREATE TABLE IF NOT EXISTS operational_metrics (
            restaurant_id TEXT NOT NULL,
            date DATE NOT NULL,
            hour_slot INTEGER NOT NULL CHECK(hour_slot >= 0 AND hour_slot <= 23),
            capacity_utilization REAL NOT NULL DEFAULT 0.0 CHECK(capacity_utilization >= 0 AND capacity_utilization <= 100),
            overbooking_incidents INTEGER NOT NULL DEFAULT 0,
            underbooking_slots INTEGER NOT NULL DEFAULT 0,
            online_bookings INTEGER NOT NULL DEFAULT 0,
            offline_bookings INTEGER NOT NULL DEFAULT 0,
            service_delay_minutes REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id),
            UNIQUE(restaurant_id, date, hour_slot)
        )
        '''
        
        # Service Quality Tracking Table
        service_quality_tracking_sql = '''
        CREATE TABLE IF NOT EXISTS service_quality_tracking (
            restaurant_id TEXT NOT NULL,
            date DATE NOT NULL,
            reviews_count INTEGER NOT NULL DEFAULT 0,
            avg_service_rating REAL CHECK(avg_service_rating >= 1.0 AND avg_service_rating <= 5.0),
            complaints_count INTEGER NOT NULL DEFAULT 0,
            complaint_categories TEXT,
            resolution_time_hours REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id),
            UNIQUE(restaurant_id, date)
        )
        '''
        
        
        # Financial Settlements Table
        financial_settlements_sql = '''
        CREATE TABLE IF NOT EXISTS financial_settlements (
            restaurant_id TEXT NOT NULL,
            settlement_date DATE NOT NULL,
            settlement_amount REAL NOT NULL DEFAULT 0.0,
            settlement_type TEXT NOT NULL CHECK(settlement_type IN ('Commission', 'Refund', 'Penalty', 'Bonus')),
            processing_time_days INTEGER NOT NULL DEFAULT 0,
            outstanding_amount REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id)
        )
        '''
        
        # Competitive Intelligence Table
        competitive_intelligence_sql = '''
        CREATE TABLE IF NOT EXISTS competitive_intelligence (
            locality TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            capacity_range TEXT NOT NULL CHECK(capacity_range IN ('Small (1-30)', 'Medium (31-80)', 'Large (81+)')),
            competitor_count INTEGER NOT NULL DEFAULT 0,
            market_share_estimate REAL NOT NULL DEFAULT 0.0 CHECK(market_share_estimate >= 0 AND market_share_estimate <= 100),
            avg_competitor_rating REAL CHECK(avg_competitor_rating >= 1.0 AND avg_competitor_rating <= 5.0),
            price_positioning TEXT NOT NULL CHECK(price_positioning IN ('Premium', 'Mid-Range', 'Budget')),
            competitive_advantage_score REAL NOT NULL DEFAULT 0.0 CHECK(competitive_advantage_score >= 0 AND competitive_advantage_score <= 10),
            UNIQUE(locality, cuisine, capacity_range)
        )
        '''
        
        # Revenue Volatility Tracking Table
        revenue_volatility_tracking_sql = '''
        CREATE TABLE IF NOT EXISTS revenue_volatility_tracking (
            restaurant_id TEXT NOT NULL,
            date DATE NOT NULL,
            revenue_volatility_index REAL NOT NULL DEFAULT 0.0,
            anomaly_detected BOOLEAN NOT NULL DEFAULT 0,
            anomaly_category TEXT CHECK(anomaly_category IN ('Sudden_Drop', 'Revenue_Spike', 'Irregular_Pattern', 'None')),
            volatility_trend_7d REAL NOT NULL DEFAULT 0.0,
            volatility_trend_30d REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id),
            UNIQUE(restaurant_id, date)
        )
        '''
        
        # Performance Feedback Loop Table
        performance_feedback_loop_sql = '''
        CREATE TABLE IF NOT EXISTS performance_feedback_loop (
            restaurant_id TEXT NOT NULL,
            feedback_date DATE NOT NULL,
            sales_team_rating TEXT NOT NULL CHECK(sales_team_rating IN ('Positive', 'Neutral', 'Negative')),
            prr_score REAL CHECK(prr_score >= 1.0 AND prr_score <= 10.0),
            nrr_score REAL CHECK(nrr_score >= 0.0 AND nrr_score <= 200.0),
            feedback_notes TEXT,
            action_items TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id)
        )
        '''
        
        # KPI Goals Tracking Table
        kpi_goals_tracking_sql = '''
        CREATE TABLE IF NOT EXISTS kpi_goals_tracking (
            restaurant_id TEXT NOT NULL,
            goal_period TEXT NOT NULL,
            kpi_type TEXT NOT NULL CHECK(kpi_type IN ('Revenue', 'Bookings', 'Rating', 'ROI', 'Conversion_Rate')),
            target_value REAL NOT NULL DEFAULT 0.0,
            actual_value REAL NOT NULL DEFAULT 0.0,
            goal_phase TEXT NOT NULL CHECK(goal_phase IN ('Q1', 'Q2', 'Q3', 'Q4', 'Monthly')),
            achievement_percentage REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id),
            UNIQUE(restaurant_id, goal_period, kpi_type)
        )
        '''
        
        try:
            cursor = self.conn.cursor()
            
            # Create core tables (enhanced)
            cursor.execute(restaurant_master_sql)
            cursor.execute(restaurant_metrics_sql)
            cursor.execute(ads_data_sql)
            cursor.execute(peer_benchmarks_sql)
            cursor.execute(discount_history_sql)
            
            # Create extended tables
            cursor.execute(operational_metrics_sql)
            cursor.execute(service_quality_tracking_sql)
            cursor.execute(financial_settlements_sql)
            cursor.execute(competitive_intelligence_sql)
            cursor.execute(revenue_volatility_tracking_sql)
            cursor.execute(performance_feedback_loop_sql)
            cursor.execute(kpi_goals_tracking_sql)
            
            self.conn.commit()
            logger.info("All 12 tables created successfully (5 enhanced core + 7 extended)")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def generate_mock_restaurants(self) -> List[Dict[str, Any]]:
        """Generate diverse mock restaurant data with different performance personalities"""
        restaurants = [
            {
                'restaurant_id': 'R001',
                'restaurant_name': 'Spice Garden',
                'city': 'Bangalore',
                'locality': 'Koramangala',
                'cuisine': 'Indian',
                'onboarded_date': '2023-11-15',
                'personality': 'consistent_performer',  # Steady, reliable performance
                'veg_nonveg_type': 'Veg',
                'online_order_enabled': 0,
                'establishment_date': '2021-02-01',
                'exclusivity_status': 'Non-Exclusive',
                'parent_type': 'Franchise',
                'seating_capacity': 79,
                'nps_score': 52.0
            },
            {
                'restaurant_id': 'R002', 
                'restaurant_name': 'Pizza Palace',
                'city': 'Bangalore',
                'locality': 'Indiranagar',
                'cuisine': 'Italian',
                'onboarded_date': '2024-01-20',
                'personality': 'rising_star',  # New restaurant with growing performance
                'veg_nonveg_type': 'Both',
                'online_order_enabled': 1,
                'establishment_date': '2023-12-01',
                'exclusivity_status': 'Exclusive',
                'parent_type': 'Brand-Owned',
                'seating_capacity': 42,
                'nps_score': 68.0
            },
            {
                'restaurant_id': 'R003',
                'restaurant_name': 'Sushi Zen',
                'city': 'Mumbai',
                'locality': 'Bandra',
                'cuisine': 'Japanese',
                'onboarded_date': '2023-09-10',
                'personality': 'premium_niche',  # High-end, lower volume, high margins
                'veg_nonveg_type': 'Both',
                'online_order_enabled': 1,
                'establishment_date': '2020-03-15',
                'exclusivity_status': 'Exclusive',
                'parent_type': 'Independent',
                'seating_capacity': 28,
                'nps_score': 84.0
            },
            {
                'restaurant_id': 'R004',
                'restaurant_name': 'Tandoor Express',
                'city': 'Delhi',
                'locality': 'Connaught Place',
                'cuisine': 'Indian',
                'onboarded_date': '2023-12-05',
                'personality': 'struggling_veteran',  # Established but declining performance
                'veg_nonveg_type': 'Both',
                'online_order_enabled': 0,
                'establishment_date': '2018-05-20',
                'exclusivity_status': 'Non-Exclusive',
                'parent_type': 'Independent',
                'seating_capacity': 95,
                'nps_score': 31.0
            },
            {
                'restaurant_id': 'R005',
                'restaurant_name': 'Burger Hub',
                'city': 'Bangalore',
                'locality': 'Koramangala',
                'cuisine': 'American',
                'onboarded_date': '2024-02-14',
                'personality': 'volume_player',  # High volume, lower margins
                'veg_nonveg_type': 'Both',
                'online_order_enabled': 1,
                'establishment_date': '2023-11-10',
                'exclusivity_status': 'Non-Exclusive',
                'parent_type': 'Franchise',
                'seating_capacity': 120,
                'nps_score': 45.0
            },
            {
                'restaurant_id': 'R006',
                'restaurant_name': 'Green Bowl Cafe',
                'city': 'Mumbai',
                'locality': 'Bandra',
                'cuisine': 'Continental',
                'onboarded_date': '2024-03-01',
                'personality': 'weekend_champion',  # Strong weekend performance, weak weekdays
                'veg_nonveg_type': 'Veg',
                'online_order_enabled': 1,
                'establishment_date': '2023-10-05',
                'exclusivity_status': 'Exclusive',
                'parent_type': 'Independent',
                'seating_capacity': 35,
                'nps_score': 71.0
            },
            {
                'restaurant_id': 'R007',
                'restaurant_name': 'Dragon Palace',
                'city': 'Delhi',
                'locality': 'Khan Market',
                'cuisine': 'Chinese',
                'onboarded_date': '2023-08-15',
                'personality': 'volatile_performer',  # Highly variable performance
                'veg_nonveg_type': 'Both',
                'online_order_enabled': 0,
                'establishment_date': '2019-01-12',
                'exclusivity_status': 'Non-Exclusive',
                'parent_type': 'Franchise',
                'seating_capacity': 65,
                'nps_score': 38.0
            },
            {
                'restaurant_id': 'R008',
                'restaurant_name': 'Coastal Kitchen',
                'city': 'Bangalore',
                'locality': 'Whitefield',
                'cuisine': 'Seafood',
                'onboarded_date': '2023-10-20',
                'personality': 'seasonal_specialist',  # Performance varies by season
                'veg_nonveg_type': 'Non-Veg',
                'online_order_enabled': 1,
                'establishment_date': '2021-08-30',
                'exclusivity_status': 'Exclusive',
                'parent_type': 'Brand-Owned',
                'seating_capacity': 55,
                'nps_score': 62.0
            }
        ]
        return restaurants
    
    def generate_mock_metrics(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate 30 days of realistic restaurant metrics data based on restaurant personalities"""
        metrics = []
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Define personality-based performance patterns
        personality_configs = {
            'consistent_performer': {
                'base_bookings': (15, 20), 'booking_variance': 3, 'base_rating': (4.1, 4.3), 
                'spend_range': (450, 650), 'trend_factor': 0.0, 'volatility': 0.15
            },
            'rising_star': {
                'base_bookings': (8, 15), 'booking_variance': 4, 'base_rating': (4.0, 4.4), 
                'spend_range': (400, 700), 'trend_factor': 0.8, 'volatility': 0.25
            },
            'premium_niche': {
                'base_bookings': (6, 12), 'booking_variance': 2, 'base_rating': (4.3, 4.7), 
                'spend_range': (800, 1200), 'trend_factor': 0.1, 'volatility': 0.12
            },
            'struggling_veteran': {
                'base_bookings': (12, 18), 'booking_variance': 5, 'base_rating': (3.8, 4.1), 
                'spend_range': (350, 550), 'trend_factor': -0.6, 'volatility': 0.35
            },
            'volume_player': {
                'base_bookings': (20, 30), 'booking_variance': 6, 'base_rating': (3.9, 4.2), 
                'spend_range': (300, 450), 'trend_factor': 0.2, 'volatility': 0.20
            },
            'weekend_champion': {
                'base_bookings': (10, 16), 'booking_variance': 8, 'base_rating': (4.0, 4.3), 
                'spend_range': (500, 750), 'trend_factor': 0.1, 'volatility': 0.40
            },
            'volatile_performer': {
                'base_bookings': (8, 25), 'booking_variance': 12, 'base_rating': (3.7, 4.5), 
                'spend_range': (400, 900), 'trend_factor': 0.0, 'volatility': 0.60
            },
            'seasonal_specialist': {
                'base_bookings': (12, 20), 'booking_variance': 5, 'base_rating': (4.1, 4.4), 
                'spend_range': (600, 800), 'trend_factor': 0.3, 'volatility': 0.30
            }
        }
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            restaurant_name = restaurant['restaurant_name']
            locality = restaurant['locality']
            cuisine = restaurant['cuisine']
            personality = restaurant['personality']
            config = personality_configs[personality]
            
            # Set base metrics based on personality
            base_bookings = random.randint(*config['base_bookings'])
            base_rating = round(random.uniform(*config['base_rating']), 1)
            
            current_date = start_date
            day_count = 0
            
            while current_date <= end_date:
                day_count += 1
                
                # Apply personality-specific patterns
                if personality == 'weekend_champion':
                    # Higher performance on weekends
                    weekend_multiplier = 1.8 if current_date.weekday() >= 5 else 0.7
                    daily_bookings = max(1, int(base_bookings * weekend_multiplier))
                elif personality == 'seasonal_specialist':
                    # Simulate seasonal variation (assuming winter season)
                    seasonal_multiplier = 1.2 if day_count % 7 < 3 else 0.9
                    daily_bookings = max(1, int(base_bookings * seasonal_multiplier))
                else:
                    # Apply trend and normal variance
                    trend_effect = (day_count / 30.0) * config['trend_factor']
                    variance = random.randint(-config['booking_variance'], config['booking_variance'])
                    daily_bookings = max(1, int(base_bookings + trend_effect + variance))
                
                # Apply volatility for some personalities
                if personality == 'volatile_performer' and random.random() < 0.15:
                    # Random spike or drop
                    daily_bookings = int(daily_bookings * random.uniform(0.3, 2.5))
                elif personality == 'struggling_veteran' and random.random() < 0.10:
                    # Occasional bad days
                    daily_bookings = max(1, int(daily_bookings * 0.4))
                
                # Calculate dependent metrics
                cancellations = max(0, int(daily_bookings * random.uniform(0.05, 0.18)))
                covers = daily_bookings * random.randint(2, 4)
                
                # Spending varies by cuisine and personality
                base_spend = random.uniform(*config['spend_range'])
                if cuisine == 'Japanese':
                    base_spend *= 1.2  # Premium cuisine
                elif cuisine == 'American':
                    base_spend *= 0.9  # Fast casual
                
                avg_spend = round(base_spend * random.uniform(0.85, 1.15), 2)
                revenue = covers * avg_spend
                
                # Rating with personality influence
                rating_variance = config['volatility'] * 0.5
                rating = max(1.0, min(5.0, base_rating + random.uniform(-rating_variance, rating_variance)))
                
                metrics.append({
                    'restaurant_id': restaurant_id,
                    'restaurant_name': restaurant_name,
                    'locality': locality,
                    'cuisine': cuisine,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'bookings': daily_bookings,
                    'cancellations': cancellations,
                    'covers': covers,
                    'avg_spend_per_cover': avg_spend,
                    'revenue': round(revenue, 2),
                    'avg_rating': round(rating, 1)
                })
                
                current_date += timedelta(days=1)
        
        return metrics
    
    def generate_mock_ads_data(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate mock ads campaign data"""
        ads_data = []
        campaign_types = ['visibility_boost', 'weekend_special', 'lunch_deals', 'dinner_prime']
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            # Generate 2-4 campaigns per restaurant
            num_campaigns = random.randint(2, 4)
            
            for i in range(num_campaigns):
                campaign_type = random.choice(campaign_types)
                campaign_id = f"C{restaurant_id[-3:]}_{i+1:02d}_{campaign_type[:4]}"
                
                # Random campaign duration (7-30 days)
                duration = random.randint(7, 30)
                end_date = datetime.now().date() - timedelta(days=random.randint(1, 10))
                start_date = end_date - timedelta(days=duration)
                
                impressions = random.randint(15000, 50000)
                clicks = int(impressions * random.uniform(0.05, 0.12))  # 5-12% CTR
                conversions = int(clicks * random.uniform(0.06, 0.15))  # 6-15% conversion
                spend = round(random.uniform(3000, 8000), 2)
                revenue_generated = round(conversions * random.uniform(80, 150), 2)
                
                # Financial details (previously separate table)
                total_investment = spend * random.uniform(1.1, 1.5)  # Investment is usually higher than actual spend
                fund_consumption_rate = round(spend / total_investment, 3)
                yoy_funding_change = round(random.uniform(-20.0, 45.0), 1)  # Year-over-year change %
                mom_funding_change = round(random.uniform(-15.0, 25.0), 1)  # Month-over-month change %
                
                ads_data.append({
                    'restaurant_id': restaurant_id,
                    'campaign_id': campaign_id,
                    'campaign_start': start_date.strftime('%Y-%m-%d'),
                    'campaign_end': end_date.strftime('%Y-%m-%d'),
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'spend': spend,
                    'revenue_generated': revenue_generated,
                    'total_investment': round(total_investment, 2),
                    'fund_consumption_rate': fund_consumption_rate,
                    'yoy_funding_change': yoy_funding_change,
                    'mom_funding_change': mom_funding_change,
                    'campaign_category': campaign_type
                })
        
        return ads_data
    
    def generate_mock_peer_benchmarks(self) -> List[Dict[str, Any]]:
        """Generate mock peer benchmark data"""
        localities = ['Koramangala', 'Indiranagar', 'Bandra', 'Connaught Place', 'Khan Market', 'Whitefield']
        cuisines = ['Indian', 'Italian', 'Japanese', 'American', 'Chinese', 'Continental', 'Seafood']
        
        benchmarks = []
        for locality in localities:
            for cuisine in cuisines:
                benchmarks.append({
                    'locality': locality,
                    'cuisine': cuisine,
                    'avg_bookings': round(random.uniform(12, 20), 1),
                    'avg_conversion_rate': round(random.uniform(0.07, 0.12), 3),
                    'avg_ads_spend': round(random.uniform(4000, 7000), 2),
                    'avg_roi': round(random.uniform(2.2, 3.8), 1),
                    'avg_revenue': round(random.uniform(150000, 250000), 2),
                    'avg_rating': round(random.uniform(4.0, 4.5), 1)
                })
        
        return benchmarks
    
    def generate_mock_discount_history(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate mock discount history data"""
        discount_data = []
        discount_types = ['Flat', 'Tiered', 'Combo', 'Happy Hour']
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            # Generate 1-3 discount periods per restaurant
            num_periods = random.randint(1, 3)
            
            for i in range(num_periods):
                duration = random.randint(14, 45)  # 2-6 weeks
                end_date = datetime.now().date() - timedelta(days=random.randint(1, 30))
                start_date = end_date - timedelta(days=duration)
                
                discount_data.append({
                    'restaurant_id': restaurant_id,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'discount_type': random.choice(discount_types),
                    'discount_percent': round(random.uniform(5, 25), 1),
                    'roi_from_discount': round(random.uniform(2.0, 4.2), 1)
                })
        
        return discount_data
    
    def generate_restaurant_profile_extensions(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate restaurant profile extensions with business context"""
        profile_extensions = []
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            personality = restaurant['personality']
            cuisine = restaurant['cuisine']
            
            # Determine characteristics based on personality and cuisine
            if personality == 'premium_niche':
                veg_type = 'Non-Veg' if cuisine == 'Japanese' else 'Both'
                exclusivity = 'Exclusive'
                parent_type = 'Independent'
                capacity = random.randint(20, 40)
                nps = random.randint(65, 85)
                establishment_date = (datetime.now().date() - timedelta(days=random.randint(1095, 2555))).strftime('%Y-%m-%d')
            elif personality == 'volume_player':
                veg_type = 'Both'
                exclusivity = 'Non-Exclusive'
                parent_type = 'Franchise'
                capacity = random.randint(80, 150)
                nps = random.randint(35, 55)
                establishment_date = (datetime.now().date() - timedelta(days=random.randint(730, 1825))).strftime('%Y-%m-%d')
            elif personality == 'rising_star':
                veg_type = 'Both'
                exclusivity = 'Exclusive'
                parent_type = 'Independent'
                capacity = random.randint(40, 70)
                nps = random.randint(55, 75)
                establishment_date = (datetime.now().date() - timedelta(days=random.randint(180, 720))).strftime('%Y-%m-%d')
            else:
                veg_type = random.choice(['Veg', 'Non-Veg', 'Both'])
                exclusivity = random.choice(['Exclusive', 'Non-Exclusive'])
                parent_type = random.choice(['Franchise', 'Brand-Owned', 'Independent'])
                capacity = random.randint(30, 80)
                nps = random.randint(40, 70)
                establishment_date = (datetime.now().date() - timedelta(days=random.randint(365, 2190))).strftime('%Y-%m-%d')
            
            profile_extensions.append({
                'restaurant_id': restaurant_id,
                'veg_nonveg_type': veg_type,
                'online_order_enabled': random.choice([0, 1]),
                'establishment_date': establishment_date,
                'exclusivity_status': exclusivity,
                'parent_type': parent_type,
                'seating_capacity': capacity,
                'nps_score': nps
            })
        
        return profile_extensions
    
    def generate_operational_metrics(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate hourly operational metrics for last 30 days"""
        operational_data = []
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Operating hours: 12 PM to 11 PM (12-23)
        operating_hours = list(range(12, 24))
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            personality = restaurant['personality']
            capacity = random.randint(30, 100)  # Base capacity for calculations
            
            current_date = start_date
            while current_date <= end_date:
                for hour in operating_hours:
                    # Peak hours: 1-3 PM and 7-9 PM
                    is_peak = hour in [13, 14, 15, 19, 20, 21]
                    is_weekend = current_date.weekday() >= 5
                    
                    # Base utilization varies by personality and time
                    if personality == 'weekend_champion':
                        base_utilization = 85 if is_weekend else 45
                    elif personality == 'premium_niche':
                        base_utilization = 65 if is_peak else 30
                    elif personality == 'volume_player':
                        base_utilization = 75 if is_peak else 55
                    else:
                        base_utilization = 70 if is_peak else 40
                    
                    # Add randomness
                    utilization = max(0, min(100, base_utilization + random.randint(-15, 15)))
                    
                    # Calculate other metrics based on utilization
                    online_bookings = int(utilization * 0.4 * random.uniform(0.7, 1.3))
                    offline_bookings = int(utilization * 0.6 * random.uniform(0.7, 1.3))
                    
                    # Overbooking incidents (rare but realistic)
                    overbooking = 1 if utilization > 90 and random.random() < 0.1 else 0
                    underbooking = max(0, capacity - online_bookings - offline_bookings) if utilization < 50 else 0
                    
                    # Service delays increase with utilization
                    delay_factor = max(0, (utilization - 60) / 40)
                    service_delay = random.uniform(0, 15) * delay_factor
                    
                    operational_data.append({
                        'restaurant_id': restaurant_id,
                        'date': current_date.strftime('%Y-%m-%d'),
                        'hour_slot': hour,
                        'capacity_utilization': round(utilization, 1),
                        'overbooking_incidents': overbooking,
                        'underbooking_slots': underbooking,
                        'online_bookings': online_bookings,
                        'offline_bookings': offline_bookings,
                        'service_delay_minutes': round(service_delay, 1)
                    })
                
                current_date += timedelta(days=1)
        
        return operational_data
    
    def generate_service_quality_data(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate daily service quality tracking data"""
        quality_data = []
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        complaint_categories = ['Food Quality', 'Service Speed', 'Staff Behavior', 'Cleanliness', 'Billing Issues']
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            personality = restaurant['personality']
            
            # Base service levels vary by personality
            if personality == 'premium_niche':
                base_service_rating = random.uniform(4.3, 4.7)
                complaints_rate = 0.02
            elif personality == 'struggling_veteran':
                base_service_rating = random.uniform(3.5, 3.9)
                complaints_rate = 0.08
            else:
                base_service_rating = random.uniform(3.8, 4.4)
                complaints_rate = 0.04
            
            current_date = start_date
            while current_date <= end_date:
                # Daily review volume based on restaurant size
                reviews_count = random.randint(2, 15)
                
                # Service rating with daily variation
                service_rating = max(1.0, min(5.0, base_service_rating + random.uniform(-0.4, 0.4)))
                
                # Complaints based on service level
                complaints = max(0, int(reviews_count * complaints_rate * random.uniform(0.5, 1.5)))
                
                # Resolution time varies by restaurant efficiency
                if personality == 'premium_niche':
                    resolution_time = random.uniform(2, 8)
                elif personality == 'struggling_veteran':
                    resolution_time = random.uniform(12, 48)
                else:
                    resolution_time = random.uniform(4, 24)
                
                # Select complaint categories
                selected_categories = random.sample(complaint_categories, min(complaints, len(complaint_categories)))
                
                quality_data.append({
                    'restaurant_id': restaurant_id,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'reviews_count': reviews_count,
                    'avg_service_rating': round(service_rating, 1),
                    'complaints_count': complaints,
                    'complaint_categories': ', '.join(selected_categories) if selected_categories else None,
                    'resolution_time_hours': round(resolution_time, 1)
                })
                
                current_date += timedelta(days=1)
        
        return quality_data
    
    def generate_campaign_financial_details(self, ads_data: List[Dict]) -> List[Dict[str, Any]]:
        """Generate financial details for ad campaigns"""
        financial_details = []
        
        campaign_categories = ['Brand Awareness', 'Revenue Drive', 'Customer Acquisition', 'Retention']
        
        for ad in ads_data:
            spend = ad['spend']
            
            # Total investment is usually 10-30% higher than actual spend
            total_investment = spend * random.uniform(1.1, 1.3)
            
            # Fund consumption rate
            consumption_rate = spend / total_investment if total_investment > 0 else 0
            
            # YoY and MoM changes (simulated)
            yoy_change = random.uniform(-25, 40)  # -25% to +40%
            mom_change = random.uniform(-15, 25)  # -15% to +25%
            
            financial_details.append({
                'restaurant_id': ad['restaurant_id'],
                'campaign_id': ad['campaign_id'],
                'total_investment': round(total_investment, 2),
                'fund_consumption_rate': round(consumption_rate, 3),
                'yoy_funding_change': round(yoy_change, 1),
                'mom_funding_change': round(mom_change, 1),
                'campaign_category': random.choice(campaign_categories)
            })
        
        return financial_details
    
    def generate_financial_settlements(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate financial settlement records"""
        settlement_data = []
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)  # 3 months of settlement history
        
        settlement_types = ['Commission', 'Refund', 'Penalty', 'Bonus']
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            personality = restaurant['personality']
            
            # Number of settlements varies by restaurant type
            if personality == 'volume_player':
                num_settlements = random.randint(8, 15)
            elif personality == 'premium_niche':
                num_settlements = random.randint(3, 8)
            else:
                num_settlements = random.randint(5, 12)
            
            for _ in range(num_settlements):
                settlement_date = start_date + timedelta(days=random.randint(0, 90))
                settlement_type = random.choice(settlement_types)
                
                if settlement_type == 'Commission':
                    amount = random.uniform(5000, 25000)
                    processing_days = random.randint(2, 7)
                elif settlement_type == 'Refund':
                    amount = random.uniform(500, 5000)
                    processing_days = random.randint(1, 5)
                elif settlement_type == 'Penalty':
                    amount = random.uniform(200, 2000)
                    processing_days = random.randint(1, 3)
                else:  # Bonus
                    amount = random.uniform(1000, 8000)
                    processing_days = random.randint(3, 10)
                
                outstanding = random.uniform(0, amount * 0.2) if random.random() < 0.2 else 0
                
                settlement_data.append({
                    'restaurant_id': restaurant_id,
                    'settlement_date': settlement_date.strftime('%Y-%m-%d'),
                    'settlement_amount': round(amount, 2),
                    'settlement_type': settlement_type,
                    'processing_time_days': processing_days,
                    'outstanding_amount': round(outstanding, 2)
                })
        
        return settlement_data
    
    def generate_competitive_intelligence(self) -> List[Dict[str, Any]]:
        """Generate competitive intelligence data"""
        competitive_data = []
        
        localities = ['Koramangala', 'Indiranagar', 'Bandra', 'Connaught Place', 'Khan Market', 'Whitefield']
        cuisines = ['Indian', 'Italian', 'Japanese', 'American', 'Chinese', 'Continental', 'Seafood']
        capacity_ranges = ['Small (1-30)', 'Medium (31-80)', 'Large (81+)']
        price_positions = ['Premium', 'Mid-Range', 'Budget']
        
        for locality in localities:
            for cuisine in cuisines:
                for capacity_range in capacity_ranges:
                    # Market characteristics vary by locality and cuisine
                    if locality in ['Bandra', 'Khan Market'] and cuisine == 'Japanese':
                        competitor_count = random.randint(8, 15)
                        market_share = random.uniform(5, 15)
                        avg_rating = random.uniform(4.2, 4.6)
                        price_pos = 'Premium'
                        competitive_score = random.uniform(7, 9)
                    elif capacity_range == 'Large (81+)' and cuisine == 'American':
                        competitor_count = random.randint(12, 25)
                        market_share = random.uniform(8, 20)
                        avg_rating = random.uniform(3.8, 4.2)
                        price_pos = 'Mid-Range'
                        competitive_score = random.uniform(5, 7)
                    else:
                        competitor_count = random.randint(5, 20)
                        market_share = random.uniform(3, 25)
                        avg_rating = random.uniform(3.5, 4.5)
                        price_pos = random.choice(price_positions)
                        competitive_score = random.uniform(4, 8)
                    
                    competitive_data.append({
                        'locality': locality,
                        'cuisine': cuisine,
                        'capacity_range': capacity_range,
                        'competitor_count': competitor_count,
                        'market_share_estimate': round(market_share, 1),
                        'avg_competitor_rating': round(avg_rating, 1),
                        'price_positioning': price_pos,
                        'competitive_advantage_score': round(competitive_score, 1)
                    })
        
        return competitive_data
    
    def generate_revenue_volatility_tracking(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate revenue volatility and anomaly detection data"""
        volatility_data = []
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        anomaly_categories = ['Sudden_Drop', 'Revenue_Spike', 'Irregular_Pattern', 'None']
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            personality = restaurant['personality']
            
            # Base volatility varies by personality
            if personality == 'volatile_performer':
                base_volatility = random.uniform(0.6, 0.9)
                anomaly_probability = 0.25
            elif personality == 'consistent_performer':
                base_volatility = random.uniform(0.1, 0.3)
                anomaly_probability = 0.05
            elif personality == 'struggling_veteran':
                base_volatility = random.uniform(0.4, 0.7)
                anomaly_probability = 0.15
            else:
                base_volatility = random.uniform(0.2, 0.5)
                anomaly_probability = 0.10
            
            current_date = start_date
            while current_date <= end_date:
                # Daily volatility index
                volatility_index = max(0, base_volatility + random.uniform(-0.2, 0.2))
                
                # Anomaly detection
                is_anomaly = random.random() < anomaly_probability
                anomaly_category = random.choice(anomaly_categories[:-1]) if is_anomaly else 'None'
                
                # Trend calculations (simplified)
                trend_7d = random.uniform(-0.3, 0.3)
                trend_30d = random.uniform(-0.5, 0.5)
                
                volatility_data.append({
                    'restaurant_id': restaurant_id,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'revenue_volatility_index': round(volatility_index, 3),
                    'anomaly_detected': 1 if is_anomaly else 0,
                    'anomaly_category': anomaly_category,
                    'volatility_trend_7d': round(trend_7d, 3),
                    'volatility_trend_30d': round(trend_30d, 3)
                })
                
                current_date += timedelta(days=1)
        
        return volatility_data
    
    def generate_performance_feedback(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate sales team feedback data"""
        feedback_data = []
        end_date = datetime.now().date()
        
        feedback_notes_templates = [
            "Strong performance this quarter, exceeding targets",
            "Needs improvement in weekend conversion rates",
            "Excellent customer feedback and ratings",
            "Struggling with operational efficiency",
            "Great potential for growth with right strategy",
            "Concerns about declining review scores",
            "Outstanding ROI on recent campaigns"
        ]
        
        action_items_templates = [
            "Increase ad spend by 20%",
            "Focus on service quality improvement",
            "Implement weekend promotional strategy",
            "Review pricing and discount strategy",
            "Schedule operational efficiency consultation",
            "Launch customer retention campaign"
        ]
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            personality = restaurant['personality']
            
            # Generate 2-4 feedback records per restaurant
            num_feedback = random.randint(2, 4)
            
            for i in range(num_feedback):
                feedback_date = end_date - timedelta(days=random.randint(1, 90))
                
                # Rating based on personality
                if personality == 'rising_star':
                    sales_rating = 'Positive'
                    prr_score = random.uniform(7, 9)
                    nrr_score = random.uniform(110, 150)
                elif personality == 'struggling_veteran':
                    sales_rating = 'Negative'
                    prr_score = random.uniform(3, 5)
                    nrr_score = random.uniform(70, 95)
                elif personality == 'premium_niche':
                    sales_rating = 'Positive'
                    prr_score = random.uniform(8, 10)
                    nrr_score = random.uniform(120, 160)
                else:
                    sales_rating = random.choice(['Positive', 'Neutral', 'Negative'])
                    prr_score = random.uniform(5, 8)
                    nrr_score = random.uniform(90, 130)
                
                feedback_data.append({
                    'restaurant_id': restaurant_id,
                    'feedback_date': feedback_date.strftime('%Y-%m-%d'),
                    'sales_team_rating': sales_rating,
                    'prr_score': round(prr_score, 1),
                    'nrr_score': round(nrr_score, 1),
                    'feedback_notes': random.choice(feedback_notes_templates),
                    'action_items': random.choice(action_items_templates)
                })
        
        return feedback_data
    
    def generate_kpi_goals_tracking(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate KPI goals and tracking data"""
        kpi_data = []
        
        kpi_types = ['Revenue', 'Bookings', 'Rating', 'ROI', 'Conversion_Rate']
        goal_phases = ['Q1', 'Q2', 'Q3', 'Q4']
        current_year = datetime.now().year
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            personality = restaurant['personality']
            
            for quarter in goal_phases:
                for kpi_type in kpi_types:
                    goal_period = f"{current_year}-{quarter}"
                    
                    # Set targets based on personality and KPI type
                    if kpi_type == 'Revenue':
                        if personality == 'volume_player':
                            target = random.uniform(200000, 350000)
                            actual = target * random.uniform(0.8, 1.2)
                        elif personality == 'premium_niche':
                            target = random.uniform(150000, 250000)
                            actual = target * random.uniform(0.9, 1.15)
                        else:
                            target = random.uniform(100000, 200000)
                            actual = target * random.uniform(0.7, 1.3)
                    
                    elif kpi_type == 'Bookings':
                        if personality == 'volume_player':
                            target = random.uniform(600, 900)
                            actual = target * random.uniform(0.8, 1.2)
                        else:
                            target = random.uniform(300, 600)
                            actual = target * random.uniform(0.7, 1.3)
                    
                    elif kpi_type == 'Rating':
                        target = random.uniform(4.0, 4.5)
                        actual = target + random.uniform(-0.3, 0.3)
                    
                    elif kpi_type == 'ROI':
                        target = random.uniform(2.5, 4.0)
                        actual = target * random.uniform(0.6, 1.4)
                    
                    else:  # Conversion_Rate
                        target = random.uniform(0.08, 0.15)
                        actual = target * random.uniform(0.7, 1.3)
                    
                    achievement = (actual / target * 100) if target > 0 else 0
                    
                    kpi_data.append({
                        'restaurant_id': restaurant_id,
                        'goal_period': goal_period,
                        'kpi_type': kpi_type,
                        'target_value': round(target, 2),
                        'actual_value': round(actual, 2),
                        'goal_phase': quarter,
                        'achievement_percentage': round(achievement, 1)
                    })
        
        return kpi_data
    
    def insert_data(self, table_name: str, data: List[Dict[str, Any]]):
        """Insert data into specified table"""
        if not data:
            logger.warning(f"No data to insert into {table_name}")
            return
        
        try:
            cursor = self.conn.cursor()
            columns = list(data[0].keys())
            placeholders = ', '.join(['?' for _ in columns])
            sql = f"INSERT OR REPLACE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            values = [tuple(row[col] for col in columns) for row in data]
            cursor.executemany(sql, values)
            self.conn.commit()
            
            logger.info(f"Inserted {len(data)} records into {table_name}")
        except sqlite3.Error as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            raise
    
    def initialize_database(self):
        """Main method to initialize the entire database"""
        try:
            logger.info("Starting database initialization...")
            
            # Remove existing database file
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                logger.info(f"Removed existing database: {self.db_path}")
            
            # Connect and create tables
            self.connect()
            self.create_tables()
            
            # Generate and insert mock data
            logger.info("Generating comprehensive mock data for all 12 consolidated tables...")
            
            # Core data generation
            restaurants = self.generate_mock_restaurants()
            
            # Filter out personality field for database insertion (used only for data generation logic)
            restaurants_for_db = []
            for restaurant in restaurants:
                restaurant_copy = restaurant.copy()
                restaurant_copy.pop('personality', None)  # Remove personality field
                restaurants_for_db.append(restaurant_copy)
            
            self.insert_data('restaurant_master', restaurants_for_db)
            
            metrics = self.generate_mock_metrics(restaurants)
            self.insert_data('restaurant_metrics', metrics)
            
            ads_data = self.generate_mock_ads_data(restaurants)
            self.insert_data('ads_data', ads_data)
            
            peer_benchmarks = self.generate_mock_peer_benchmarks()
            self.insert_data('peer_benchmarks', peer_benchmarks)
            
            discount_history = self.generate_mock_discount_history(restaurants)
            self.insert_data('discount_history', discount_history)
            
            # Extended data generation
            logger.info("Generating extended business intelligence data...")
            
            operational_metrics = self.generate_operational_metrics(restaurants)
            self.insert_data('operational_metrics', operational_metrics)
            
            service_quality = self.generate_service_quality_data(restaurants)
            self.insert_data('service_quality_tracking', service_quality)
            
            financial_settlements = self.generate_financial_settlements(restaurants)
            self.insert_data('financial_settlements', financial_settlements)
            
            competitive_intel = self.generate_competitive_intelligence()
            self.insert_data('competitive_intelligence', competitive_intel)
            
            volatility_tracking = self.generate_revenue_volatility_tracking(restaurants)
            self.insert_data('revenue_volatility_tracking', volatility_tracking)
            
            performance_feedback = self.generate_performance_feedback(restaurants)
            self.insert_data('performance_feedback_loop', performance_feedback)
            
            kpi_goals = self.generate_kpi_goals_tracking(restaurants)
            self.insert_data('kpi_goals_tracking', kpi_goals)
            
            logger.info("Database initialization completed successfully!")
            
            # Print summary
            cursor = self.conn.cursor()
            
            # Core tables
            core_tables = ['restaurant_master', 'restaurant_metrics', 'ads_data', 'peer_benchmarks', 'discount_history']
            
            # Extended tables
            extended_tables = [
                'operational_metrics', 'service_quality_tracking', 'financial_settlements', 
                'competitive_intelligence', 'revenue_volatility_tracking', 'performance_feedback_loop', 
                'kpi_goals_tracking'
            ]
            
            print("\n" + "="*70)
            print("DATABASE INITIALIZATION SUMMARY")
            print("="*70)
            
            print("\nCORE TABLES (Problem Statement):")
            print("-" * 40)
            for table in core_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table:<30}: {count:>8} records")
            
            print("\nEXTENDED TABLES (Business Intelligence):")
            print("-" * 40)
            for table in extended_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table:<30}: {count:>8} records")
            
            # Calculate totals
            total_records = 0
            for table in core_tables + extended_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                total_records += cursor.fetchone()[0]
            
            print("\n" + "="*70)
            print(f"Total Tables: {len(core_tables + extended_tables)} (5 enhanced core + 7 extended)")
            print(f"Total Records: {total_records:,}")
            print(f"Database file: {self.db_path}")
            print("="*70)
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
        finally:
            self.close()

def main():
    """Main function to run database initialization"""
    try:
        db_initializer = DatabaseInitializer()
        db_initializer.initialize_database()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())