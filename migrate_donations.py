#!/usr/bin/env python3
"""
Database migration script to add donation tables
Run this script to add the new donation-related tables to the database
"""

from app import app, db
from models import DonationPurpose, OfflineDonation

def migrate_donations():
    """Add donation tables to the database"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'donation_purpose' in tables:
                print("✅ DonationPurpose table created")
            else:
                print("❌ DonationPurpose table not found")
                
            if 'offline_donation' in tables:
                print("✅ OfflineDonation table created")
            else:
                print("❌ OfflineDonation table not found")
            
            # Create some sample donation purposes
            sample_purposes = [
                {
                    'name': 'Temple Maintenance',
                    'description': 'Funds for maintaining and upkeeping the sacred temple space, including cleaning, repairs, and general maintenance.',
                    'created_by': 1  # Assuming admin user has ID 1
                },
                {
                    'name': 'Spiritual Events',
                    'description': 'Support for organizing spiritual events, festivals, ceremonies, and special gatherings for the community.',
                    'created_by': 1
                },
                {
                    'name': 'Community Support',
                    'description': 'Helping devotees and community members in need, including food distribution and emergency assistance.',
                    'created_by': 1
                },
                {
                    'name': 'Educational Programs',
                    'description': 'Funding for spiritual education, workshops, classes, and learning materials for the community.',
                    'created_by': 1
                },
                {
                    'name': 'Garden & Environment',
                    'description': 'Maintaining the sacred garden, environmental projects, and creating a peaceful natural environment.',
                    'created_by': 1
                }
            ]
            
            # Add sample purposes if they don't exist
            for purpose_data in sample_purposes:
                existing = DonationPurpose.query.filter_by(name=purpose_data['name']).first()
                if not existing:
                    purpose = DonationPurpose(**purpose_data)
                    db.session.add(purpose)
                    print(f"✅ Added sample purpose: {purpose_data['name']}")
                else:
                    print(f"ℹ️  Purpose already exists: {purpose_data['name']}")
            
            db.session.commit()
            print("✅ Sample donation purposes added successfully!")
            
            print("\n🎉 Donation system migration completed successfully!")
            print("\nNext steps:")
            print("1. Set up Google Sheets credentials (google_credentials.json)")
            print("2. Configure the Google Sheets ID in google_sheets.py")
            print("3. Test the donation system by adding a sample donation")
            print("4. Access admin panel to manage donations and purposes")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_donations()

