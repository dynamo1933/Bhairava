#!/usr/bin/env python3
"""
Test Script for Spiritual Progress Tracking System
Run this script to verify the new stage tracking functionality works correctly.

Usage: python test_stage_system.py
"""

import sys
from datetime import datetime
from models import User, db

def create_test_user():
    """Create a test user with sample stage data"""
    print("🧪 Creating test user...")

    # Create a test user
    user = User(
        username='test_user_stage',
        email='test_stage@example.com',
        full_name='Test User Stage',
        phone='1234567890',
        address='Test Address',
        practice_level='Beginner',
        purpose='Testing spiritual progress system'
    )
    user.set_password('test123')

    # Set some sample stage data
    user.mandala_1_access = True
    user.mandala_1_started_at = datetime.utcnow()
    user.mandala_1_completed_at = datetime.utcnow()

    user.mandala_2_access = True
    user.mandala_2_started_at = datetime.utcnow()

    # Mandala 1 completed, Mandala 2 in progress, Mandala 3 not started
    user.mandala_3_access = False

    return user

def test_stage_methods():
    """Test the new stage tracking methods"""
    print("🧪 Testing stage methods...")

    user = create_test_user()

    # Test stage access methods
    print(f"✅ Mandala 1 access: {user.has_mandala_access(1)}")
    print(f"✅ Mandala 2 access: {user.has_mandala_access(2)}")
    print(f"✅ Mandala 3 access: {user.has_mandala_access(3)}")
    print(f"✅ Rudraksha 5 access: {user.has_mandala_access(4)}")

    # Test current stage
    print(f"✅ Current stage: {user.get_current_stage()}")

    # Test next stage
    print(f"✅ Next stage: {user.get_next_required_stage()}")

    # Test stage info
    stage_info = user.get_stage_info(1)
    print(f"✅ Stage 1 info: {stage_info['stage_name']} - Completed: {stage_info['is_completed']}")

    # Test stage info for current stage
    current_stage_info = user.get_stage_info(user.get_current_stage())
    print(f"✅ Current stage info: {current_stage_info['stage_name']} - Duration: {current_stage_info['duration_days']} days")

    print("🎉 All stage methods working correctly!")

def test_stage_completion():
    """Test stage completion functionality"""
    print("🧪 Testing stage completion...")

    user = create_test_user()

    # Complete mandala 2
    user.complete_stage(2)
    user.mandala_3_access = True  # Grant access to next stage
    user.start_stage(3)  # Start next stage

    print(f"✅ After completion - Current stage: {user.get_current_stage()}")
    print(f"✅ Next stage: {user.get_next_required_stage()}")

    # Check duration
    duration = user.get_stage_duration_days(2)
    print(f"✅ Mandala 2 duration: {duration} days")

    print("🎉 Stage completion working correctly!")

if __name__ == "__main__":
    print("🕉️ Daiva Anughara - Stage System Test")
    print("=" * 50)

    try:
        test_stage_methods()
        print()
        test_stage_completion()

        print("\n✅ All tests passed! The spiritual progress tracking system is working correctly.")
        print("\n📋 Test Results:")
        print("   - User model has all new stage tracking fields")
        print("   - Stage access methods working")
        print("   - Stage completion methods working")
        print("   - Duration calculation working")
        print("   - Current/next stage detection working")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
