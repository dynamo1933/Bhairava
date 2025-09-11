#!/usr/bin/env python3
"""
Render Deployment Setup Helper
This script helps you set up Google Sheets credentials for Render deployment
"""

import json
import os

def create_render_env_vars():
    """Create environment variables for Render deployment"""
    
    # Check if credentials file exists
    if not os.path.exists('google_credentials.json'):
        print("❌ google_credentials.json not found!")
        print("Please create the credentials file first by following GOOGLE_SHEETS_SETUP.md")
        return False
    
    # Read the credentials file
    with open('google_credentials.json', 'r') as f:
        credentials = json.load(f)
    
    # Create the environment variable value
    credentials_json = json.dumps(credentials)
    
    print("🔧 Render Deployment Setup")
    print("=" * 50)
    print()
    print("📋 Follow these steps to configure your Render deployment:")
    print()
    print("1. Go to your Render dashboard: https://dashboard.render.com")
    print("2. Select your 'daiva-anughara' service")
    print("3. Go to 'Environment' tab")
    print("4. Add the following environment variable:")
    print()
    print("   Variable Name: GOOGLE_CREDENTIALS_JSON")
    print("   Variable Value:")
    print("   " + credentials_json)
    print()
    print("5. Click 'Save Changes'")
    print("6. Redeploy your service")
    print()
    print("🔍 Alternative: Copy this command to set the environment variable:")
    print(f"export GOOGLE_CREDENTIALS_JSON='{credentials_json}'")
    print()
    print("✅ After setting the environment variable and redeploying,")
    print("   your donations page should show data from Google Sheets!")
    
    return True

def verify_credentials():
    """Verify that the credentials are valid"""
    try:
        with open('google_credentials.json', 'r') as f:
            credentials = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email', 'client_id']
        missing_fields = [field for field in required_fields if field not in credentials]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        print("✅ Credentials file is valid")
        print(f"   Project ID: {credentials['project_id']}")
        print(f"   Client Email: {credentials['client_email']}")
        return True
        
    except Exception as e:
        print(f"❌ Error reading credentials file: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Daiva Anughara - Render Deployment Setup")
    print("=" * 50)
    print()
    
    if verify_credentials():
        create_render_env_vars()
    else:
        print("Please fix the credentials file first.")
