# Supabase PostgreSQL Setup Instructions

## Issue Identified

The hostname `db.cuyilngsmocyhadlbrgv.supabase.co` is **incorrect**.

✅ **Correct hostname**: `cuyilngsmocyhadlbrgv.supabase.co` (without the `db.` prefix)
❌ **Issue**: Cannot connect directly to this hostname - Supabase requires using the **Connection Pooler**

## Solution: Get the Correct Connection String

### Step 1: Log into Supabase Dashboard
1. Go to: https://app.supabase.com
2. Select your project
3. Navigate to: **Settings** → **Database**

### Step 2: Copy the Connection String

In the **Connection string** section, you'll see different connection modes:

#### Transaction Mode (Recommended for Flask)
Look for **"URI"** under "Transaction Pooler" or "Session Pooler"

Example format:
```
postgresql://postgres:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:5432/postgres
```

#### Or use the Connection Info
Look for fields like:
- **Host**: `aws-0-xxxxx.pooler.supabase.com` or similar
- **Database name**: `postgres`
- **Port**: `5432` (for transaction pooler) or `6543` (for session pooler)
- **User**: `postgres.xxxxx` (note the project reference!)
- **Password**: Your database password

### Step 3: Important Notes

1. **Use the Pooler URL, not direct connection**
   - Direct connection to `cuyilngsmocyhadlbrgv.supabase.co` will timeout
   - You MUST use the pooler URL (usually `aws-0-xxxxx.pooler.supabase.com`)

2. **User format**
   - Direct connection: `postgres`
   - Pooler connection: `postgres.xxxxx` (where xxxxx is your project reference)

3. **Database reference**
   - You need to specify which database: `postgres` or another database name

## What to Share

Please provide the following from your Supabase Dashboard:

1. The complete **Connection string (URI)** from Settings → Database
2. Or provide these individual fields:
   - Host
   - Port
   - Database name
   - User (with project reference if applicable)
   - Password

## Temporary Solution

If you just want to test locally, we can switch back to SQLite temporarily:

1. Update `app.py` to use SQLite again
2. Run your application
3. Later, when you have the correct Supabase connection string, migrate to PostgreSQL

## Common Supabase Connection String Formats

### Format 1: Transaction Pooler (Recommended)
```
postgresql://postgres.xxxxx:[password]@aws-0-xxxxx.pooler.supabase.com:5432/postgres
```

### Format 2: Session Pooler
```
postgresql://postgres.xxxxx:[password]@aws-0-xxxxx.pooler.supabase.com:6543/postgres
```

### Format 3: Direct Connection (Usually blocked by Supabase)
```
postgresql://postgres:[password]@db.xxxxx.supabase.co:5432/postgres
```

## Next Steps

1. ✅ Get the connection string from Supabase dashboard
2. ✅ Share it with me or update `app.py` yourself
3. ✅ I'll help you configure the application to use it

## Quick Commands

Once you have the correct connection string, update `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'YOUR_CONNECTION_STRING_HERE'
```

Remember to URL-encode special characters in the password:
- `@` → `%40`
- `#` → `%23`
- `/` → `%2F`
- etc.

