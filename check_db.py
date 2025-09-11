#!/usr/bin/env python3
"""
Quick script to check database structure
"""

import sqlite3
import os

def check_database():
    db_path = 'instance/daiva_anughara.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check offline_donation table structure
        cursor.execute("PRAGMA table_info(offline_donation)")
        columns = cursor.fetchall()
        
        print("📋 OfflineDonation table columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Check if donor_id exists
        donor_id_exists = any(col[1] == 'donor_id' for col in columns)
        print(f"\n✅ donor_id column exists: {donor_id_exists}")
        
        # Count existing records
        cursor.execute("SELECT COUNT(*) FROM offline_donation")
        count = cursor.fetchone()[0]
        print(f"📊 Total records in offline_donation: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_database()
