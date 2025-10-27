#!/usr/bin/env python3
"""
Database Migration Script for Spiritual Progress Tracking
Run this script to add the new stage tracking fields to the existing User table.

Usage:
1. Make sure your Flask app is properly configured
2. Run: python database_migration.py
3. The script will add the new columns to the User table

New Fields Added:
- Rudraksha access permissions (5 Mukhi, 11 Mukhi, 14 Mukhi)
- Stage completion dates for all 6 stages
- Stage start dates for duration tracking
"""

import sys
from flask import Flask
from models import db, User
from datetime import datetime
from sqlalchemy import text

def create_app():
    """Create Flask app for migration"""
    app = Flask(__name__)

    # Configuration from app.py
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daiva_anughara.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    db.init_app(app)
    return app

def add_stage_tracking_columns():
    """Add new stage tracking columns to User table"""
    print("🕉️ Starting database migration for spiritual progress tracking...")

    try:
        # Add Rudraksha access permissions
        print("📿 Adding Rudraksha access permission fields...")
        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE user ADD COLUMN rudraksha_5_mukhi_access BOOLEAN DEFAULT 0"))
                conn.commit()
            print("   ✓ rudraksha_5_mukhi_access added")
        except Exception as e:
            print(f"   ⚠️ rudraksha_5_mukhi_access: {e}")

        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE user ADD COLUMN rudraksha_11_mukhi_access BOOLEAN DEFAULT 0"))
                conn.commit()
            print("   ✓ rudraksha_11_mukhi_access added")
        except Exception as e:
            print(f"   ⚠️ rudraksha_11_mukhi_access: {e}")

        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE user ADD COLUMN rudraksha_14_mukhi_access BOOLEAN DEFAULT 0"))
                conn.commit()
            print("   ✓ rudraksha_14_mukhi_access added")
        except Exception as e:
            print(f"   ⚠️ rudraksha_14_mukhi_access: {e}")

        # Add stage completion dates
        print("📅 Adding stage completion date fields...")
        completion_fields = [
            'mandala_1_completed_at',
            'mandala_2_completed_at',
            'mandala_3_completed_at',
            'rudraksha_5_mukhi_completed_at',
            'rudraksha_11_mukhi_completed_at',
            'rudraksha_14_mukhi_completed_at'
        ]

        for field in completion_fields:
            try:
                with db.engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE user ADD COLUMN {field} DATETIME"))
                    conn.commit()
                print(f"   ✓ {field} added")
            except Exception as e:
                print(f"   ⚠️ {field}: {e}")

        # Add stage start dates
        print("⏱️ Adding stage start date fields...")
        start_fields = [
            'mandala_1_started_at',
            'mandala_2_started_at',
            'mandala_3_started_at',
            'rudraksha_5_mukhi_started_at',
            'rudraksha_11_mukhi_started_at',
            'rudraksha_14_mukhi_started_at'
        ]

        for field in start_fields:
            try:
                with db.engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE user ADD COLUMN {field} DATETIME"))
                    conn.commit()
                print(f"   ✓ {field} added")
            except Exception as e:
                print(f"   ⚠️ {field}: {e}")

        print("✅ Migration completed!")
        print("\n📊 Migration Results:")
        print("   The script attempted to add new spiritual progress tracking fields.")
        print("   Warnings for existing fields are normal - they indicate the columns already exist.")
        print("\n📋 Expected new fields:")
        print("   - Rudraksha access permissions (5, 11, 14 Mukhi)")
        print("   - Stage completion dates for all 6 stages")
        print("   - Stage start dates for duration tracking")

    except Exception as e:
        print(f"❌ Error during migration: {e}")
        print("This might mean the columns already exist or there's a database issue.")
        return False

    return True

def reset_database_for_testing():
    """Optional: Reset database for testing (WARNING: This will delete all data!)"""
    print("⚠️ WARNING: This will delete all existing data!")
    response = input("Are you sure you want to reset the database? (type 'YES' to confirm): ")

    if response == 'YES':
        print("🗑️ Dropping all tables...")
        db.drop_all()
        print("🆕 Creating all tables...")
        db.create_all()
        print("✅ Database reset complete!")
        return True
    else:
        print("❌ Database reset cancelled.")
        return False

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        print("🕉️ Daiva Anughara - Spiritual Progress Database Migration")
        print("=" * 60)

        if len(sys.argv) > 1 and sys.argv[1] == '--reset':
            reset_database_for_testing()
        else:
            success = add_stage_tracking_columns()

            if success:
                print("\n🎉 Migration completed! The spiritual progress tracking system is ready.")
                print("\nNext steps:")
                print("1. Restart your Flask application")
                print("2. Test the new admin stage management features")
                print("3. Test the user progress bar on the padati page")
                print("4. Update existing users' stage access as needed")
            else:
                print("\n⚠️ Migration failed. Please check the error messages above.")
