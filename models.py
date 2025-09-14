from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Additional fields for spiritual practice
    spiritual_name = db.Column(db.String(100), nullable=True)
    guru_name = db.Column(db.String(100), nullable=True)
    practice_level = db.Column(db.String(50), nullable=True)  # Beginner, Intermediate, Advanced
    purpose = db.Column(db.Text, nullable=False)  # Purpose for starting sadhana
    
    # Profile picture
    profile_picture = db.Column(db.String(255), nullable=True)  # Path to profile picture
    
    # Mandala access permissions
    mandala_1_access = db.Column(db.Boolean, default=True)  # All users get access to Mandala 1
    mandala_2_access = db.Column(db.Boolean, default=False)  # Admin must approve
    mandala_3_access = db.Column(db.Boolean, default=False)  # Admin must approve
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def can_login(self):
        return self.is_active and (self.is_admin() or self.is_approved)
    
    def has_mandala_access(self, mandala_number):
        """Check if user has access to a specific mandala"""
        if mandala_number == 1:
            return self.mandala_1_access
        elif mandala_number == 2:
            return self.mandala_2_access
        elif mandala_number == 3:
            return self.mandala_3_access
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'

class DonationPurpose(db.Model):
    """Model for donation purposes/categories"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_purposes')
    
    def __repr__(self):
        return f'<DonationPurpose {self.name}>'

class OfflineDonation(db.Model):
    """Model for tracking offline donations"""
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.String(50), nullable=True)  # Donor ID from Google Sheets (not unique)
    worksheet = db.Column(db.String(100), nullable=True)  # Worksheet name from Google Sheets
    donor_name = db.Column(db.String(100), nullable=False)
    donor_email = db.Column(db.String(120), nullable=True)
    donor_phone = db.Column(db.String(20), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='INR')
    purpose_id = db.Column(db.Integer, db.ForeignKey('donation_purpose.id'), nullable=False)
    donation_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # Cash, Bank Transfer, UPI, etc.
    reference_number = db.Column(db.String(100), nullable=True)  # Transaction reference
    notes = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verified_at = db.Column(db.DateTime, nullable=True)
    verified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relationships
    purpose = db.relationship('DonationPurpose', backref='donations')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_donations')
    verifier = db.relationship('User', foreign_keys=[verified_by], backref='verified_donations')
    
    def __repr__(self):
        return f'<OfflineDonation {self.donor_name} - {self.amount} {self.currency}>'

class MandalaSadhanaRegistration(db.Model):
    """Model for Mandala Sadhana registrations"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)  # Full Name & Geo Location
    mandala_48_commitment = db.Column(db.Boolean, nullable=False)  # 48-day Mandala commitment
    mandala_144_commitment = db.Column(db.String(50), nullable=False)  # 144-day Mandala commitment (Yes/No/Not Yet Ready)
    commitment_text = db.Column(db.Text, nullable=False)  # Sadhana commitment question
    sadhana_start_date = db.Column(db.Date, nullable=False)  # When did Sadhana begin
    sadhana_type = db.Column(db.String(100), nullable=False)  # Type of Sadhana
    send_copy = db.Column(db.Boolean, default=False)  # Send copy of responses
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MandalaSadhanaRegistration {self.full_name} - {self.sadhana_type}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'mandala_48_commitment': self.mandala_48_commitment,
            'mandala_144_commitment': self.mandala_144_commitment,
            'commitment_text': self.commitment_text,
            'sadhana_start_date': self.sadhana_start_date.strftime('%Y-%m-%d') if self.sadhana_start_date else None,
            'sadhana_type': self.sadhana_type,
            'send_copy': self.send_copy,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }