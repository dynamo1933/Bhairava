#!/usr/bin/env python3
"""
Quick purge script - deletes all donations without confirmation
Use with extreme caution!
"""

import os
import sys

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from app import app

def quick_purge():
    """Quickly delete all donation records"""
    try:
        with app.app_context():
            # Get counts
            donation_count = OfflineDonation.query.count()
            purpose_count = DonationPurpose.query.count()
            
            print(f"🗑️  Purging {donation_count} donations and {purpose_count} purposes...")
            
            # Delete all records
            OfflineDonation.query.delete()
            DonationPurpose.query.delete()
            db.session.commit()
            
            print("✅ Purge completed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()

if __name__ == "__main__":
    if not os.path.exists("instance/daiva_anughara.db"):
        print("❌ Database not found")
        sys.exit(1)
    
    quick_purge()
