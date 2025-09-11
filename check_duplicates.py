#!/usr/bin/env python3
"""
Check for duplicate donor_ids in the database
"""

import os
import sys

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation
from app import app

def check_duplicates():
    """Check for duplicate donor_ids"""
    print("🔍 Checking for Duplicate Donor IDs")
    print("=" * 40)
    
    with app.app_context():
        # Get all donations
        all_donations = OfflineDonation.query.all()
        print(f"📊 Total donations in database: {len(all_donations)}")
        
        # Check for duplicates by donor_id
        duplicates = db.session.query(OfflineDonation.donor_id).filter(
            OfflineDonation.donor_id.isnot(None)
        ).group_by(OfflineDonation.donor_id).having(
            db.func.count(OfflineDonation.donor_id) > 1
        ).all()
        
        if duplicates:
            print(f"❌ Found {len(duplicates)} duplicate donor_ids:")
            for dup in duplicates:
                print(f"   - {dup[0]}")
        else:
            print("✅ No duplicate donor_ids found!")
        
        # Show unique donor_ids
        unique_donor_ids = set(d.donor_id for d in all_donations if d.donor_id)
        print(f"📊 Unique donor_ids: {len(unique_donor_ids)}")
        print(f"📋 Sample donor_ids: {list(unique_donor_ids)[:10]}")

if __name__ == "__main__":
    check_duplicates()
