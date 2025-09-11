#!/usr/bin/env python3
"""
Migration script to add donor_id column to OfflineDonation table
This script adds the donor_id field to prevent duplicate records during sync
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add donor_id column to OfflineDonation table"""
    
    # Database path
    db_path = 'instance/daiva_anughara.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found. Please run the application first to create the database.")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"📁 Database path: {db_path}")
        
        # Check if donor_id column already exists
        cursor.execute("PRAGMA table_info(offline_donation)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Current columns: {columns}")
        
        if 'donor_id' in columns:
            print("✅ donor_id column already exists. Migration not needed.")
            return True
        
        print("🔄 Adding donor_id column to OfflineDonation table...")
        
        # Add the donor_id column
        cursor.execute("""
            ALTER TABLE offline_donation 
            ADD COLUMN donor_id VARCHAR(50)
        """)
        
        # Commit changes
        conn.commit()
        
        print("✅ Successfully added donor_id column to OfflineDonation table")
        print("📝 The donor_id column will be used to prevent duplicate records during sync")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False
    finally:
        if conn:
            conn.close()

def verify_migration():
    """Verify that the migration was successful"""
    db_path = 'instance/daiva_anughara.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if donor_id column exists
        cursor.execute("PRAGMA table_info(offline_donation)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'donor_id' in columns:
            print("✅ Migration verification successful: donor_id column exists")
            return True
        else:
            print("❌ Migration verification failed: donor_id column not found")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Daiva Anughara - Database Migration")
    print("=" * 50)
    print("Adding donor_id column to prevent duplicate records during sync")
    print()
    
    if migrate_database():
        if verify_migration():
            print()
            print("🎉 Migration completed successfully!")
            print("📋 Next steps:")
            print("1. Restart your application")
            print("2. Run sync from admin panel")
            print("3. Duplicate records will be prevented using Donor_ID from Google Sheets")
        else:
            print("❌ Migration verification failed")
    else:
        print("❌ Migration failed")
