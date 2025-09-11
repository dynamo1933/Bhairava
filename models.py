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