#!/usr/bin/env python3
"""
Debug the sync process step by step
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from google_sheets import sheets_manager
from app import app

def debug_sync_process():
    """Debug the sync process step by step"""
    print("🔍 Debugging Sync Process Step by Step")
    print("=" * 50)
    
    with app.app_context():
        # Get a few donations from Google Sheets
        all_donations = sheets_manager.get_all_donations_from_sheets()
        print(f"📊 Google Sheets donations: {len(all_donations)}")
        
        if not all_donations:
            print("❌ No donations from Google Sheets")
            return
        
        # Test with first few donations
        test_donations = all_donations[:3]
        print(f"\n🧪 Testing with {len(test_donations)} donations:")
        
        for i, donation_data in enumerate(test_donations):
            print(f"\n--- Donation {i+1} ---")
            donor_id = str(donation_data.get('id', '')).strip()
            donor_name = donation_data.get('donor_name', 'N/A')
            amount = donation_data.get('amount', 0)
            
            print(f"   Google Sheets data:")
            print(f"      donor_id: '{donor_id}'")
            print(f"      donor_name: '{donor_name}'")
            print(f"      amount: {amount}")
            
            # Check if this donor_id exists in database
            existing_donation = None
            if donor_id:
                existing_donation = OfflineDonation.query.filter_by(donor_id=donor_id).first()
                print(f"   Database lookup:")
                print(f"      Searching for donor_id: '{donor_id}'")
                if existing_donation:
                    print(f"      ✅ Found existing: {existing_donation.donor_name} - ₹{existing_donation.amount}")
                else:
                    print(f"      ❌ Not found - will create new")
            else:
                print(f"   ❌ No donor_id - will create new")
            
            # Check if there's a donation with same name and amount (without donor_id)
            if not existing_donation:
                same_name_amount = OfflineDonation.query.filter_by(
                    donor_name=donor_name,
                    amount=amount
                ).first()
                if same_name_amount:
                    print(f"      🔍 Found by name+amount: {same_name_amount.donor_name} - ID: '{same_name_amount.donor_id}'")
                else:
                    print(f"      ❌ No match by name+amount")

if __name__ == "__main__":
    debug_sync_process()
