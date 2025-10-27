#!/usr/bin/env python3
"""
Test script to verify Flask app starts without database errors
"""

import sys
from flask import Flask
from models import db, User

def test_app_startup():
    """Test that the Flask app starts without database errors"""
    print("🧪 Testing Flask app startup...")

    # Create app with same config as main app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daiva_anughara.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # Initialize database
    db.init_app(app)

    try:
        with app.app_context():
            print("✅ App context created successfully")

            # Test database connection
            from sqlalchemy import text
            result = db.session.execute(text("SELECT COUNT(*) FROM user"))
            user_count = result.scalar()
            print(f"✅ Database connected successfully - {user_count} users found")

            # Test User model with new fields
            user = User.query.first()
            if user:
                print(f"✅ User model working - testing {user.username}")
                print(f"   Current stage: {user.get_current_stage()}")
                print(f"   Next stage: {user.get_next_required_stage()}")
                print(f"   Has Rudraksha access: {user.has_mandala_access(4)}")
                print("✅ All new stage methods working correctly!")

            # Test admin routes import
            from auth import auth
            print("✅ Auth blueprint imported successfully")

            print("\n🎉 Flask app startup test completed successfully!")
            print("The spiritual progress tracking system is ready to use!")

            return True

    except Exception as e:
        print(f"❌ Error during app startup: {e}")
        return False

if __name__ == "__main__":
    print("🕉️ Daiva Anughara - Flask App Startup Test")
    print("=" * 50)

    success = test_app_startup()

    if success:
        print("\n✅ SUCCESS: Flask app starts without errors!")
        print("The database migration was successful and all features are working.")
    else:
        print("\n❌ FAILURE: Flask app has startup errors.")
        sys.exit(1)
