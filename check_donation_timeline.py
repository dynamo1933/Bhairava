#!/usr/bin/env python3
"""
Check the timeline of donations to understand the data
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation
from app import app

def check_donation_timeline():
    """Check donation timeline"""
    print("🔍 Checking Donation Timeline")
    print("=" * 40)
    
    with app.app_context():
        # Get all donations ordered by creation date
        all_donations = OfflineDonation.query.order_by(OfflineDonation.created_at.asc()).all()
        print(f"📊 Total donations: {len(all_donations)}")
        
        # Group by donor_id status
        with_donor_id = [d for d in all_donations if d.donor_id]
        without_donor_id = [d for d in all_donations if not d.donor_id]
        
        print(f"📊 With donor_id: {len(with_donor_id)}")
        print(f"📊 Without donor_id: {len(without_donor_id)}")
        
        if with_donor_id:
            print(f"\n📋 First few with donor_id:")
            for i, donation in enumerate(with_donor_id[:5]):
                print(f"   {i+1}. {donation.donor_name} - ID: '{donation.donor_id}' - Created: {donation.created_at}")
        
        if without_donor_id:
            print(f"\n📋 First few without donor_id:")
            for i, donation in enumerate(without_donor_id[:5]):
                print(f"   {i+1}. {donation.donor_name} - ID: '{donation.donor_id}' - Created: {donation.created_at}")
        
        # Check if we can identify patterns
        print(f"\n📊 Analysis:")
        print(f"   Oldest donation: {min(d.created_at for d in all_donations)}")
        print(f"   Newest donation: {max(d.created_at for d in all_donations)}")
        
        # Check if donations without donor_id are older
        if without_donor_id and with_donor_id:
            oldest_without = min(d.created_at for d in without_donor_id)
            oldest_with = min(d.created_at for d in with_donor_id)
            print(f"   Oldest without donor_id: {oldest_without}")
            print(f"   Oldest with donor_id: {oldest_with}")
            
            if oldest_without < oldest_with:
                print(f"   ✅ Donations without donor_id are older (as expected)")
            else:
                print(f"   ❌ Unexpected: donations with donor_id are older")

if __name__ == "__main__":
    check_donation_timeline()
