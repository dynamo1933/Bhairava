from flask import Flask, render_template, request, jsonify, send_from_directory, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRFError
from models import db, User, DonationPurpose, OfflineDonation, MandalaSadhanaRegistration
from auth import auth
from forms import DonationPurposeForm, OfflineDonationForm, DonationSearchForm, MandalaSadhanaRegistrationForm, MandalaSadhanaSearchForm
from google_sheets import get_sheets_manager
import os
import socket
import qrcode
import io
import base64
import threading
import time
from datetime import datetime, timedelta
from zeroconf import ServiceInfo, Zeroconf

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daiva_anughara.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Network configuration
NETWORK_PORT = 5000

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote server to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"⚠️  Warning: Could not determine local IP: {e}")
        # Fallback to localhost
        return "127.0.0.1"

def get_all_network_interfaces():
    """Get all available network interfaces and their IP addresses"""
    try:
        import netifaces  # type: ignore[import-untyped]
        interfaces = {}
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    if not ip.startswith('127.') and not ip.startswith('169.254.'):
                        interfaces[interface] = ip
        return interfaces
    except ImportError:
        print("⚠️  netifaces not available, using basic method")
        return {}
    except Exception as e:
        print(f"⚠️  Error getting network interfaces: {e}")
        return {}

def get_network_info():
    """Get comprehensive network information"""
    local_ip = get_local_ip()
    return {
        'local_ip': local_ip,
        'port': NETWORK_PORT,
        'url': f"http://{local_ip}:{NETWORK_PORT}",
        'network_url': f"http://{local_ip}:{NETWORK_PORT}",
        'hostname': socket.gethostname()
    }

