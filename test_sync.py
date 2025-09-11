#!/usr/bin/env python3
"""
Test script to verify sync functionality with donor_id
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from google_sheets import sheets_manager

def test_sync():
    """Test the sync functionality"""
    print("🧪 Testing Sync Functionality with Donor_ID")
    print("=" * 50)
    
    # Check if Google Sheets is connected
    if not sheets_manager.is_connected():
        print("❌ Google Sheets not connected. Please set up credentials first.")
        return False
    
    print("✅ Google Sheets connected")
    
    # Get current record count
    initial_count = OfflineDonation.query.count()
    print(f"📊 Initial record count: {initial_count}")
    
    # Test sync
    print("🔄 Running sync...")
    try:
        success, message = sheets_manager.sync_donations_from_sheets()
        if success:
            print(f"✅ Sync successful: {message}")
            
            # Check final record count
            final_count = OfflineDonation.query.count()
            print(f"📊 Final record count: {final_count}")
            print(f"📈 Records added/updated: {final_count - initial_count}")
            
            # Check for duplicates by donor_id
            duplicates = db.session.query(OfflineDonation.donor_id).filter(
                OfflineDonation.donor_id.isnot(None)
            ).group_by(OfflineDonation.donor_id).having(
                db.func.count(OfflineDonation.donor_id) > 1
            ).all()
            
            if duplicates:
                print(f"❌ Found {len(duplicates)} duplicate donor_ids:")
                for dup in duplicates:
                    print(f"  - {dup[0]}")
            else:
                print("✅ No duplicate donor_ids found!")
            
            return True
        else:
            print(f"❌ Sync failed: {message}")
            return False
            
    except Exception as e:
        print(f"❌ Error during sync: {e}")
        return False

if __name__ == "__main__":
    # Initialize Flask app context
    from app import app
    with app.app_context():
        test_sync()
