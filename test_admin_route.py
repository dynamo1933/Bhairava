#!/usr/bin/env python3
"""
Test script to check what the admin route returns
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from app import app

def test_admin_route():
    """Test what the admin route returns"""
    print("🧪 Testing Admin Route Data")
    print("=" * 40)
    
    with app.app_context():
        # Simulate the admin_donations route logic
        try:
            # Always fetch from local database (after sync)
            data_source = "Local Database"
            
            # Get all donations from local database
            all_donations = OfflineDonation.query.order_by(OfflineDonation.donation_date.desc()).all()
            print(f"📊 All donations from DB: {len(all_donations)}")
            
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
            
            # Get all purposes for reference
            all_purposes = DonationPurpose.query.filter_by(is_active=True).all()
            
            # Get recent donations for stats (last 30 days)
            thirty_days_ago = datetime.now().date() - timedelta(days=30)
            recent_donations = OfflineDonation.query.filter(
                OfflineDonation.donation_date >= thirty_days_ago
            ).order_by(OfflineDonation.donation_date.desc()).limit(10).all()
            
            print(f"\n📊 Template Variables:")
            print(f"   all_worksheet_data: {len(all_worksheet_data)} categories")
            print(f"   total_donations: {total_donations}")
            print(f"   total_amount: ₹{total_amount:.2f}")
            print(f"   all_purposes: {len(all_purposes)}")
            print(f"   recent_donations: {len(recent_donations)}")
            print(f"   data_source: {data_source}")
            
            # Check if the template condition will work
            if all_worksheet_data:
                print(f"\n✅ Template will show tabs: {list(all_worksheet_data.keys())}")
            else:
                print(f"\n❌ Template will show 'No Donations Available' message")
                
        except Exception as e:
            print(f"❌ Error in admin route logic: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_admin_route()
