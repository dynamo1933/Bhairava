#!/usr/bin/env python3
"""
Purge script to delete all donation records from the database
Use with caution - this will permanently delete all donation data
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append('.')

from models import db, OfflineDonation, DonationPurpose
from app import app

def confirm_purge():
    """Ask for confirmation before purging"""
    print("⚠️  WARNING: This will permanently delete ALL donation records!")
    print("=" * 60)
    print("This action cannot be undone.")
    print()
    
    # Show current record count
    with app.app_context():
        donation_count = OfflineDonation.query.count()
        purpose_count = DonationPurpose.query.count()
        
        print(f"📊 Current records in database:")
        print(f"   - Donations: {donation_count}")
        print(f"   - Purposes: {purpose_count}")
        print()
    
    # Get confirmation
    while True:
        response = input("Are you sure you want to delete ALL donation records? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def purge_donations():
    """Delete all donation records from the database"""
    try:
        with app.app_context():
            # Get counts before deletion
            donation_count = OfflineDonation.query.count()
            purpose_count = DonationPurpose.query.count()
            
            print(f"🗑️  Starting purge process...")
            print(f"📊 Records to be deleted:")
            print(f"   - Donations: {donation_count}")
            print(f"   - Purposes: {purpose_count}")
            print()
            
            # Delete all donations first (due to foreign key constraints)
            print("🔄 Deleting donation records...")
            OfflineDonation.query.delete()
            
            # Delete all purposes
            print("🔄 Deleting purpose records...")
            DonationPurpose.query.delete()
            
            # Commit changes
            db.session.commit()
            
            print("✅ Purge completed successfully!")
            print(f"📊 Deleted {donation_count} donation records")
            print(f"📊 Deleted {purpose_count} purpose records")
            
            return True
            
    except Exception as e:
        print(f"❌ Error during purge: {e}")
        db.session.rollback()
        return False

def create_backup():
    """Create a backup before purging"""
    try:
        import shutil
        from datetime import datetime
        
        # Create backup directory
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/daiva_anughara_backup_{timestamp}.db"
        
        # Copy database file
        source_db = "instance/daiva_anughara.db"
        if os.path.exists(source_db):
            shutil.copy2(source_db, backup_file)
            print(f"💾 Backup created: {backup_file}")
            return backup_file
        else:
            print("⚠️  Database file not found, skipping backup")
            return None
            
    except Exception as e:
        print(f"⚠️  Could not create backup: {e}")
        return None

def restore_backup(backup_file):
    """Restore from backup file"""
    try:
        import shutil
        
        if backup_file and os.path.exists(backup_file):
            source_db = "instance/daiva_anughara.db"
            shutil.copy2(backup_file, source_db)
            print(f"🔄 Restored from backup: {backup_file}")
            return True
        else:
            print("❌ Backup file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error restoring backup: {e}")
        return False

def main():
    """Main purge function"""
    print("🧹 Daiva Anughara - Donation Purge Script")
    print("=" * 50)
    print("This script will permanently delete ALL donation records")
    print()
    
    # Check if database exists
    if not os.path.exists("instance/daiva_anughara.db"):
        print("❌ Database file not found. Nothing to purge.")
        return
    
    # Create backup
    print("💾 Creating backup before purge...")
    backup_file = create_backup()
    
    # Confirm purge
    if not confirm_purge():
        print("❌ Purge cancelled by user")
        return
    
    # Perform purge
    if purge_donations():
        print()
        print("🎉 Purge completed successfully!")
        print("📝 Next steps:")
        print("1. Restart your application")
        print("2. Run sync from admin panel to repopulate data")
        if backup_file:
            print(f"3. Backup available at: {backup_file}")
    else:
        print("❌ Purge failed!")
        if backup_file:
            print("💾 Backup is available if you need to restore")

def restore_mode():
    """Restore from backup mode"""
    print("🔄 Daiva Anughara - Restore from Backup")
    print("=" * 40)
    
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        print("❌ No backup directory found")
        return
    
    # List available backups
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    if not backups:
        print("❌ No backup files found")
        return
    
    print("📁 Available backups:")
    for i, backup in enumerate(backups, 1):
        backup_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(backup_path)
        print(f"   {i}. {backup} ({size} bytes)")
    
    # Select backup
    try:
        choice = int(input("\nSelect backup to restore (number): ")) - 1
        if 0 <= choice < len(backups):
            backup_file = os.path.join(backup_dir, backups[choice])
            if restore_backup(backup_file):
                print("✅ Restore completed successfully!")
            else:
                print("❌ Restore failed!")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_mode()
    else:
        main()
