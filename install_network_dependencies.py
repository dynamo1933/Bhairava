#!/usr/bin/env python3
"""
Installation script for Daiva Anughara network discovery dependencies.
This script installs the required packages for network discovery functionality.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install requirements from requirements.txt"""
    try:
        print("🔧 Installing network discovery dependencies...")
        print("=" * 50)
        
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("❌ requirements.txt not found!")
            return False
        
        # Install requirements
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
            print("\n📦 Installed packages:")
            print("   - qrcode[pil] - For generating QR codes")
            print("   - zeroconf - For mDNS/Bonjour service discovery")
            return True
        else:
            print("❌ Failed to install dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_installation():
    """Check if all required packages are installed"""
    try:
        import qrcode
        import zeroconf
        print("✅ All network discovery packages are available!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False

def main():
    """Main installation function"""
    print("🌐 Daiva Anughara - Network Discovery Setup")
    print("=" * 50)
    
    # Check current installation
    if check_installation():
        print("✅ Network discovery is already set up!")
        return
    
    # Install requirements
    if install_requirements():
        print("\n🎉 Network discovery setup complete!")
        print("\n📋 Next steps:")
        print("   1. Run: python app.py")
        print("   2. The server will show network access information")
        print("   3. Devices on the same WiFi can access via:")
        print("      - Direct IP address")
        print("      - QR code scan")
        print("      - mDNS discovery (hostname.local)")
        print("\n🔍 The application will be discoverable as 'Daiva Anughara' on the network")
    else:
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
