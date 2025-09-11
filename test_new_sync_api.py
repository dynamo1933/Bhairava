#!/usr/bin/env python3
"""
Test new sync endpoint
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose, User
from app import app

def test_new_sync_api():
    """Test new sync endpoint"""
    print("🧪 Testing New Sync Endpoint")
    print("=" * 40)
    
    with app.app_context():
        # Check admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print("❌ No admin user found")
            return
        print(f"✅ Admin user: {admin_user.username}")
        
        # Test the new sync endpoint
        with app.test_client() as client:
            # Login as admin
            with client.session_transaction() as sess:
                sess['_user_id'] = str(admin_user.id)
                sess['_fresh'] = True
            
            print("🔄 Testing new sync endpoint...")
            
            try:
                response = client.get('/admin/sync-now')
                print(f"📡 Response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    print(f"📊 Response data: {data}")
                    if data.get('success'):
                        print("✅ Sync successful!")
                    else:
                        print(f"❌ Sync failed: {data.get('error')}")
                else:
                    print(f"❌ Error response: {response.get_data(as_text=True)}")
                    
            except Exception as e:
                print(f"❌ Request error: {e}")

if __name__ == "__main__":
    test_new_sync_api()