def generate_qr_code(url):
    """Generate QR code for the network URL"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for embedding in HTML
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

def register_mdns_service():
    """Register the application as an mDNS service for automatic discovery"""
    try:
        local_ip = get_local_ip()
        hostname = socket.gethostname()
        
        # Create service info
        service_name = f"Daiva Anughara._http._tcp.local."
        service_info = ServiceInfo(
            "_http._tcp.local.",
            service_name,
            addresses=[socket.inet_aton(local_ip)],
            port=NETWORK_PORT,
            properties={
                'path': '/',
                'name': 'Daiva Anughara',
                'description': 'Sacred Spiritual Practice Website',
                'version': '1.0.0'
            },
            server=f"{hostname}.local."
        )
        
        # Register the service
        zeroconf = Zeroconf()
        zeroconf.register_service(service_info)
        
        print(f"✅ mDNS service registered: {service_name}")
        print(f"   Discoverable as: http://{hostname}.local:{NETWORK_PORT}")
        
        return zeroconf, service_info
        
    except Exception as e:
        print(f"❌ Failed to register mDNS service: {e}")
        return None, None

def unregister_mdns_service(zeroconf, service_info):
    """Unregister the mDNS service"""
    try:
        if zeroconf and service_info:
            zeroconf.unregister_service(service_info)
            zeroconf.close()
            print("✅ mDNS service unregistered")
    except Exception as e:
        print(f"❌ Error unregistering mDNS service: {e}")

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Sample Ashtami dates data
ASHTAMI_DATES = [
    {
        'date': '2024-09-14',
        'start_time': '05:04',
        'end_time': '2024-09-15 03:06',
        'description': 'Krishna Paksha Ashtami'
    },
    {
        'date': '2024-10-14',
        'start_time': '04:30',
        'end_time': '2024-10-15 02:45',
        'description': 'Krishna Paksha Ashtami'
    }
]

# Routes
@app.route('/')
def home():
    network_info = get_network_info()
    return render_template('home.html', page_title='Home - Daiva Anughara', network_info=network_info)


@app.route('/documents')
def documents():
    return render_template('documents.html', page_title='Documents & Updates - Daiva Anughara')

@app.route('/ashtami')
def ashtami():
    return render_template('ashtami.html', page_title='Ashtami Sadhana - Daiva Anughara')

@app.route('/devi')
def devi():
    return render_template('devi.html', page_title='Devi Maa - Daiva Anughara')

@app.route('/about')
def about():
    return render_template('about.html', page_title='About - Daiva Anughara')

@app.route('/youtube')
def youtube():
    return render_template('youtube.html', page_title='YouTube - Daiva Anughara')


@app.route('/padati')
@login_required
def padati():
    return render_template('padati.html', page_title='Padati for You - Daiva Anughara')

@app.route('/donations')
def donations():
    """Public donations page - shows only verified donations from local database"""
    try:
        # Always fetch from local database for public users
        data_source = "Local Database"
        
        # Get recent verified donations (last 30 days)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_donations = OfflineDonation.query.filter(
            OfflineDonation.is_verified == True,
            OfflineDonation.donation_date >= thirty_days_ago
        ).order_by(OfflineDonation.donation_date.desc()).limit(50).all()
        
        # Get all purposes for grouping
        purposes = DonationPurpose.query.filter_by(is_active=True).all()
        
        # Group donations by purpose
        all_worksheet_data = {}
        total_donations = 0
        total_amount = 0
        
        for purpose in purposes:
            purpose_donations = [d for d in recent_donations if d.purpose_id == purpose.id]
            
            if purpose_donations:  # Only show purposes that have donations
                purpose_amount = sum(d.amount for d in purpose_donations)
                all_worksheet_data[purpose.name] = {
                    'donations': purpose_donations,
                    'summary': {
                        'total_donations': len(purpose_donations),
                        'total_amount': purpose_amount,
                        'verified_donations': len(purpose_donations),
                        'pending_donations': 0,
                        'average_donation': purpose_amount / len(purpose_donations) if purpose_donations else 0
                    },
                    'all_donations': purpose_donations
                }
                
                total_donations += len(purpose_donations)
                total_amount += purpose_amount
        
        # If no purpose-specific donations, show all donations in one tab
        if not all_worksheet_data:
            all_worksheet_data = {
                'All Donations': {
                    'donations': recent_donations,
                    'summary': {
                        'total_donations': len(recent_donations),
                        'total_amount': sum(d.amount for d in recent_donations),
                        'verified_donations': len(recent_donations),
                        'pending_donations': 0,
                        'average_donation': sum(d.amount for d in recent_donations) / len(recent_donations) if recent_donations else 0
                    },
                    'all_donations': recent_donations
                }
            }
            total_donations = len(recent_donations)
            total_amount = sum(d.amount for d in recent_donations)
        
    except Exception as e:
        print(f"Error fetching donations from database: {e}")
        # Fallback to empty data
        data_source = "Local Database"
        all_worksheet_data = {}
        purposes = []
        total_donations = 0
        total_amount = 0
    
    return render_template('donations.html',
                         all_worksheet_data=all_worksheet_data,
                         purposes=purposes,
                         total_donations=total_donations,
                         total_amount=total_amount,
                         data_source=data_source,
                         page_title="Donations")

@app.route('/admin/donations')
@login_required
def admin_donations():
    """Admin donations management page - shows all donations from local database with tabs"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    try:
        # Always fetch from local database (after sync)
        data_source = "Local Database"
        
        # Get all donations from local database
        all_donations = OfflineDonation.query.order_by(OfflineDonation.donation_date.desc()).all()
        
        # Group donations by worksheet
        all_worksheet_data = {}
        total_donations = 0
        total_amount = 0
        
        # Group by worksheet
        worksheets_dict = {}
        for donation in all_donations:
            worksheet_name = donation.worksheet if donation.worksheet else (donation.purpose.name if donation.purpose else 'Uncategorized')
            if worksheet_name not in worksheets_dict:
                worksheets_dict[worksheet_name] = []
            worksheets_dict[worksheet_name].append(donation)
        
        # Create worksheet data structure
        for worksheet_name, donations in worksheets_dict.items():
            worksheet_amount = sum(float(d.amount) for d in donations)
            all_worksheet_data[worksheet_name] = {
                'donations': donations,
                'summary': {
                    'total_donations': len(donations),
                    'total_amount': worksheet_amount,
                    'verified_donations': len([d for d in donations if d.is_verified]),
                    'pending_donations': len([d for d in donations if not d.is_verified]),
                    'average_donation': worksheet_amount / len(donations) if donations else 0
                },
                'all_donations': donations
            }
            
            total_donations += len(donations)
            total_amount += worksheet_amount
        
        # Get all purposes for reference
        all_purposes = DonationPurpose.query.filter_by(is_active=True).all()
        
        # Get recent donations for stats (last 30 days)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        recent_donations = OfflineDonation.query.filter(
            OfflineDonation.donation_date >= thirty_days_ago
        ).order_by(OfflineDonation.donation_date.desc()).limit(10).all()
        
    except Exception as e:
        print(f"Error fetching donations: {e}")
        # Fallback to empty data
        data_source = "Error - No Data Available"
        all_worksheet_data = {}
        all_purposes = []
        total_donations = 0
        total_amount = 0
        recent_donations = []
    
    return render_template('admin/donations.html',
                         page_title='Donation Management - Daiva Anughara',
                         all_worksheet_data=all_worksheet_data,
                         all_purposes=all_purposes,
                         total_donations=total_donations,
                         total_amount=total_amount,
                         recent_donations=recent_donations,
                         data_source=data_source)

