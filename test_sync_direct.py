#!/usr/bin/env python3
"""
Test sync functionality directly
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from google_sheets import get_sheets_manager
from app import app

def test_sync_direct():
    """Test sync functionality directly"""
    print("🧪 Testing Sync Functionality Directly")
    print("=" * 50)
    
    with app.app_context():
        # Check initial state
        initial_count = OfflineDonation.query.count()
        print(f"📊 Initial donation count: {initial_count}")
        
        # Test sync
        if get_sheets_manager().is_connected():
            print("✅ Google Sheets connected")
            try:
                success, message = get_sheets_manager().sync_donations_from_sheets()
                if success:
                    print(f"✅ Sync successful: {message}")
                    
                    # Check final state
                    final_count = OfflineDonation.query.count()
                    print(f"📊 Final donation count: {final_count}")
                    print(f"📈 Records added/updated: {final_count - initial_count}")
                    
                    # Check if data is properly structured
                    all_donations = OfflineDonation.query.order_by(OfflineDonation.donation_date.desc()).all()
                    print(f"📋 Sample donations:")
                    for i, donation in enumerate(all_donations[:3]):
                        print(f"   {i+1}. {donation.donor_name} - ₹{donation.amount} ({donation.purpose.name if donation.purpose else 'No Purpose'})")
                    
                    return True
                else:
                    print(f"❌ Sync failed: {message}")
                    return False
            except Exception as e:
                print(f"❌ Error during sync: {e}")
                return False
        else:
            print("❌ Google Sheets not connected")
            return False

if __name__ == "__main__":
    test_sync_direct()
