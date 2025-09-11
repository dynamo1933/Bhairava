#!/usr/bin/env python3
"""
Debug why donor_id is not being saved to database
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from google_sheets import sheets_manager
from app import app

def debug_donor_id_sync():
    """Debug donor_id sync issue"""
    print("🔍 Debugging Donor ID Sync Issue")
    print("=" * 50)
    
    with app.app_context():
        # Check current database state
        all_donations = OfflineDonation.query.all()
        print(f"📊 Total donations in DB: {len(all_donations)}")
        
        # Check how many have donor_id
        with_donor_id = [d for d in all_donations if d.donor_id]
        without_donor_id = [d for d in all_donations if not d.donor_id]
        
        print(f"📊 Donations with donor_id: {len(with_donor_id)}")
        print(f"📊 Donations without donor_id: {len(without_donor_id)}")
        
        if with_donor_id:
            print(f"📋 Sample with donor_id:")
            for i, donation in enumerate(with_donor_id[:3]):
                print(f"   {i+1}. {donation.donor_name} - ID: {donation.donor_id}")
        
        if without_donor_id:
            print(f"📋 Sample without donor_id:")
            for i, donation in enumerate(without_donor_id[:3]):
                print(f"   {i+1}. {donation.donor_name} - ID: {donation.donor_id}")
        
        # Check Google Sheets data
        print(f"\n📊 Google Sheets data:")
        sheets_data = sheets_manager.get_all_donations_from_sheets()
        print(f"   Total records: {len(sheets_data)}")
        
        if sheets_data:
            print(f"   Sample records:")
            for i, record in enumerate(sheets_data[:3]):
                donor_id = str(record.get('id', '')).strip()
                print(f"   {i+1}. {record.get('donor_name', 'N/A')} - ID: '{donor_id}'")
        
        # Test a single sync to see what happens
        print(f"\n🧪 Testing single record sync...")
        if sheets_data:
            test_record = sheets_data[0]
            donor_id = str(test_record.get('id', '')).strip()
            print(f"   Test record ID: '{donor_id}'")
            print(f"   Test record name: {test_record.get('donor_name', 'N/A')}")
            
            # Check if this donor_id exists in DB
            existing = OfflineDonation.query.filter_by(donor_id=donor_id).first()
            if existing:
                print(f"   ✅ Found existing record with this donor_id")
                print(f"      Name: {existing.donor_name}, Amount: {existing.amount}")
            else:
                print(f"   ❌ No existing record found with this donor_id")

if __name__ == "__main__":
    debug_donor_id_sync()