@app.route('/admin/donations/add', methods=['GET', 'POST'])
@login_required
def add_donation():
    """Add new offline donation"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    form = OfflineDonationForm()
    
    # Populate purpose choices
    purposes = DonationPurpose.query.filter_by(is_active=True).all()
    form.purpose_id.choices = [(p.id, p.name) for p in purposes]
    
    if form.validate_on_submit():
        try:
            # Parse donation date
            donation_date = datetime.strptime(form.donation_date.data, '%Y-%m-%d').date()
            
            # Create donation record
            donation = OfflineDonation(
                donor_name=form.donor_name.data,
                donor_email=form.donor_email.data,
                donor_phone=form.donor_phone.data,
                amount=float(form.amount.data),
                currency=form.currency.data,
                purpose_id=form.purpose_id.data,
                donation_date=donation_date,
                payment_method=form.payment_method.data,
                reference_number=form.reference_number.data,
                notes=form.notes.data,
                created_by=current_user.id
            )
            
            db.session.add(donation)
            db.session.commit()
            
            # Add to Google Sheets
            purpose = DonationPurpose.query.get(form.purpose_id.data)
            donation_data = {
                'id': donation.id,
                'donor_name': donation.donor_name,
                'donor_email': donation.donor_email,
                'donor_phone': donation.donor_phone,
                'amount': donation.amount,
                'currency': donation.currency,
                'donation_date': donation.donation_date.strftime('%Y-%m-%d'),
                'payment_method': donation.payment_method,
                'reference_number': donation.reference_number,
                'notes': donation.notes,
                'is_verified': donation.is_verified,
                'created_at': donation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'created_by': current_user.username
            }
            
            get_sheets_manager().add_donation(donation_data, purpose.name)
            
            flash('Donation added successfully!', 'success')
            return redirect(url_for('admin_donations'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding donation: {str(e)}', 'error')
    
    return render_template('admin/add_donation.html',
                         page_title='Add Donation - Daiva Anughara',
                         form=form)

@app.route('/admin/donations/verify/<int:donation_id>')
@login_required
def verify_donation(donation_id):
    """Verify a donation"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    donation = OfflineDonation.query.get_or_404(donation_id)
    
    if donation.is_verified:
        flash('Donation is already verified.', 'info')
    else:
        donation.is_verified = True
        donation.verified_at = datetime.now()
        donation.verified_by = current_user.id
        db.session.commit()
        
        # Update Google Sheets
        purpose = donation.purpose
        donation_data = {
            'id': donation.id,
            'donor_name': donation.donor_name,
            'donor_email': donation.donor_email,
            'donor_phone': donation.donor_phone,
            'amount': donation.amount,
            'currency': donation.currency,
            'donation_date': donation.donation_date.strftime('%Y-%m-%d'),
            'payment_method': donation.payment_method,
            'reference_number': donation.reference_number,
            'notes': donation.notes,
            'is_verified': donation.is_verified,
            'created_at': donation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': donation.creator.username
        }
        
        get_sheets_manager().add_donation(donation_data, purpose.name)
        
        flash('Donation verified successfully!', 'success')
    
    return redirect(url_for('admin_donations'))

