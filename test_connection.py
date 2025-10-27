#!/usr/bin/env python3
"""
Test PostgreSQL connection with different connection string formats
"""

import psycopg2
from urllib.parse import quote_plus

# Test connection strings
test_configs = [
    {
        'name': 'Direct connection',
        'config': {
            'host': 'db.cuyilngsmocyhadlbrgv.supabase.co',
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': '_Bottlemepani@35'
        }
    },
    {
        'name': 'Alternative host format (pooler)',
        'config': {
            'host': 'aws-0-ap-southeast-1.pooler.supabase.com',  # Common Supabase pooler format
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': '_Bottlemepani@35'
        }
    }
]

def test_connection(name, config):
    """Test a connection configuration"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    
    try:
        conn = psycopg2.connect(**config)
        print("✅ CONNECTION SUCCESSFUL!")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL Version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ CONNECTION FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🕉️ PostgreSQL Connection Tester")
    print("Testing various connection configurations...\n")
    
    for config in test_configs:
        if test_connection(config['name'], config['config']):
            print("\n✅ Found working configuration!")
            break
    
    print("\n" + "="*60)
    print("💡 If all connections failed, please verify:")
    print("   1. Check your Supabase dashboard for the correct connection string")
    print("   2. Verify the database is running and accessible")
    print("   3. Check if your IP is whitelisted in Supabase")
    print("   4. Verify the password is correct")
    print("="*60)

