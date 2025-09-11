#!/usr/bin/env python3
"""
Setup script for the donation system
This script helps you get started with the donation system
"""

import os
import sys

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    try:
        import flask
        print("   ✅ Flask installed")
    except ImportError:
        print("   ❌ Flask not installed")
        return False
    
    try:
        import gspread
        print("   ✅ gspread installed")
    except ImportError:
        print("   ❌ gspread not installed")
        return False
    
    try:
        import google.auth
        print("   ✅ google-auth installed")
    except ImportError:
        print("   ❌ google-auth not installed")
        return False
    
    return True

def check_google_credentials():
    """Check if Google credentials file exists"""
    print("\n🔍 Checking Google credentials...")
    
    if os.path.exists('google_credentials.json'):
        print("   ✅ google_credentials.json found")
        return True
    else:
        print("   ❌ google_credentials.json not found")
        print("   ℹ️  Please follow the setup guide in GOOGLE_SHEETS_SETUP.md")
        return False

def setup_database():
    """Set up the database"""
    print("\n🗄️  Setting up database...")
    
    try:
        from migrate_donations import migrate_donations
        migrate_donations()
        print("   ✅ Database setup completed")
        return True
    except Exception as e:
        print(f"   ❌ Database setup failed: {e}")
        return False

def test_google_sheets():
    """Test Google Sheets connection"""
    print("\n🌐 Testing Google Sheets connection...")
    
    try:
        from test_google_sheets import test_google_sheets_integration
        if test_google_sheets_integration():
            print("   ✅ Google Sheets integration working")
            return True
        else:
            print("   ⚠️  Google Sheets integration has issues")
            return False
    except Exception as e:
        print(f"   ❌ Google Sheets test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Daiva Anughara Donation System Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install requirements first:")
        print("   pip install -r requirements.txt")
        return False
    
    # Check Google credentials
    has_credentials = check_google_credentials()
    
    # Setup database
    if not setup_database():
        print("\n❌ Database setup failed")
        return False
    
    # Test Google Sheets if credentials are available
    if has_credentials:
        test_google_sheets()
    else:
        print("\n⚠️  Skipping Google Sheets test (no credentials)")
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Start the application: python app.py")
    print("2. Visit http://localhost:5000/donations to see the public page")
    print("3. Login as admin (admin/admin123) to manage donations")
    
    if not has_credentials:
        print("4. Set up Google Sheets credentials for full functionality")
        print("   (See GOOGLE_SHEETS_SETUP.md for instructions)")
    
    return True

if __name__ == '__main__':
    main()

