#!/usr/bin/env python3
"""
Migration script to add worksheet column to OfflineDonation table
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add worksheet column to OfflineDonation table"""
    
    # Database path
    db_path = 'instance/daiva_anughara.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found.")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if worksheet column already exists
        cursor.execute("PRAGMA table_info(offline_donation)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'worksheet' in columns:
            print("✅ worksheet column already exists. Migration not needed.")
            return True
        
        print("🔄 Adding worksheet column to OfflineDonation table...")
        
        # Add the worksheet column
        cursor.execute("""
            ALTER TABLE offline_donation 
            ADD COLUMN worksheet VARCHAR(100)
        """)
        
        # Commit changes
        conn.commit()
        
        print("✅ Successfully added worksheet column to OfflineDonation table")
        
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

if __name__ == "__main__":
    print("🚀 Adding Worksheet Column Migration")
    print("=" * 40)
    
    if migrate_database():
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed")
