#!/usr/bin/env python3
"""
Simple Database Fix Script
Adds the profile_picture column to the user table
"""

import sqlite3
import os

def fix_database():
    """Add profile_picture column to user table"""
    db_path = 'daiva_anughara.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found!")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'profile_picture' in columns:
            print("✅ profile_picture column already exists in user table")
            conn.close()
            return True
        
        # Add the new column
        print("🔄 Adding profile_picture column to user table...")
        cursor.execute('ALTER TABLE user ADD COLUMN profile_picture VARCHAR(255)')
        
        # Commit the changes
        conn.commit()
        conn.close()
        
        print("✅ Successfully added profile_picture column to user table")
        return True
        
    except Exception as e:
        print(f"❌ Error during database fix: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting database fix...")
    success = fix_database()
    
    if success:
        print("🎉 Database fix completed successfully!")
    else:
        print("⚠️  Database fix failed. Please check the errors above.")
