# Google Sheets Integration Setup Guide

This guide will help you set up Google Sheets integration for transparent donation tracking.

## Prerequisites

1. A Google account
2. Access to the Google Sheets spreadsheet: https://docs.google.com/spreadsheets/d/1AwipeokLOKRFZFLaz8lz9c5J-68Wskeo79YfimEncH4/edit?usp=sharing

## Step 1: Create Google Service Account

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click on it and press "Enable"
4. Create a service account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the service account details
   - Click "Create and Continue"
   - Skip the optional steps and click "Done"

## Step 2: Generate Service Account Key

1. In the "Credentials" section, find your service account
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose "JSON" format
6. Download the JSON file
7. Rename it to `google_credentials.json`
8. Place it in the root directory of your project

## Step 3: Share Google Sheet with Service Account

1. Open the Google Sheet: https://docs.google.com/spreadsheets/d/1AwipeokLOKRFZFLaz8lz9c5J-68Wskeo79YfimEncH4/edit?usp=sharing
2. Click "Share" button (top right)
3. Add the service account email (found in the JSON file as `client_email`)
4. Give it "Editor" permissions
5. Click "Send"

## Step 4: Configure the Application

1. The spreadsheet ID is already configured in `google_sheets.py`
2. Make sure `google_credentials.json` is in the project root
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 5: Test the Integration

1. Run the migration script:
   ```bash
   python migrate_donations.py
   ```

2. Start the application:
   ```bash
   python app.py
   ```

3. Login as admin and go to "Admin" > "Donation Management"
4. Add a test donation to verify Google Sheets integration

## How It Works

### Data Flow
- **Primary Source**: Google Sheets (your shared Excel link)
- **Secondary Source**: Local database (for offline functionality)
- **Sync Direction**: Google Sheets → Website (read-only for transparency)

### Automatic Sheet Reading
- The website fetches donations directly from your Google Sheets
- Each worksheet represents a donation purpose/category
- Headers expected: ID, Donor Name, Donor Email, Donor Phone, Amount, Currency, Purpose, Donation Date, Payment Method, Reference Number, Notes, Status, Created At, Created By

### Data Synchronization
- **Public Page**: Shows donations directly from Google Sheets
- **Admin Sync**: Can sync Google Sheets data to local database for backup
- **Real-time Updates**: Changes in Google Sheets are reflected on the website
- **Fallback**: If Google Sheets is unavailable, falls back to local database

### Transparency Features
- Public donations page shows recent verified donations from Google Sheets
- Summary statistics calculated from Google Sheets data
- All donation purposes are automatically detected from worksheets
- Admin can sync data for offline access and backup

## Troubleshooting

### Common Issues

1. **"Credentials file not found"**
   - Make sure `google_credentials.json` is in the project root
   - Check the file name is exactly `google_credentials.json`

2. **"Permission denied"**
   - Make sure the service account email has "Editor" access to the Google Sheet
   - Check that the spreadsheet ID is correct

3. **"Worksheet not found"**
   - The application will create worksheets automatically
   - Check that the service account has permission to create worksheets

4. **"API not enabled"**
   - Make sure Google Sheets API is enabled in Google Cloud Console
   - Check that the service account has the necessary permissions

### Testing Connection

You can test the Google Sheets connection by running:

```python
from google_sheets import sheets_manager
sheets_manager.test_connection()
```

## Security Notes

- Keep `google_credentials.json` secure and never commit it to version control
- Add `google_credentials.json` to your `.gitignore` file
- The service account should only have access to the specific Google Sheet
- Regularly rotate service account keys for security

## File Structure

```
project_root/
├── google_credentials.json  # Service account credentials (DO NOT COMMIT)
├── google_sheets.py         # Google Sheets integration module
├── migrate_donations.py     # Database migration script
├── app.py                   # Main application
├── models.py                # Database models
├── forms.py                 # Form definitions
└── templates/
    ├── donations.html       # Public donations page
    └── admin/
        ├── donations.html   # Admin donation management
        ├── add_donation.html
        ├── donation_purposes.html
        └── add_donation_purpose.html
```

## Support

If you encounter any issues:

1. Check the application logs for error messages
2. Verify all setup steps were completed correctly
3. Test the Google Sheets connection manually
4. Ensure all dependencies are installed correctly
