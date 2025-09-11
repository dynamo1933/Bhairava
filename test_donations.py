#!/usr/bin/env python3
"""
Test script for the donation system
Run this to verify the donation functionality works correctly
"""

from app import app, db
from models import DonationPurpose, OfflineDonation, User
from datetime import datetime, date

def test_donation_system():
    """Test the donation system functionality"""
    with app.app_context():
        try:
            print("🧪 Testing Donation System...")
            
            # Test 1: Check if tables exist
            print("\n1. Checking database tables...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['donation_purpose', 'offline_donation']
            for table in required_tables:
                if table in tables:
                    print(f"   ✅ {table} table exists")
                else:
                    print(f"   ❌ {table} table missing")
                    return False
            
            # Test 2: Create a test donation purpose
            print("\n2. Testing donation purpose creation...")
            test_purpose = DonationPurpose(
                name="Test Purpose",
                description="A test purpose for donation system testing",
                created_by=1
            )
            
            # Check if test purpose already exists
            existing = DonationPurpose.query.filter_by(name="Test Purpose").first()
            if existing:
                print("   ℹ️  Test purpose already exists")
                test_purpose = existing
            else:
                db.session.add(test_purpose)
                db.session.commit()
                print("   ✅ Test purpose created successfully")
            
            # Test 3: Create a test donation
            print("\n3. Testing donation creation...")
            test_donation = OfflineDonation(
                donor_name="Test Donor",
                donor_email="test@example.com",
                donor_phone="1234567890",
                amount=100.50,
                currency="INR",
                purpose_id=test_purpose.id,
                donation_date=date.today(),
                payment_method="Cash",
                reference_number="TEST001",
                notes="Test donation for system testing",
                created_by=1
            )
            
            # Check if test donation already exists
            existing_donation = OfflineDonation.query.filter_by(reference_number="TEST001").first()
            if existing_donation:
                print("   ℹ️  Test donation already exists")
                test_donation = existing_donation
            else:
                db.session.add(test_donation)
                db.session.commit()
                print("   ✅ Test donation created successfully")
            
            # Test 4: Test relationships
            print("\n4. Testing relationships...")
            purpose_donations = test_purpose.donations
            print(f"   ✅ Purpose has {len(purpose_donations)} donations")
            
            donation_purpose = test_donation.purpose
            print(f"   ✅ Donation belongs to purpose: {donation_purpose.name}")
            
            # Test 5: Test verification
            print("\n5. Testing donation verification...")
            if not test_donation.is_verified:
                test_donation.is_verified = True
                test_donation.verified_at = datetime.now()
                test_donation.verified_by = 1
                db.session.commit()
                print("   ✅ Donation verified successfully")
            else:
                print("   ℹ️  Donation already verified")
            
            # Test 6: Test queries
            print("\n6. Testing queries...")
            all_purposes = DonationPurpose.query.all()
            print(f"   ✅ Found {len(all_purposes)} donation purposes")
            
            all_donations = OfflineDonation.query.all()
            print(f"   ✅ Found {len(all_donations)} donations")
            
            verified_donations = OfflineDonation.query.filter_by(is_verified=True).all()
            print(f"   ✅ Found {len(verified_donations)} verified donations")
            
            # Test 7: Test Google Sheets integration (if credentials exist)
            print("\n7. Testing Google Sheets integration...")
            try:
                from google_sheets import sheets_manager
                if sheets_manager.test_connection():
                    print("   ✅ Google Sheets connection successful")
                else:
                    print("   ⚠️  Google Sheets connection failed (credentials may be missing)")
            except Exception as e:
                print(f"   ⚠️  Google Sheets test failed: {e}")
            
            print("\n🎉 All tests completed successfully!")
            print("\nNext steps:")
            print("1. Run the application: python app.py")
            print("2. Login as admin and go to Admin > Donation Management")
            print("3. Add some real donations")
            print("4. Check the public donations page: /donations")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    test_donation_system()
