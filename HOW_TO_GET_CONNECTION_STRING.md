# How to Get the Correct Supabase Connection String

## Steps to Get Working Connection String:

### 1. In Your Supabase Dashboard:
   - Go to: Settings → Database
   - Tab: "Connection String"

### 2. Change the Method Dropdown:
   - Currently showing: **"Method: Direct connection"**
   - Click the dropdown and change to: **"Method: Session Pooler"** or **"Transaction Pooler"**
   
### 3. Copy the New Connection String:
   After changing the method, you'll see a different hostname like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@aws-0-xxxxx.pooler.supabase.com:6543/postgres
   ```
   
   **OR**
   
   ```
   postgresql://postgres:[YOUR-PASSWORD]@aws-0-xxxxx.pooler.supabase.com:5432/postgres
   ```

### 4. Important Differences:
   - **Direct connection**: `db.cuyilngsmocyhadlbrgv.supabase.co` ❌ (Won't work from IPv4)
   - **Session Pooler**: `aws-0-xxxxx.pooler.supabase.com` ✅ (Works from IPv4)

### 5. After You Get It:
   1. Copy the full connection string
   2. Replace `[YOUR-PASSWORD]` with your actual password: `_Bottlemepani@35`
   3. URL-encode the password: `@` → `%40`
   4. Share it with me so I can update your app

## Why Direct Connection Doesn't Work:
- Your IP is on IPv4 network (Windows)
- Supabase direct connection requires IPv6 or an add-on
- The **Session Pooler** works with IPv4 without any add-ons

## What You Should See After Switching:
The connection string should look like:
```
postgresql://postgres:_Bottlemepani%4035@aws-0-[some-number].pooler.supabase.com:[port]/postgres
```

Where `aws-0-[some-number].pooler.supabase.com` is your pooler hostname.

