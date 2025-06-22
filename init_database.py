#!/usr/bin/env python3
"""
Swiggy Dineout GenAI Co-Pilot Challenge - Database Initialization Script

This script initializes a SQLite database with tables and mock data for the
restaurant performance analytics system.
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
        
        # Restaurant Master Table
        restaurant_master_sql = '''
        CREATE TABLE IF NOT EXISTS restaurant_master (
            restaurant_id TEXT PRIMARY KEY,
            restaurant_name TEXT NOT NULL,
            city TEXT NOT NULL,
            locality TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            onboarded_date DATE NOT NULL
        )
        '''
        
        # Restaurant Metrics Table
        restaurant_metrics_sql = '''
        CREATE TABLE IF NOT EXISTS restaurant_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id TEXT NOT NULL,
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
        
        # Ads Data Table
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
            FOREIGN KEY (restaurant_id) REFERENCES restaurant_master (restaurant_id),
            UNIQUE(restaurant_id, campaign_id)
        )
        '''
        
        # Peer Benchmarks Table
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
        
        # Discount History Table
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
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(restaurant_master_sql)
            cursor.execute(restaurant_metrics_sql)
            cursor.execute(ads_data_sql)
            cursor.execute(peer_benchmarks_sql)
            cursor.execute(discount_history_sql)
            self.conn.commit()
            logger.info("All tables created successfully")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def generate_mock_restaurants(self) -> List[Dict[str, Any]]:
        """Generate mock restaurant data"""
        restaurants = [
            {
                'restaurant_id': 'R001',
                'restaurant_name': 'Spice Garden',
                'city': 'Bangalore',
                'locality': 'Koramangala',
                'cuisine': 'Indian',
                'onboarded_date': '2023-11-15'
            },
            {
                'restaurant_id': 'R002',
                'restaurant_name': 'Pizza Palace',
                'city': 'Bangalore',
                'locality': 'Indiranagar',
                'cuisine': 'Italian',
                'onboarded_date': '2024-01-20'
            },
            {
                'restaurant_id': 'R003',
                'restaurant_name': 'Sushi Zen',
                'city': 'Mumbai',
                'locality': 'Bandra',
                'cuisine': 'Japanese',
                'onboarded_date': '2023-09-10'
            },
            {
                'restaurant_id': 'R004',
                'restaurant_name': 'Tandoor Express',
                'city': 'Delhi',
                'locality': 'Connaught Place',
                'cuisine': 'Indian',
                'onboarded_date': '2023-12-05'
            },
            {
                'restaurant_id': 'R005',
                'restaurant_name': 'Burger Hub',
                'city': 'Bangalore',
                'locality': 'Koramangala',
                'cuisine': 'American',
                'onboarded_date': '2024-02-14'
            }
        ]
        return restaurants
    
    def generate_mock_metrics(self, restaurants: List[Dict]) -> List[Dict[str, Any]]:
        """Generate 30 days of mock restaurant metrics data"""
        metrics = []
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        for restaurant in restaurants:
            restaurant_id = restaurant['restaurant_id']
            base_bookings = random.randint(8, 25)  # Base daily bookings
            base_rating = round(random.uniform(3.8, 4.8), 1)
            
            current_date = start_date
            while current_date <= end_date:
                # Add some randomness to daily metrics
                bookings = max(0, base_bookings + random.randint(-5, 8))
                cancellations = max(0, int(bookings * random.uniform(0.05, 0.15)))
                covers = bookings * random.randint(2, 4)
                avg_spend = round(random.uniform(400, 800), 2)
                revenue = covers * avg_spend
                rating = max(1.0, min(5.0, base_rating + random.uniform(-0.3, 0.3)))
                
                metrics.append({
                    'restaurant_id': restaurant_id,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'bookings': bookings,
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
                
                ads_data.append({
                    'restaurant_id': restaurant_id,
                    'campaign_id': campaign_id,
                    'campaign_start': start_date.strftime('%Y-%m-%d'),
                    'campaign_end': end_date.strftime('%Y-%m-%d'),
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'spend': spend,
                    'revenue_generated': revenue_generated
                })
        
        return ads_data
    
    def generate_mock_peer_benchmarks(self) -> List[Dict[str, Any]]:
        """Generate mock peer benchmark data"""
        localities = ['Koramangala', 'Indiranagar', 'Bandra', 'Connaught Place', 'Whitefield']
        cuisines = ['Indian', 'Italian', 'Japanese', 'American', 'Chinese']
        
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
            logger.info("Generating mock data...")
            
            restaurants = self.generate_mock_restaurants()
            self.insert_data('restaurant_master', restaurants)
            
            metrics = self.generate_mock_metrics(restaurants)
            self.insert_data('restaurant_metrics', metrics)
            
            ads_data = self.generate_mock_ads_data(restaurants)
            self.insert_data('ads_data', ads_data)
            
            peer_benchmarks = self.generate_mock_peer_benchmarks()
            self.insert_data('peer_benchmarks', peer_benchmarks)
            
            discount_history = self.generate_mock_discount_history(restaurants)
            self.insert_data('discount_history', discount_history)
            
            logger.info("Database initialization completed successfully!")
            
            # Print summary
            cursor = self.conn.cursor()
            tables = ['restaurant_master', 'restaurant_metrics', 'ads_data', 'peer_benchmarks', 'discount_history']
            
            print("\n" + "="*50)
            print("DATABASE INITIALIZATION SUMMARY")
            print("="*50)
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table:20}: {count:6} records")
            
            print("="*50)
            print(f"Database file: {self.db_path}")
            print("="*50)
            
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