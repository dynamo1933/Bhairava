#!/usr/bin/env python3
"""
Test script to check what data the admin page should display
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from app import app

def test_admin_data():
    """Test what data the admin page should display"""
    print("🧪 Testing Admin Page Data")
    print("=" * 40)
    
    with app.app_context():
        # Get all donations from local database (same as admin page)
        all_donations = OfflineDonation.query.order_by(OfflineDonation.donation_date.desc()).all()
        print(f"📊 Total donations in database: {len(all_donations)}")
        
        # Group donations by purpose
        all_worksheet_data = {}
        total_donations = 0
        total_amount = 0
        
        # Group by purpose
        purposes_dict = {}
        for donation in all_donations:
            purpose_name = donation.purpose.name if donation.purpose else 'Uncategorized'
            if purpose_name not in purposes_dict:
                purposes_dict[purpose_name] = []
            purposes_dict[purpose_name].append(donation)
        
        print(f"📋 Purposes found: {list(purposes_dict.keys())}")
        
        # Create worksheet data structure
        for purpose_name, donations in purposes_dict.items():
            purpose_amount = sum(float(d.amount) for d in donations)
            all_worksheet_data[purpose_name] = {
                'donations': donations,
                'summary': {
                    'total_donations': len(donations),
                    'total_amount': purpose_amount,
                    'verified_donations': len([d for d in donations if d.is_verified]),
                    'pending_donations': len([d for d in donations if not d.is_verified]),
                    'average_donation': purpose_amount / len(donations) if donations else 0
                },
                'all_donations': donations
            }
            
            total_donations += len(donations)
            total_amount += purpose_amount
            
            print(f"   📁 {purpose_name}: {len(donations)} donations, ₹{purpose_amount:.2f}")
        
        print(f"\n📊 Summary:")
        print(f"   Total Donations: {total_donations}")
        print(f"   Total Amount: ₹{total_amount:.2f}")
        print(f"   Categories: {len(all_worksheet_data)}")
        
        # Check if there are any purposes in the database
        all_purposes = DonationPurpose.query.filter_by(is_active=True).all()
        print(f"   Active Purposes in DB: {len(all_purposes)}")
        
        # Show first few donations as example
        if all_donations:
            print(f"\n📋 Sample donations:")
            for i, donation in enumerate(all_donations[:3]):
                print(f"   {i+1}. {donation.donor_name} - ₹{donation.amount} ({donation.purpose.name if donation.purpose else 'No Purpose'})")

if __name__ == "__main__":
    test_admin_data()
