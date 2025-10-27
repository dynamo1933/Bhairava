# PostgreSQL Migration Guide

## Overview
This document explains the changes made to migrate your Daiva Anughara application from SQLite to PostgreSQL for user management.

## Changes Made

### 1. Updated Dependencies
**File**: `requirements.txt`
- Added `psycopg2-binary==2.9.9` - PostgreSQL driver for Python

### 2. Updated Database Configuration
**File**: `app.py`
- Changed `SQLALCHEMY_DATABASE_URI` from SQLite to PostgreSQL
- Connection details:
  - Host: `db.cuyilngsmocyhadlbrgv.supabase.co`
  - Port: `5432`
  - Database: `postgres`
  - User: `postgres`
- Password contains special character `@` which is URL-encoded as `%40`

### 3. Updated Migration Script
**File**: `database_migration.py`
- Updated to use PostgreSQL connection string instead of SQLite

### 4. Created New Migration Script
**File**: `migrate_to_postgresql.py`
- Comprehensive script to migrate existing SQLite data to PostgreSQL
- Migrates all tables: Users, DonationPurpose, OfflineDonation, MandalaSadhanaRegistration
- Includes data verification after migration

## What You Need to Do

### Step 1: Install PostgreSQL Driver
Run this command in your terminal:
```bash
pip install psycopg2-binary==2.9.9
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Migrate Existing Data (If Applicable)
If you have existing data in your SQLite database that you want to migrate:

1. **Backup your current SQLite database** (recommended):
   ```bash
   cp instance/daiva_anughara.db instance/daiva_anughara.db.backup
   ```

2. **Run the migration script**:
   ```bash
   python migrate_to_postgresql.py
   ```

3. **Follow the prompts** - the script will:
   - Read all data from SQLite
   - Create tables in PostgreSQL
   - Migrate all data
   - Verify the migration

### Step 3: Verify Connection
Test that your application can connect to PostgreSQL:

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ PostgreSQL connection successful!')"
```

### Step 4: Start Your Application
```bash
python app.py
```

## Important Notes

### Database Access
- Your PostgreSQL database is hosted on Supabase
- The connection string includes credentials - **DO NOT commit this to version control**
- Consider using environment variables for production

### What's Migrated
The following data will be migrated if you run the migration script:
- ✅ Users (with all fields including passwords, permissions, progress)
- ✅ Donation Purposes
- ✅ Offline Donations
- ✅ Mandala Sadhana Registrations

### If You're Starting Fresh
If you don't need to migrate existing data, you can skip Step 2. The application will automatically create the necessary tables when you first start it.

### Environment Variables (Recommended for Production)
For better security, consider storing the connection string in an environment variable:

1. Create a `.env` file:
   ```
   DATABASE_URL=postgresql://postgres:_Bottlemepani%4035@db.cuyilngsmocyhadlbrgv.supabase.co:5432/postgres
   ```
   Note: The `@` in the password must be URL-encoded as `%40`

2. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

3. Update `app.py` to use environment variable:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
   ```

## Troubleshooting

### Connection Issues
- Verify your Supabase database is accessible from your IP
- Check that the credentials in the connection string are correct
- Ensure you have internet connectivity

### Migration Errors
- Check that both SQLite and PostgreSQL databases are accessible
- Verify you have write permissions on PostgreSQL
- Check that all required packages are installed

### Testing
After migration, test these features:
- User login/registration
- Admin user management
- Donation management
- Mandala Sadhana registration

## Support
If you encounter any issues during migration, check:
1. Supabase dashboard for database status
2. Application logs for error messages
3. Network connectivity to Supabase

---

## Security Reminder
⚠️ **IMPORTANT**: The database connection string contains sensitive credentials. Make sure to:
1. Never commit credentials to version control
2. Use environment variables for production
3. Rotate credentials regularly
4. Use Supabase's connection pooling for better performance