@app.route('/admin/donation-purposes')
@login_required
def donation_purposes():
    """Manage donation purposes"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    purposes = DonationPurpose.query.order_by(DonationPurpose.created_at.desc()).all()
    return render_template('admin/donation_purposes.html',
                         page_title='Donation Purposes - Daiva Anughara',
                         purposes=purposes)

@app.route('/admin/donation-purposes/add', methods=['GET', 'POST'])
@login_required
def add_donation_purpose():
    """Add new donation purpose"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    form = DonationPurposeForm()
    
    if form.validate_on_submit():
        try:
            purpose = DonationPurpose(
                name=form.name.data,
                description=form.description.data,
                created_by=current_user.id
            )
            
            db.session.add(purpose)
            db.session.commit()
            
            flash('Donation purpose added successfully!', 'success')
            return redirect(url_for('donation_purposes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding donation purpose: {str(e)}', 'error')
    
    return render_template('admin/add_donation_purpose.html',
                         page_title='Add Donation Purpose - Daiva Anughara',
                         form=form)

@app.route('/admin/donation-purposes/toggle/<int:purpose_id>')
@login_required
def toggle_donation_purpose(purpose_id):
    """Toggle donation purpose active status"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    purpose = DonationPurpose.query.get_or_404(purpose_id)
    purpose.is_active = not purpose.is_active
    db.session.commit()
    
    status = 'activated' if purpose.is_active else 'deactivated'
    flash(f'Donation purpose {status} successfully!', 'success')
    
    return redirect(url_for('donation_purposes'))

@app.route('/admin/sync-donations')
@login_required
def sync_donations():
    """Admin-only sync donations from Google Sheets to local database"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    if not get_sheets_manager().is_connected():
        flash('❌ Google Sheets not connected. Please set up credentials first.', 'error')
        return redirect(url_for('admin_donations'))
    
    try:
        success, message = get_sheets_manager().sync_donations_from_sheets()
        if success:
            flash(f'✅ {message}', 'success')
        else:
            flash(f'❌ {message}', 'error')
    except Exception as e:
        flash(f'❌ Error syncing donations: {str(e)}', 'error')
    
    return redirect(url_for('admin_donations'))

@app.route('/admin/api/sync-donations', methods=['POST'])
@login_required
def api_sync_donations():
    """API endpoint for syncing donations (returns JSON)"""
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    if not get_sheets_manager().is_connected():
        return jsonify({
            'success': False,
            'error': 'Google Sheets not connected. Please set up credentials first.'
        }), 400
    
    try:
        success, message = get_sheets_manager().sync_donations_from_sheets()
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error syncing donations: {str(e)}'
        }), 500

# Alternative sync endpoint without CSRF protection
@app.route('/admin/sync-now', methods=['GET'])
@login_required
def sync_now():
    """Alternative sync endpoint without CSRF protection"""
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    if not get_sheets_manager().is_connected():
        return jsonify({
            'success': False,
            'error': 'Google Sheets not connected. Please set up credentials first.'
        }), 400
    
    try:
        success, message = get_sheets_manager().sync_donations_from_sheets()
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/admin/sync-status')
@login_required
def sync_status():
    """Check Google Sheets connection status (admin only)"""
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Lightweight check - just verify if credentials exist
        # Don't actually connect to Google Sheets
        credentials_exist = (
            os.path.exists('google_credentials.json') or 
            os.getenv('GOOGLE_CREDENTIALS_JSON') is not None
        )
        
        return jsonify({
            'connected': credentials_exist,
            'message': 'Credentials available' if credentials_exist else 'No credentials found'
        })
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e)
        })

@app.route('/admin/api/donations-from-sheets')
@login_required
def admin_api_donations_from_sheets():
    """Admin-only API endpoint to get donations from Google Sheets"""
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    if not get_sheets_manager().is_connected():
        return jsonify({
            'success': False,
            'error': 'Google Sheets not connected',
            'donations': [],
            'count': 0
        })
    
    try:
        donations = get_sheets_manager().get_all_donations_from_sheets()
        return jsonify({
            'success': True,
            'donations': donations,
            'count': len(donations)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'donations': [],
            'count': 0
        })

