#!/usr/bin/env python3
"""
Database Migration Script: SQLite to PostgreSQL

This script migrates data from the existing SQLite database to PostgreSQL.

Usage:
1. Make sure you have installed psycopg2-binary: pip install psycopg2-binary
2. Update the PostgreSQL connection string in the CONFIG section below
3. Run: python migrate_to_postgresql.py
4. The script will create tables and migrate all data

WARNING: This will overwrite any existing data in the PostgreSQL database!
"""

import sys
import os
from datetime import datetime

# Database URLs
SQLITE_URL = 'sqlite:///instance/daiva_anughara.db'
# PostgreSQL connection - Session Pooler (IPv4 compatible)
# Password contains @ which needs to be URL-encoded as %40
POSTGRESQL_URL = 'postgresql://postgres.cuyilngsmocyhadlbrgv:_Bottlemepani%4035@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres'

def create_flask_app(database_url):
    """Create Flask app with specified database URL"""
    from flask import Flask
    from models import db
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app, db

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    print("🕉️ Daiva Anughara - Database Migration: SQLite to PostgreSQL")
    print("=" * 70)
    
    # Create Flask apps for both databases
    print("\n1️⃣ Setting up database connections...")
    sqlite_app, sqlite_db = create_flask_app(SQLITE_URL)
    postgres_app, postgres_db = create_flask_app(POSTGRESQL_URL)
    
    # Import models
    from models import User, DonationPurpose, OfflineDonation, MandalaSadhanaRegistration
    
    # Check if SQLite database exists
    sqlite_path = 'instance/daiva_anughara.db'
    if not os.path.exists(sqlite_path):
        print(f"\n❌ SQLite database not found at: {sqlite_path}")
        print("   Nothing to migrate. Exiting...")
        return False
    
    with sqlite_app.app_context():
        # Get all data from SQLite
        print("\n2️⃣ Reading data from SQLite database...")
        users = User.query.all()
        donation_purposes = DonationPurpose.query.all()
        offline_donations = OfflineDonation.query.all()
        mandala_registrations = MandalaSadhanaRegistration.query.all()
        
        print(f"   ✓ Found {len(users)} users")
        print(f"   ✓ Found {len(donation_purposes)} donation purposes")
        print(f"   ✓ Found {len(offline_donations)} offline donations")
        print(f"   ✓ Found {len(mandala_registrations)} mandala registrations")
    
    # Confirmation
    print("\n⚠️  WARNING: This will create tables and migrate data to PostgreSQL.")
    response = input("   Do you want to continue? (type 'yes' to confirm): ")
    
    if response.lower() != 'yes':
        print("\n❌ Migration cancelled.")
        return False
    
    with postgres_app.app_context():
        print("\n3️⃣ Creating tables in PostgreSQL...")
        postgres_db.drop_all()  # Drop existing tables
        postgres_db.create_all()  # Create fresh tables
        print("   ✓ Tables created successfully")
        
        print("\n4️⃣ Migrating data to PostgreSQL...")
        
        # Migrate Users
        print("   → Migrating users...")
        for user in users:
            new_user = User(
                id=user.id,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                full_name=user.full_name,
                phone=user.phone,
                address=user.address,
                role=user.role,
                is_approved=user.is_approved,
                is_active=user.is_active,
                created_at=user.created_at,
                approved_at=user.approved_at,
                approved_by=user.approved_by,
                practice_level=user.practice_level,
                purpose=user.purpose,
                profile_picture=user.profile_picture,
                mandala_1_access=user.mandala_1_access,
                mandala_2_access=user.mandala_2_access,
                mandala_3_access=user.mandala_3_access,
                rudraksha_8_mukhi_access=user.rudraksha_8_mukhi_access,
                rudraksha_11_mukhi_access=user.rudraksha_11_mukhi_access,
                rudraksha_14_mukhi_access=user.rudraksha_14_mukhi_access,
                mandala_1_completed_at=user.mandala_1_completed_at,
                mandala_2_completed_at=user.mandala_2_completed_at,
                mandala_3_completed_at=user.mandala_3_completed_at,
                rudraksha_8_mukhi_completed_at=user.rudraksha_8_mukhi_completed_at,
                rudraksha_11_mukhi_completed_at=user.rudraksha_11_mukhi_completed_at,
                rudraksha_14_mukhi_completed_at=user.rudraksha_14_mukhi_completed_at,
                mandala_1_started_at=user.mandala_1_started_at,
                mandala_2_started_at=user.mandala_2_started_at,
                mandala_3_started_at=user.mandala_3_started_at,
                rudraksha_8_mukhi_started_at=user.rudraksha_8_mukhi_started_at,
                rudraksha_11_mukhi_started_at=user.rudraksha_11_mukhi_started_at,
                rudraksha_14_mukhi_started_at=user.rudraksha_14_mukhi_started_at
            )
            postgres_db.session.add(new_user)
        postgres_db.session.commit()
        print(f"   ✓ Migrated {len(users)} users")
        
        # Migrate Donation Purposes
        print("   → Migrating donation purposes...")
        for purpose in donation_purposes:
            new_purpose = DonationPurpose(
                id=purpose.id,
                name=purpose.name,
                description=purpose.description,
                is_active=purpose.is_active,
                created_at=purpose.created_at,
                created_by=purpose.created_by
            )
            postgres_db.session.add(new_purpose)
        postgres_db.session.commit()
        print(f"   ✓ Migrated {len(donation_purposes)} donation purposes")
        
        # Migrate Offline Donations
        print("   → Migrating offline donations...")
        for donation in offline_donations:
            new_donation = OfflineDonation(
                id=donation.id,
                donor_id=donation.donor_id,
                worksheet=donation.worksheet,
                donor_name=donation.donor_name,
                donor_email=donation.donor_email,
                donor_phone=donation.donor_phone,
                amount=donation.amount,
                currency=donation.currency,
                purpose_id=donation.purpose_id,
                donation_date=donation.donation_date,
                payment_method=donation.payment_method,
                reference_number=donation.reference_number,
                notes=donation.notes,
                is_verified=donation.is_verified,
                created_at=donation.created_at,
                created_by=donation.created_by,
                verified_at=donation.verified_at,
                verified_by=donation.verified_by
            )
            postgres_db.session.add(new_donation)
        postgres_db.session.commit()
        print(f"   ✓ Migrated {len(offline_donations)} offline donations")
        
        # Migrate Mandala Registrations
        print("   → Migrating mandala registrations...")
        for registration in mandala_registrations:
            new_registration = MandalaSadhanaRegistration(
                id=registration.id,
                email=registration.email,
                full_name=registration.full_name,
                mandala_48_commitment=registration.mandala_48_commitment,
                mandala_144_commitment=registration.mandala_144_commitment,
                commitment_text=registration.commitment_text,
                sadhana_start_date=registration.sadhana_start_date,
                sadhana_type=registration.sadhana_type,
                send_copy=registration.send_copy,
                created_at=registration.created_at,
                updated_at=registration.updated_at
            )
            postgres_db.session.add(new_registration)
        postgres_db.session.commit()
        print(f"   ✓ Migrated {len(mandala_registrations)} mandala registrations")
        
        print("\n✅ Migration completed successfully!")
        
        # Verify migration
        print("\n5️⃣ Verifying migration...")
        migrated_users = User.query.count()
        migrated_purposes = DonationPurpose.query.count()
        migrated_donations = OfflineDonation.query.count()
        migrated_registrations = MandalaSadhanaRegistration.query.count()
        
        print(f"   ✓ PostgreSQL now has:")
        print(f"     • {migrated_users} users")
        print(f"     • {migrated_purposes} donation purposes")
        print(f"     • {migrated_donations} offline donations")
        print(f"     • {migrated_registrations} mandala registrations")
        
        return True

if __name__ == "__main__":
    try:
        success = migrate_data()
        
        if success:
            print("\n" + "=" * 70)
            print("🎉 Migration complete! Your application is now using PostgreSQL.")
            print("\nNext steps:")
            print("1. Update app.py to use the PostgreSQL connection string (already done)")
            print("2. Restart your Flask application")
            print("3. Test login and user management features")
            print("4. Once confirmed working, you can archive the SQLite database")
            print("=" * 70)
        else:
            print("\n❌ Migration failed. Please check the error messages above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

