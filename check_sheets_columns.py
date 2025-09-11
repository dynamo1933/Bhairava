#!/usr/bin/env python3
"""
Check what columns are available in Google Sheets
"""

import os
import sys

# Add the current directory to Python path
sys.path.append('.')

from google_sheets import sheets_manager

def check_sheets_columns():
    """Check what columns are available in Google Sheets"""
    print("🔍 Checking Google Sheets Columns")
    print("=" * 40)
    
    if not sheets_manager.is_connected():
        print("❌ Google Sheets not connected")
        return
    
    try:
        # Get all worksheets
        worksheets = sheets_manager.spreadsheet.worksheets()
        print(f"📊 Total worksheets: {len(worksheets)}")
        
        for worksheet in worksheets:
            if worksheet.title == 'Sheet1':  # Skip default sheet
                continue
                
            print(f"\n📋 Worksheet: {worksheet.title}")
            
            # Get first few rows to see column structure
            records = worksheet.get_all_records()
            if records:
                print(f"   Total rows: {len(records)}")
                print(f"   Columns: {list(records[0].keys())}")
                
                # Show first record
                print(f"   Sample record:")
                for key, value in records[0].items():
                    print(f"      {key}: '{value}'")
            else:
                print("   No records found")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_sheets_columns()