# Mandala Sadhana Routes
@app.route('/mandala-sadhana', methods=['GET', 'POST'])
@login_required
def mandala_sadhana_registration():
    """Mandala Sadhana registration form - requires login"""
    # Check if user is approved (for non-admin users)
    if not current_user.is_admin() and not current_user.is_approved:
        flash('Your account needs to be approved before you can access Mandala Sadhana registration.', 'warning')
        return redirect(url_for('auth.profile'))
    
    form = MandalaSadhanaRegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Convert boolean values
            mandala_48_commitment = (form.mandala_48_commitment.data == 'Yes') if form.mandala_48_commitment.data else False
            send_copy = (form.send_copy.data == 'True') if form.send_copy.data else False
            
            # Create registration record
            registration = MandalaSadhanaRegistration(
                email=form.email.data,
                full_name=form.full_name.data,
                mandala_48_commitment=mandala_48_commitment,
                mandala_144_commitment=form.mandala_144_commitment.data or 'No',
                commitment_text=form.commitment_text.data,
                sadhana_start_date=form.sadhana_start_date.data,
                sadhana_type=form.sadhana_type.data,
                send_copy=send_copy
            )
            
            db.session.add(registration)
            db.session.commit()
            
            flash('Mandala Sadhana registration submitted successfully! Jai Bhairava! 🙏', 'success')
            return redirect(url_for('mandala_sadhana_registration'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting registration: {str(e)}', 'error')
    
    return render_template('mandala_sadhana_form.html', 
                         page_title='Mandala Sadhana Registration - Daiva Anughara',
                         form=form)

@app.route('/api/mandala-sadhana', methods=['POST'])
@login_required
def api_mandala_sadhana_registration():
    """API endpoint for Mandala Sadhana registration (for AJAX submissions) - requires login"""
    # Check if user is approved (for non-admin users)
    if not current_user.is_admin() and not current_user.is_approved:
        return jsonify({
            'success': False, 
            'error': 'Your account needs to be approved before you can access Mandala Sadhana registration.'
        }), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'full_name', 'mandala_48_commitment', 'mandala_144_commitment', 
                          'commitment_text', 'sadhana_start_date', 'sadhana_type']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Convert boolean values
        mandala_48_commitment = data['mandala_48_commitment'] == 'Yes'
        send_copy = data.get('send_copy', False)
        
        # Parse date
        from datetime import datetime
        sadhana_start_date = datetime.strptime(data['sadhana_start_date'], '%Y-%m-%d').date()
        
        # Create registration record
        registration = MandalaSadhanaRegistration(
            email=data['email'],
            full_name=data['full_name'],
            mandala_48_commitment=mandala_48_commitment,
            mandala_144_commitment=data['mandala_144_commitment'],
            commitment_text=data['commitment_text'],
            sadhana_start_date=sadhana_start_date,
            sadhana_type=data['sadhana_type'],
            send_copy=send_copy
        )
        
        db.session.add(registration)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mandala Sadhana registration submitted successfully! Jai Bhairava! 🙏',
            'registration_id': registration.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error submitting registration: {str(e)}'
        }), 500

