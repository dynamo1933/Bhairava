#!/usr/bin/env python3
"""
Check current data distribution in the database
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from app import app

def check_current_data():
    """Check current data distribution"""
    print("🔍 Checking Current Data Distribution")
    print("=" * 50)
    
    with app.app_context():
        # Get all donations
        all_donations = OfflineDonation.query.all()
        print(f"📊 Total donations: {len(all_donations)}")
        
        # Group by purpose
        purposes_dict = {}
        for donation in all_donations:
            purpose_name = donation.purpose.name if donation.purpose else 'Uncategorized'
            if purpose_name not in purposes_dict:
                purposes_dict[purpose_name] = []
            purposes_dict[purpose_name].append(donation)
        
        print(f"\n📋 Donations by Purpose:")
        for purpose_name, donations in purposes_dict.items():
            total_amount = sum(d.amount for d in donations)
            print(f"   {purpose_name}: {len(donations)} donations, ₹{total_amount:.2f}")
        
        # Check if we need to sync from Google Sheets to get more data
        print(f"\n🔄 Checking if we need to sync from Google Sheets...")
        from google_sheets import sheets_manager
        
        if sheets_manager.is_connected():
            sheets_data = sheets_manager.get_all_donations_from_sheets()
            print(f"   Google Sheets has {len(sheets_data)} donations")
            
            # Group by worksheet
            worksheets_dict = {}
            for donation in sheets_data:
                worksheet_name = donation.get('purpose', 'Uncategorized')
                if worksheet_name not in worksheets_dict:
                    worksheets_dict[worksheet_name] = []
                worksheets_dict[worksheet_name].append(donation)
            
            print(f"\n📋 Google Sheets by Worksheet:")
            for worksheet_name, donations in worksheets_dict.items():
                total_amount = sum(float(d.get('amount', 0)) for d in donations)
                print(f"   {worksheet_name}: {len(donations)} donations, ₹{total_amount:.2f}")
        else:
            print("   ❌ Google Sheets not connected")

if __name__ == "__main__":
    check_current_data()
