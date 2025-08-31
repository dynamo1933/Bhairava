from flask import Flask, render_template, request, jsonify, send_from_directory, flash
from flask_login import LoginManager, current_user, login_required
from flask_wtf.csrf import CSRFProtect, generate_csrf
from models import db, User
from auth import auth
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daiva_anughara.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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
    return render_template('home.html', page_title='Home - Daiva Anughara')

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

@app.route('/padati')
@login_required
def padati():
    return render_template('padati.html', page_title='Padati for You - Daiva Anughara')

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
    
    app.run(debug=True, host='0.0.0.0', port=5000)
