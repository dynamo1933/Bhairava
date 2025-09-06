#!/usr/bin/env python3
"""
Recreate Database Script
Recreates the database with the updated schema including profile_picture column
"""

from flask import Flask
from models import db, User
import os

def create_app():
    """Create Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daiva_anughara.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def recreate_database():
    """Recreate database with updated schema"""
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables
            print("🔄 Dropping existing tables...")
            db.drop_all()
            
            # Create all tables with new schema
            print("🔄 Creating tables with updated schema...")
            db.create_all()
            
            # Create admin user
            print("🔄 Creating admin user...")
            admin = User(
                username='admin',
                email='admin@daivaanughara.com',
                full_name='Administrator',
                role='admin',
                is_approved=True,
                is_active=True,
                purpose='Administrator account for system management and user approval.',
                mandala_1_access=True,
                mandala_2_access=True,
                mandala_3_access=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Database recreated successfully with profile_picture column!")
            print("✅ Admin user created:")
            print("   Username: admin")
            print("   Password: admin123")
            return True
            
        except Exception as e:
            print(f"❌ Error during database recreation: {e}")
            return False

if __name__ == '__main__':
    print("🚀 Starting database recreation...")
    success = recreate_database()
    
    if success:
        print("🎉 Database recreation completed successfully!")
    else:
        print("⚠️  Database recreation failed. Please check the errors above.")