@app.route('/admin/mandala-sadhana')
@login_required
def admin_mandala_sadhana():
    """Admin page for viewing Mandala Sadhana registrations"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    # Get search parameters
    search_term = request.args.get('search_term', '')
    mandala_48_filter = request.args.get('mandala_48_filter', 'all')
    mandala_144_filter = request.args.get('mandala_144_filter', 'all')
    sadhana_type_filter = request.args.get('sadhana_type_filter', 'all')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = MandalaSadhanaRegistration.query
    
    # Apply filters
    if search_term:
        query = query.filter(
            db.or_(
                MandalaSadhanaRegistration.full_name.contains(search_term),
                MandalaSadhanaRegistration.email.contains(search_term),
                MandalaSadhanaRegistration.sadhana_type.contains(search_term)
            )
        )
    
    if mandala_48_filter != 'all':
        query = query.filter(MandalaSadhanaRegistration.mandala_48_commitment == (mandala_48_filter == 'Yes'))
    
    if mandala_144_filter != 'all':
        query = query.filter(MandalaSadhanaRegistration.mandala_144_commitment == mandala_144_filter)
    
    if sadhana_type_filter != 'all':
        query = query.filter(MandalaSadhanaRegistration.sadhana_type == sadhana_type_filter)
    
    if date_from:
        try:
            from datetime import datetime
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(MandalaSadhanaRegistration.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            from datetime import datetime
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(MandalaSadhanaRegistration.created_at <= date_to_obj)
        except ValueError:
            pass
    
    # Get registrations
    registrations = query.order_by(MandalaSadhanaRegistration.created_at.desc()).all()
    
    # Get statistics
    total_registrations = len(registrations)
    mandala_48_yes = len([r for r in registrations if r.mandala_48_commitment])
    mandala_144_yes = len([r for r in registrations if r.mandala_144_commitment == 'Yes'])
    mandala_144_not_ready = len([r for r in registrations if r.mandala_144_commitment == 'Not Yet Ready'])
    
    # Group by sadhana type
    sadhana_type_stats = {}
    for registration in registrations:
        sadhana_type = registration.sadhana_type
        if sadhana_type not in sadhana_type_stats:
            sadhana_type_stats[sadhana_type] = 0
        sadhana_type_stats[sadhana_type] += 1
    
    # Create search form
    search_form = MandalaSadhanaSearchForm()
    search_form.search_term.data = search_term
    search_form.mandala_48_filter.data = mandala_48_filter
    search_form.mandala_144_filter.data = mandala_144_filter
    search_form.sadhana_type_filter.data = sadhana_type_filter
    search_form.date_from.data = date_from
    search_form.date_to.data = date_to
    
    return render_template('admin/mandala_sadhana.html',
                         page_title='Mandala Sadhana Registrations - Daiva Anughara',
                         registrations=registrations,
                         total_registrations=total_registrations,
                         mandala_48_yes=mandala_48_yes,
                         mandala_144_yes=mandala_144_yes,
                         mandala_144_not_ready=mandala_144_not_ready,
                         sadhana_type_stats=sadhana_type_stats,
                         search_form=search_form)

@app.route('/admin/mandala-sadhana/export')
@login_required
def admin_mandala_sadhana_export():
    """Export Mandala Sadhana registrations to CSV"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    try:
        import csv
        from io import StringIO
        
        # Get all registrations
        registrations = MandalaSadhanaRegistration.query.order_by(MandalaSadhanaRegistration.created_at.desc()).all()
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Email', 'Full Name & Geo Location', '48-Day Mandala Commitment',
            '144-Day Mandala Commitment', 'Commitment Text', 'Sadhana Start Date',
            'Sadhana Type', 'Send Copy', 'Created At', 'Updated At'
        ])
        
        # Write data
        for registration in registrations:
            writer.writerow([
                registration.id,
                registration.email,
                registration.full_name,
                'Yes' if registration.mandala_48_commitment else 'No',
                registration.mandala_144_commitment,
                registration.commitment_text,
                registration.sadhana_start_date.strftime('%Y-%m-%d') if registration.sadhana_start_date else '',
                registration.sadhana_type,
                'Yes' if registration.send_copy else 'No',
                registration.created_at.strftime('%Y-%m-%d %H:%M:%S') if registration.created_at else '',
                registration.updated_at.strftime('%Y-%m-%d %H:%M:%S') if registration.updated_at else ''
            ])
        
        # Prepare response
        output.seek(0)
        from flask import Response
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=mandala_sadhana_registrations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        )
        
    except Exception as e:
        flash(f'Error exporting data: {str(e)}', 'error')
        return redirect(url_for('admin_mandala_sadhana'))

