# Supabase PostgreSQL Connection Guide

## Issue
The hostname `db.cuyilngsmocyhadlbrgv.supabase.co` cannot be resolved.

## Solution: Get the Correct Connection String

### Step 1: Log into Supabase Dashboard
1. Go to https://app.supabase.com
2. Log into your account
3. Select your project

### Step 2: Get the Connection String
1. In your Supabase project, go to **Settings** → **Database**
2. Scroll down to **Connection string**
3. Select **URI** (not Pooler)
4. You'll see something like:
   ```
   postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-xx-xx-x.pooler.supabase.com:5432/postgres
   ```

### Step 3: Supabase Connection Options

Supabase provides **THREE** different connection modes:

#### Option 1: Transaction Pooler (Recommended for Server-side)
- **Format**: `aws-0-[region].pooler.supabase.com`
- **Port**: `5432` 
- **Use for**: Server-side connections with connection pooling

#### Option 2: Session Pooler
- **Format**: `aws-0-[region].pooler.supabase.com`
- **Port**: `6543`
- **Use for**: Web applications that need session-level pooling

#### Option 3: Direct Connection
- **Format**: `aws-0-[region].pooler.supabase.com`  
- **Port**: `5432`
- **Use for**: Direct connections without pooling

### Step 4: Fix the Connection String in App

Once you have the correct connection string:

1. **Update `app.py`**:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:[YOUR-PASSWORD]@aws-0-xx-xx-x.pooler.supabase.com:5432/postgres'
   ```

2. **URL-encode special characters** in the password:
   - `@` → `%40`
   - `#` → `%23`
   - `/` → `%2F`
   - etc.

### Step 5: Alternative - Use Connection Parameters

Instead of using a connection string, you can use individual parameters:

Update `app.py` to use connection parameters:

```python
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER', 'postgres'),
    os.getenv('DB_PASSWORD', '_Bottlemepani@35'),
    os.getenv('DB_HOST', 'aws-0-xx-xx-x.pooler.supabase.com'),
    os.getenv('DB_PORT', '5432'),
    os.getenv('DB_NAME', 'postgres')
)
```

## Common Issues

### Issue 1: "could not translate host name"
- **Cause**: Incorrect or mistyped hostname
- **Solution**: Copy the exact hostname from Supabase dashboard

### Issue 2: "Tenant or user not found"
- **Cause**: Wrong connection string or tenant ID mismatch
- **Solution**: Use the exact connection string from Supabase dashboard

### Issue 3: "password authentication failed"
- **Cause**: Incorrect password
- **Solution**: Reset password in Supabase settings

### Issue 4: Connection timeout
- **Cause**: Firewall or network restriction
- **Solution**: Check Supabase network restrictions or use Supabase's IP allowlist

## Testing Your Connection

After updating the connection string, test it:

```bash
python test_connection.py
```

Or test directly in Python:

```python
import psycopg2

conn = psycopg2.connect(
    host="YOUR-HOST",
    port=5432,
    database="postgres",
    user="postgres",
    password="YOUR-PASSWORD"
)
print("✅ Connected successfully!")
conn.close()
```

## Security Best Practices

1. **Never commit credentials to git**
2. Use environment variables
3. Enable SSL/TLS connections
4. Use Supabase's connection pooling for better performance
5. Rotate passwords regularly

## Quick Reference

**Your Supabase Connection Details** (to be confirmed):
- Host: [Check Supabase Dashboard]
- Port: 5432
- Database: postgres
- User: postgres
- Password: _Bottlemepani@35 (URL-encode special characters)

**Next Steps**:
1. Get the correct connection string from Supabase dashboard
2. Update it in `app.py`
3. URL-encode the password if it contains special characters
4. Test the connection

