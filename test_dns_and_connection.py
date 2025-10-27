#!/usr/bin/env python3
"""
Comprehensive DNS and connection test for Supabase PostgreSQL
"""

import socket
import sys

def test_dns_hostname(hostname):
    """Test if hostname can be resolved"""
    print(f"\n{'='*70}")
    print(f"DNS Resolution Test: {hostname}")
    print(f"{'='*70}")
    
    try:
        # Try to resolve the hostname
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution SUCCESS")
        print(f"   Hostname: {hostname}")
        print(f"   IP Address: {ip_address}")
        return ip_address
    except socket.gaierror as e:
        print(f"❌ DNS Resolution FAILED")
        print(f"   Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_tcp_connection(hostname, port):
    """Test TCP connection to hostname:port"""
    print(f"\n{'='*70}")
    print(f"TCP Connection Test: {hostname}:{port}")
    print(f"{'='*70}")
    
    try:
        # Try to establish a TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is OPEN")
            return True
        else:
            print(f"❌ Port {port} is CLOSED or UNREACHABLE")
            return False
    except socket.gaierror:
        print(f"❌ Cannot resolve hostname")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def try_alternative_hostnames():
    """Try common Supabase hostname patterns"""
    hostname = "db.cuyilngsmocyhadlbrgv.supabase.co"
    
    # Try different variations
    alternatives = [
        hostname,
        hostname.replace("db.", ""),
        f"pooler.{hostname.replace('db.', '')}",
        f"direct.{hostname.replace('db.', '')}",
        "aws-0-ap-southeast-1.pooler.supabase.com",
        f"aws-0-ap-southeast-1.pooler.supabase.com:{hostname.split('.')[0]}"
    ]
    
    print(f"\n{'='*70}")
    print("Trying Alternative Hostname Formats")
    print(f"{'='*70}")
    
    for alt_hostname in alternatives:
        print(f"\nTrying: {alt_hostname}")
        result = test_dns_hostname(alt_hostname)
        if result:
            test_tcp_connection(alt_hostname, 5432)
            return alt_hostname
    
    return None

if __name__ == "__main__":
    print("🕉️ Supabase DNS and Connection Diagnostic Tool")
    print("=" * 70)
    
    hostname = "db.cuyilngsmocyhadlbrgv.supabase.co"
    
    # Test 1: DNS Resolution
    ip_address = test_dns_hostname(hostname)
    
    # Test 2: TCP Connection (if DNS works)
    if ip_address:
        test_tcp_connection(hostname, 5432)
    else:
        print(f"\n⚠️ DNS resolution failed. Trying alternative hostname formats...")
        working_hostname = try_alternative_hostnames()
        
        if not working_hostname:
            print("\n" + "="*70)
            print("❌ DIAGNOSIS")
            print("="*70)
            print("The hostname cannot be resolved by DNS.")
            print("\nPossible reasons:")
            print("1. The Supabase project might not be active/paused")
            print("2. DNS propagation delay (wait a few minutes)")
            print("3. Network connectivity issues")
            print("4. The hostname might be incorrect")
            print("5. The Supabase project might not exist")
            print("\n💡 RECOMMENDATIONS:")
            print("1. Check Supabase dashboard: https://app.supabase.com")
            print("2. Verify project status (not paused)")
            print("3. Get the connection string from Settings → Database")
            print("4. Try using the connection pooler URL instead")
            print("5. Check your internet connection")
            print("="*70)

