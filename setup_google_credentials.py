#!/usr/bin/env python3
"""
Google Sheets credentials setup helper
This script helps you set up Google Sheets credentials
"""

import os
import json

def create_sample_credentials():
    """Create a sample credentials file with instructions"""
    sample_credentials = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
    }
    
    with open('google_credentials_sample.json', 'w') as f:
        json.dump(sample_credentials, f, indent=2)
    
    print("✅ Created google_credentials_sample.json")
    print("📝 Instructions:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable Google Sheets API")
    print("4. Create a service account")
    print("5. Download the JSON key file")
    print("6. Rename it to 'google_credentials.json'")
    print("7. Place it in this directory")
    print("8. Share your Google Sheet with the service account email")

def check_credentials():
    """Check if credentials file exists and is valid"""
    if not os.path.exists('google_credentials.json'):
        print("❌ google_credentials.json not found")
        return False
    
    try:
        with open('google_credentials.json', 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        for field in required_fields:
            if field not in creds:
                print(f"❌ Missing required field: {field}")
                return False
        
        if creds['type'] != 'service_account':
            print("❌ Invalid credentials type")
            return False
        
        print("✅ google_credentials.json looks valid")
        return True
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON in google_credentials.json")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials: {e}")
        return False

def test_connection():
    """Test Google Sheets connection"""
    try:
        from google_sheets import sheets_manager
        
        if sheets_manager.is_connected():
            print("✅ Google Sheets connection successful!")
            return True
        else:
            print("❌ Google Sheets connection failed")
            return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def main():
    """Main setup function"""
    print("🔧 Google Sheets Credentials Setup")
    print("=" * 40)
    
    # Check if credentials already exist
    if check_credentials():
        print("\n🧪 Testing connection...")
        if test_connection():
            print("\n🎉 Google Sheets integration is working!")
            return True
        else:
            print("\n❌ Connection test failed")
            return False
    else:
        print("\n📝 Creating sample credentials file...")
        create_sample_credentials()
        print("\n📖 Please follow the instructions above to set up your credentials")
        return False

if __name__ == '__main__':
    main()

