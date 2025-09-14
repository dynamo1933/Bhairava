#!/usr/bin/env python3
"""
Test script for Mandala Sadhana functionality
"""

from app import app, db
from models import MandalaSadhanaRegistration
from datetime import datetime, date

def test_mandala_sadhana():
    """Test Mandala Sadhana registration functionality"""
    with app.app_context():
        try:
            # Test creating a registration
            test_registration = MandalaSadhanaRegistration(
                email="test@example.com",
                full_name="Test User - Mumbai, India",
                mandala_48_commitment=True,
                mandala_144_commitment="Yes",
                commitment_text="I am committed to this sacred practice with full dedication and sincerity.",
                sadhana_start_date=date.today(),
                sadhana_type="Aṣṭamī Sādhana",
                send_copy=True
            )
            
            db.session.add(test_registration)
            db.session.commit()
            
            print("✅ Test registration created successfully!")
            print(f"   ID: {test_registration.id}")
            print(f"   Name: {test_registration.full_name}")
            print(f"   Email: {test_registration.email}")
            print(f"   48-Day Commitment: {test_registration.mandala_48_commitment}")
            print(f"   144-Day Commitment: {test_registration.mandala_144_commitment}")
            print(f"   Sadhana Type: {test_registration.sadhana_type}")
            
            # Test querying registrations
            all_registrations = MandalaSadhanaRegistration.query.all()
            print(f"\n✅ Total registrations in database: {len(all_registrations)}")
            
            # Test filtering
            ashtami_registrations = MandalaSadhanaRegistration.query.filter_by(sadhana_type="Aṣṭamī Sādhana").all()
            print(f"✅ Aṣṭamī Sādhana registrations: {len(ashtami_registrations)}")
            
            # Test to_dict method
            registration_dict = test_registration.to_dict()
            print(f"\n✅ Registration as dictionary: {registration_dict}")
            
            # Clean up test data
            db.session.delete(test_registration)
            db.session.commit()
            print("\n✅ Test registration cleaned up successfully!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing Mandala Sadhana functionality: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🔄 Testing Mandala Sadhana functionality...")
    success = test_mandala_sadhana()
    
    if success:
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n💥 Tests failed!")

