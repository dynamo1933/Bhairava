#!/usr/bin/env python3
"""
Debug script to check what donor_id values are coming from Google Sheets
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from google_sheets import sheets_manager
from app import app

def debug_sync():
    """Debug the sync process to see donor_id values"""
    print("🔍 Debugging Sync Process")
    print("=" * 50)
    
    with app.app_context():
        # Get all donations from Google Sheets
        all_donations = sheets_manager.get_all_donations_from_sheets()
        print(f"📊 Total donations from Google Sheets: {len(all_donations)}")
        
        # Check first few donations for donor_id
        print(f"\n📋 Sample donations from Google Sheets:")
        for i, donation in enumerate(all_donations[:5]):
            donor_id = str(donation.get('id', '')).strip()
            print(f"   {i+1}. ID: '{donor_id}' | Name: {donation.get('donor_name', 'N/A')} | Amount: {donation.get('amount', 'N/A')}")
        
        # Check current database state
        print(f"\n📊 Current database state:")
        db_donations = OfflineDonation.query.all()
        print(f"   Total donations in DB: {len(db_donations)}")
        
        # Check for duplicates by donor_id
        donor_ids_in_db = [d.donor_id for d in db_donations if d.donor_id]
        unique_donor_ids = set(donor_ids_in_db)
        print(f"   Unique donor_ids in DB: {len(unique_donor_ids)}")
        print(f"   Sample donor_ids in DB: {list(unique_donor_ids)[:5]}")
        
        # Check for duplicates
        duplicates = db.session.query(OfflineDonation.donor_id).filter(
            OfflineDonation.donor_id.isnot(None)
        ).group_by(OfflineDonation.donor_id).having(
            db.func.count(OfflineDonation.donor_id) > 1
        ).all()
        
        if duplicates:
            print(f"   ❌ Duplicate donor_ids found: {len(duplicates)}")
            for dup in duplicates[:5]:
                print(f"      - {dup[0]}")
        else:
            print(f"   ✅ No duplicate donor_ids found")
        
        # Check if Google Sheets has donor_id values
        sheets_donor_ids = [str(d.get('id', '')).strip() for d in all_donations if str(d.get('id', '')).strip()]
        print(f"\n📊 Google Sheets donor_id analysis:")
        print(f"   Donations with donor_id: {len(sheets_donor_ids)}")
        print(f"   Sample donor_ids from sheets: {sheets_donor_ids[:5]}")
        
        if not sheets_donor_ids:
            print("   ❌ No donor_id values found in Google Sheets!")
        else:
            print("   ✅ donor_id values found in Google Sheets")

if __name__ == "__main__":
    debug_sync()
