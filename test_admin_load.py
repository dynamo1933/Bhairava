#!/usr/bin/env python3
"""
Test admin page load without Google Sheets connection
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from app import app

def test_admin_page_load():
    """Test admin page load without Google Sheets connection"""
    print("🧪 Testing Admin Page Load")
    print("=" * 40)
    
    with app.app_context():
        print("✅ App context created")
        
        # Test the admin donations route logic
        try:
            # Get all donations from local database
            all_donations = OfflineDonation.query.order_by(OfflineDonation.donation_date.desc()).all()
            print(f"📊 Found {len(all_donations)} donations in database")
            
            # Group donations by worksheet
            worksheets_dict = {}
            for donation in all_donations:
                worksheet_name = donation.worksheet if donation.worksheet else (donation.purpose.name if donation.purpose else 'Uncategorized')
                if worksheet_name not in worksheets_dict:
                    worksheets_dict[worksheet_name] = []
                worksheets_dict[worksheet_name].append(donation)
            
            print(f"📋 Found {len(worksheets_dict)} worksheets:")
            for worksheet_name, donations in worksheets_dict.items():
                total_amount = sum(d.amount for d in donations)
                print(f"   {worksheet_name}: {len(donations)} donations, ₹{total_amount:.2f}")
            
            print("✅ Admin page data prepared successfully without Google Sheets connection")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_admin_page_load()
