#!/usr/bin/env python3
"""
Delete all donation records without donor_id
This is a one-time cleanup script
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation
from app import app

def delete_records_without_donor_id():
    """Delete all records without donor_id"""
    print("🗑️  Deleting Records Without Donor ID")
    print("=" * 50)
    
    with app.app_context():
        # Get current counts
        total_donations = OfflineDonation.query.count()
        without_donor_id = OfflineDonation.query.filter(OfflineDonation.donor_id.is_(None)).count()
        with_donor_id = OfflineDonation.query.filter(OfflineDonation.donor_id.isnot(None)).count()
        
        print(f"📊 Current database state:")
        print(f"   Total donations: {total_donations}")
        print(f"   With donor_id: {with_donor_id}")
        print(f"   Without donor_id: {without_donor_id}")
        
        if without_donor_id == 0:
            print("✅ No records without donor_id found. Nothing to delete.")
            return
        
        # Show sample records that will be deleted
        print(f"\n📋 Sample records to be deleted:")
        sample_records = OfflineDonation.query.filter(OfflineDonation.donor_id.is_(None)).limit(5).all()
        for i, record in enumerate(sample_records):
            print(f"   {i+1}. {record.donor_name} - ₹{record.amount} - {record.purpose.name if record.purpose else 'No Purpose'}")
        
        # Confirmation
        print(f"\n⚠️  WARNING: This will permanently delete {without_donor_id} records!")
        print("This action cannot be undone.")
        
        while True:
            response = input(f"\nAre you sure you want to delete {without_donor_id} records without donor_id? (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                break
            elif response in ['no', 'n']:
                print("❌ Operation cancelled by user")
                return
            else:
                print("Please enter 'yes' or 'no'")
        
        try:
            # Delete records without donor_id
            print(f"\n🔄 Deleting {without_donor_id} records...")
            deleted_count = OfflineDonation.query.filter(OfflineDonation.donor_id.is_(None)).delete()
            
            # Commit changes
            db.session.commit()
            
            print(f"✅ Successfully deleted {deleted_count} records")
            
            # Show final state
            final_total = OfflineDonation.query.count()
            final_with_donor_id = OfflineDonation.query.filter(OfflineDonation.donor_id.isnot(None)).count()
            
            print(f"\n📊 Final database state:")
            print(f"   Total donations: {final_total}")
            print(f"   With donor_id: {final_with_donor_id}")
            print(f"   Without donor_id: {final_total - final_with_donor_id}")
            
            if final_total - final_with_donor_id == 0:
                print("✅ All remaining records have donor_id!")
            else:
                print("⚠️  Some records still don't have donor_id")
                
        except Exception as e:
            print(f"❌ Error during deletion: {e}")
            db.session.rollback()
            print("🔄 Database rollback completed")

if __name__ == "__main__":
    delete_records_without_donor_id()
