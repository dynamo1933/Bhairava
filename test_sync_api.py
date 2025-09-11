#!/usr/bin/env python3
"""
Test sync API endpoint properly
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose, User
from app import app

def test_sync_api():
    """Test sync API endpoint"""
    print("🧪 Testing Sync API Endpoint")
    print("=" * 40)
    
    with app.app_context():
        # Create a test admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print("❌ No admin user found")
            return
        
        print(f"✅ Found admin user: {admin_user.username}")
        
        # Test the sync API endpoint
        with app.test_client() as client:
            # Login as admin (simulate session)
            with client.session_transaction() as sess:
                sess['_user_id'] = str(admin_user.id)
                sess['_fresh'] = True
            
            print("🔄 Testing sync API endpoint...")
            response = client.post('/admin/api/sync-donations')
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📊 Response data: {response.get_json()}")
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print("✅ Sync API working correctly!")
                else:
                    print(f"❌ Sync failed: {data.get('error')}")
            else:
                print(f"❌ API error: {response.status_code}")

if __name__ == "__main__":
    test_sync_api()