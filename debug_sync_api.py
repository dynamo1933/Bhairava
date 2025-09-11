#!/usr/bin/env python3
"""
Debug sync API endpoint step by step
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose, User
from app import app
from google_sheets import get_sheets_manager

def debug_sync_api():
    """Debug sync API endpoint step by step"""
    print("🔍 Debugging Sync API Endpoint")
    print("=" * 40)
    
    with app.app_context():
        # Check admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print("❌ No admin user found")
            return
        print(f"✅ Admin user: {admin_user.username}")
        
        # Check Google Sheets connection
        try:
            sheets_manager = get_sheets_manager()
            print(f"✅ Sheets manager created")
            
            is_connected = sheets_manager.is_connected()
            print(f"📊 Google Sheets connected: {is_connected}")
            
            if not is_connected:
                print("❌ Google Sheets not connected - this is why sync fails")
                return
                
        except Exception as e:
            print(f"❌ Error checking Google Sheets: {e}")
            return
        
        # Test the sync API endpoint with detailed logging
        with app.test_client() as client:
            # Login as admin
            with client.session_transaction() as sess:
                sess['_user_id'] = str(admin_user.id)
                sess['_fresh'] = True
            
            print("🔄 Testing sync API endpoint...")
            
            # Make the request and capture any errors
            try:
                response = client.post('/admin/api/sync-donations')
                print(f"📡 Response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    print(f"📊 Response data: {data}")
                else:
                    print(f"❌ Error response: {response.get_data(as_text=True)}")
                    
            except Exception as e:
                print(f"❌ Request error: {e}")

if __name__ == "__main__":
    debug_sync_api()