@app.route('/admin/mandala-sadhana/<int:registration_id>')
@login_required
def admin_mandala_sadhana_detail(registration_id):
    """View detailed information about a specific registration"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    registration = MandalaSadhanaRegistration.query.get_or_404(registration_id)
    
    return render_template('admin/mandala_sadhana_detail.html',
                         page_title=f'Registration Details - {registration.full_name}',
                         registration=registration)


# API Routes
@app.route('/api/next-ashtami')
def next_ashtami():
    """Get the next upcoming Ashtami date"""
    today = datetime.now().date()
    
    for ashtami in ASHTAMI_DATES:
        ashtami_date = datetime.strptime(ashtami['date'], '%Y-%m-%d').date()
        if ashtami_date >= today:
            return jsonify(ashtami)
    
    # If no future dates found, return the first one
    return jsonify(ASHTAMI_DATES[0] if ASHTAMI_DATES else None)

@app.route('/api/countdown')
def countdown():
    """Get countdown data for the next Ashtami"""
    next_ashtami = request.args.get('next_ashtami')
    
    if not next_ashtami:
        return jsonify({'error': 'No Ashtami date provided'}), 400
    
    try:
        # Parse the Ashtami date
        ashtami_date = datetime.strptime(next_ashtami, '%Y-%m-%d')
        now = datetime.now()
        
        if ashtami_date <= now:
            return jsonify({'error': 'Ashtami date has passed'}), 400
        
        # Calculate time difference
        time_diff = ashtami_date - now
        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        
        return jsonify({
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'total_seconds': int(time_diff.total_seconds())
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

@app.route('/api/network-info')
def api_network_info():
    """Get network information as JSON"""
    network_info = get_network_info()
    qr_code = generate_qr_code(network_info['url'])
    network_info['qr_code'] = qr_code
    return jsonify(network_info)

@app.route('/network-diagnostics')
def network_diagnostics():
    """Network diagnostics page for troubleshooting"""
    import subprocess
    import platform
    
    # Get basic network info
    network_info = get_network_info()
    
    # Get all network interfaces
    all_interfaces = get_all_network_interfaces()
    
    # Test if port is accessible
    port_open = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', NETWORK_PORT))
            port_open = (result == 0)
    except Exception:
        port_open = False
    
    # Get system info
    system_info = {
        'platform': platform.system(),
        'hostname': socket.gethostname(),
        'python_version': platform.python_version(),
        'port_open': port_open
    }
    
    # Get network connectivity test
    connectivity_test = {}
    try:
        # Test if we can reach external network
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.connect(("8.8.8.8", 80))
            connectivity_test['external'] = True
    except Exception:
        connectivity_test['external'] = False
    
    return render_template('network_diagnostics.html',
                         page_title='Network Diagnostics - Daiva Anughara',
                         network_info=network_info,
                         all_interfaces=all_interfaces,
                         system_info=system_info,
                         connectivity_test=connectivity_test)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', page_title='Page Not Found - Daiva Anughara'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', page_title='Server Error - Daiva Anughara'), 500

# Context processors
@app.context_processor
def inject_user():
    """Inject current user into all templates"""
    return dict(current_user=current_user)

@app.context_processor
def inject_flash_messages():
    """Inject flash messages into all templates"""
    from flask import get_flashed_messages
    return dict(get_flashed_messages=get_flashed_messages)

@app.context_processor
def inject_csrf_token():
    """Inject CSRF token into all templates"""
    return dict(csrf_token=generate_csrf)

# Create admin user function
def create_admin_user():
    """Create the initial admin user if it doesn't exist"""
    with app.app_context():
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@daivaanughara.com',
                full_name='Administrator',
                role='admin',
                is_approved=True,
                is_active=True,
                purpose='Administrator account for system management and user approval.',
                mandala_1_access=True,
                mandala_2_access=True,
                mandala_3_access=True
            )
            admin.set_password('admin123')  # Change this password in production!
            
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("Please change the password after first login!")

if __name__ == '__main__':
    # Create admin user on first run
    create_admin_user()
    
    # Get network information
    network_info = get_network_info()
    
    # Register mDNS service for automatic discovery
    zeroconf, service_info = register_mdns_service()
    
    print("\n" + "="*60)
    print("🌐 DAIVA ANUGHARA - NETWORK ACCESS INFORMATION")
    print("="*60)
    print(f"📱 Local Access: http://localhost:{NETWORK_PORT}")
    print(f"🌍 Network Access: {network_info['url']}")
    print(f"🖥️  Hostname: {network_info['hostname']}")
    print(f"🔍 mDNS Discovery: http://{network_info['hostname']}.local:{NETWORK_PORT}")
    print("="*60)
    print("📱 Share this URL with devices on the same WiFi network:")
    print(f"   {network_info['url']}")
    print("="*60)
    print("🔍 Devices can also discover this service automatically via mDNS")
    print("   (Look for 'Daiva Anughara' in network services)")
    print("="*60)
    print("🚀 Server starting...")
    print("="*60 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=NETWORK_PORT)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
    finally:
        # Clean up mDNS service
        unregister_mdns_service(zeroconf, service_info)
