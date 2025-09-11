#!/usr/bin/env python3
"""
Check donor_id values in database directly
"""

import os
import sys

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation
from app import app

def check_donor_ids_db():
    """Check donor_id values in database"""
    print("🔍 Checking Donor IDs in Database")
    print("=" * 40)
    
    with app.app_context():
        # Get all donations
        all_donations = OfflineDonation.query.all()
        print(f"📊 Total donations: {len(all_donations)}")
        
        # Check donor_id values
        with_donor_id = [d for d in all_donations if d.donor_id]
        without_donor_id = [d for d in all_donations if not d.donor_id]
        
        print(f"📊 With donor_id: {len(with_donor_id)}")
        print(f"📊 Without donor_id: {len(without_donor_id)}")
        
        if with_donor_id:
            print(f"\n📋 Sample with donor_id:")
            for i, donation in enumerate(with_donor_id[:5]):
                print(f"   {i+1}. {donation.donor_name} - ID: '{donation.donor_id}' - Amount: ₹{donation.amount}")
        
        if without_donor_id:
            print(f"\n📋 Sample without donor_id:")
            for i, donation in enumerate(without_donor_id[:5]):
                print(f"   {i+1}. {donation.donor_name} - ID: '{donation.donor_id}' - Amount: ₹{donation.amount}")
        
        # Check for duplicates by donor_id
        duplicates = db.session.query(OfflineDonation.donor_id).filter(
            OfflineDonation.donor_id.isnot(None)
        ).group_by(OfflineDonation.donor_id).having(
            db.func.count(OfflineDonation.donor_id) > 1
        ).all()
        
        if duplicates:
            print(f"\n❌ Duplicate donor_ids: {len(duplicates)}")
            for dup in duplicates:
                print(f"   - {dup[0]}")
        else:
            print(f"\n✅ No duplicate donor_ids")

if __name__ == "__main__":
    check_donor_ids_db()
