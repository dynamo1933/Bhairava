#!/usr/bin/env python3
"""
Network connectivity test script for Daiva Anughara.
This script helps diagnose network connectivity issues.
"""

import socket
import subprocess
import platform
import sys
import requests
from datetime import datetime

def test_port_availability(host, port):
    """Test if a port is open and accessible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception as e:
        print(f"Error testing port {port} on {host}: {e}")
        return False

def get_local_ip():
    """Get the local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def test_http_connection(url):
    """Test HTTP connection to a URL"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"HTTP test failed for {url}: {e}")
        return False

def run_network_tests():
    """Run comprehensive network tests"""
    print("🌐 Daiva Anughara - Network Connectivity Test")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 60)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"📍 Local IP: {local_ip}")
    
    # Test localhost connection
    print("\n🔍 Testing localhost connection...")
    localhost_ok = test_port_availability("127.0.0.1", 5000)
    print(f"   localhost:5000 - {'✅ OK' if localhost_ok else '❌ FAILED'}")
    
    # Test local IP connection
    print(f"\n🔍 Testing local IP connection...")
    local_ip_ok = test_port_availability(local_ip, 5000)
    print(f"   {local_ip}:5000 - {'✅ OK' if local_ip_ok else '❌ FAILED'}")
    
    # Test HTTP connections
    print(f"\n🌐 Testing HTTP connections...")
    localhost_http = test_http_connection("http://127.0.0.1:5000")
    local_ip_http = test_http_connection(f"http://{local_ip}:5000")
    
    print(f"   http://127.0.0.1:5000 - {'✅ OK' if localhost_http else '❌ FAILED'}")
    print(f"   http://{local_ip}:5000 - {'✅ OK' if local_ip_http else '❌ FAILED'}")
    
    # Test external connectivity
    print(f"\n🌍 Testing external connectivity...")
    try:
        external_test = requests.get("http://httpbin.org/ip", timeout=5)
        if external_test.status_code == 200:
            print("   External connectivity - ✅ OK")
        else:
            print("   External connectivity - ❌ FAILED")
    except Exception as e:
        print(f"   External connectivity - ❌ FAILED ({e})")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if localhost_ok and local_ip_ok:
        print("✅ Server is running and accessible")
        print(f"🌐 Network URL: http://{local_ip}:5000")
        print("\n📱 To access from other devices:")
        print(f"   1. Use: http://{local_ip}:5000")
        print(f"   2. Scan QR code on the home page")
        print(f"   3. Use mDNS: http://{socket.gethostname()}.local:5000")
        
        if not local_ip_http:
            print("\n⚠️  WARNING: HTTP test failed - check if Flask app is running")
    else:
        print("❌ Server is not accessible")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Make sure the Flask app is running (python app.py)")
        print("   2. Check Windows Firewall settings")
        print("   3. Ensure port 5000 is not blocked")
        print("   4. Try running as administrator")
    
    print("\n" + "=" * 60)

def check_firewall_windows():
    """Check Windows Firewall status"""
    if platform.system() != "Windows":
        return
    
    print("\n🛡️  Checking Windows Firewall...")
    try:
        result = subprocess.run([
            "netsh", "advfirewall", "show", "allprofiles", "state"
        ], capture_output=True, text=True, timeout=10)
        
        if "ON" in result.stdout:
            print("   ⚠️  Windows Firewall is ON")
            print("   💡 You may need to add Python or port 5000 to allowed programs")
        else:
            print("   ✅ Windows Firewall is OFF")
    except Exception as e:
        print(f"   ❓ Could not check firewall status: {e}")

if __name__ == "__main__":
    try:
        run_network_tests()
        check_firewall_windows()
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
