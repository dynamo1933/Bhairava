#!/usr/bin/env python3
"""
Database Migration Script
Adds the profile_picture column to the user table
"""

from flask import Flask
from models import db, User
import os

def create_app():
    """Create Flask app for migration"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daiva_anughara.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def migrate_database():
    """Add profile_picture column to user table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if the column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [column['name'] for column in inspector.get_columns('user')]
            
            if 'profile_picture' in columns:
                print("✅ profile_picture column already exists in user table")
                return
            
            # Add the new column
            print("🔄 Adding profile_picture column to user table...")
            db.engine.execute('ALTER TABLE user ADD COLUMN profile_picture VARCHAR(255)')
            print("✅ Successfully added profile_picture column to user table")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            # Try alternative approach
            try:
                print("🔄 Trying alternative migration approach...")
                db.engine.execute('ALTER TABLE user ADD COLUMN profile_picture TEXT')
                print("✅ Successfully added profile_picture column using alternative approach")
            except Exception as e2:
                print(f"❌ Alternative approach also failed: {e2}")
                print("💡 You may need to recreate the database or manually add the column")
                return False
        
        return True

if __name__ == '__main__':
    print("🚀 Starting database migration...")
    success = migrate_database()
    
    if success:
        print("🎉 Database migration completed successfully!")
    else:
        print("⚠️  Database migration failed. Please check the errors above.")
