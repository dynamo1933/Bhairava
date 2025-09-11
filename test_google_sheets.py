#!/usr/bin/env python3
"""
Test script for Google Sheets integration
This script tests fetching donations from the Google Sheets
"""

from app import app
from google_sheets import sheets_manager

def test_google_sheets_integration():
    """Test Google Sheets integration"""
    with app.app_context():
        try:
            print("🧪 Testing Google Sheets Integration...")
            
            # Test 1: Connection test
            print("\n1. Testing Google Sheets connection...")
            if sheets_manager.test_connection():
                print("   ✅ Google Sheets connection successful")
            else:
                print("   ❌ Google Sheets connection failed")
                print("   ℹ️  Make sure you have set up google_credentials.json")
                return False
            
            # Test 2: Get all donations
            print("\n2. Fetching donations from Google Sheets...")
            donations = sheets_manager.get_all_donations_from_sheets()
            print(f"   ✅ Found {len(donations)} donations in Google Sheets")
            
            if donations:
                print("   📋 Sample donation data:")
                for i, donation in enumerate(donations[:3]):  # Show first 3
                    print(f"      {i+1}. {donation.get('donor_name', 'N/A')} - {donation.get('amount', 0)} {donation.get('currency', 'INR')} - {donation.get('purpose', 'N/A')}")
            
            # Test 3: Get summary
            print("\n3. Getting donations summary...")
            summary = sheets_manager.get_donations_summary()
            print(f"   ✅ Found {len(summary)} purpose categories")
            
            for purpose, data in summary.items():
                print(f"      {purpose}: {data['total_donations']} donations, {data['total_amount']} total")
            
            # Test 4: Test API endpoint
            print("\n4. Testing API endpoint...")
            from app import api_donations_from_sheets
            with app.test_client() as client:
                response = client.get('/api/donations-from-sheets')
                if response.status_code == 200:
                    data = response.get_json()
                    if data['success']:
                        print(f"   ✅ API endpoint working - {data['count']} donations")
                    else:
                        print(f"   ❌ API endpoint error: {data['error']}")
                else:
                    print(f"   ❌ API endpoint failed with status {response.status_code}")
            
            print("\n🎉 Google Sheets integration test completed!")
            print("\nNext steps:")
            print("1. Visit /donations to see the public donations page")
            print("2. Login as admin and go to Admin > Donation Management")
            print("3. Click 'Sync from Sheets' to sync donations to local database")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return False

if __name__ == '__main__':
    test_google_sheets_integration()

