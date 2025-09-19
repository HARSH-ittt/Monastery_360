#!/usr/bin/env python3
"""
Database setup script for Sacred Sikkim Research Submission System
Run this script to create the MySQL database and tables
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(__file__))
from config.database import db_manager

def create_database():
    """Create the sacred_sikkim database if it doesn't exist"""
    try:
        # Connect to MySQL server without specifying database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change this to your MySQL username
            password=''   # Change this to your MySQL password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS sacred_sikkim CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'sacred_sikkim' created successfully")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def setup_tables():
    """Create all necessary tables"""
    try:
        if db_manager.connect():
            success = db_manager.create_tables()
            db_manager.close()
            return success
        else:
            print("❌ Failed to connect to database")
            return False
    except Error as e:
        print(f"❌ Error setting up tables: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Sacred Sikkim Research Database...")
    print("=" * 50)
    
    # Step 1: Create database
    print("📊 Creating database...")
    if not create_database():
        print("❌ Failed to create database. Please check your MySQL connection.")
        sys.exit(1)
    
    # Step 2: Create tables
    print("📋 Creating tables...")
    if not setup_tables():
        print("❌ Failed to create tables. Please check your MySQL connection.")
        sys.exit(1)
    
    print("=" * 50)
    print("✅ Database setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Make sure your MySQL server is running")
    print("2. Update database credentials in backend/config/database.py if needed")
    print("3. Install Python dependencies: pip install -r requirements.txt")
    print("4. Start the Flask server: python api/server.py")
    print("\n🌐 The research submission system will be available at:")
    print("   - Frontend: http://localhost:3000")
    print("   - API: http://localhost:3000/api/research/")

if __name__ == '__main__':
    main()

