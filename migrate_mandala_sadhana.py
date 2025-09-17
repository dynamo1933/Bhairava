#!/usr/bin/env python3
"""
Migration script to add Mandala Sadhana Registration table
"""

from app import app, db
from models import MandalaSadhanaRegistration

def migrate_mandala_sadhana():
    """Add Mandala Sadhana Registration table"""
    with app.app_context():
        try:
            # Create the table
            db.create_all()
            print("✅ Mandala Sadhana Registration table created successfully!")
            
            # Verify the table exists
            result = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mandala_sadhana_registration'")
            if result.fetchone():
                print("✅ Table 'mandala_sadhana_registration' verified in database")
            else:
                print("❌ Table 'mandala_sadhana_registration' not found in database")
                
        except Exception as e:
            print(f"❌ Error creating Mandala Sadhana Registration table: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🔄 Starting Mandala Sadhana Registration migration...")
    success = migrate_mandala_sadhana()
    
    if success:
        print("🎉 Migration completed successfully!")
    else:
        print("💥 Migration failed!")





