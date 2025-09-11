from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    spiritual_name = StringField('Spiritual Name (Optional)', validators=[Length(max=100)])
    guru_name = StringField('Guru Name (Optional)', validators=[Length(max=100)])
    practice_level = SelectField('Practice Level', choices=[
        ('', 'Select Practice Level'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ])
    purpose = TextAreaField('Purpose for Starting Sadhana', validators=[
        DataRequired(), 
        Length(min=20, max=1000, message='Please explain your purpose in 20-1000 characters')
    ])
    profile_picture = FileField('Profile Picture (Optional)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files (JPG, PNG, GIF) are allowed!')
    ])

    def validate_username(self, username):
        # We'll handle this validation in the route to avoid circular imports
        pass

    def validate_email(self, email):
        # We'll handle this validation in the route to avoid circular imports
        pass

class AdminApprovalForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    action = SelectField('Action', choices=[
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('suspend', 'Suspend')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes (Optional)', validators=[Length(max=500)])

class UserSearchForm(FlaskForm):
    search_term = StringField('Search by Username, Email, or Full Name')
    status_filter = SelectField('Status Filter', choices=[
        ('all', 'All Users'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended')
    ])
    role_filter = SelectField('Role Filter', choices=[
        ('all', 'All Roles'),
        ('admin', 'Admin'),
        ('user', 'User')
    ])

class DonationPurposeForm(FlaskForm):
    name = StringField('Purpose Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])

class OfflineDonationForm(FlaskForm):
    donor_name = StringField('Donor Name', validators=[DataRequired(), Length(max=100)])
    donor_email = StringField('Donor Email', validators=[Optional(), Email(), Length(max=120)])
    donor_phone = StringField('Donor Phone', validators=[Optional(), Length(max=20)])
    amount = StringField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', choices=[
        ('INR', 'INR (₹)'),
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
        ('GBP', 'GBP (£)')
    ], default='INR')
    purpose_id = SelectField('Donation Purpose', coerce=int, validators=[DataRequired()])
    donation_date = StringField('Donation Date', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('Cheque', 'Cheque'),
        ('Card', 'Card Payment'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    reference_number = StringField('Reference Number', validators=[Optional(), Length(max=100)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])

class DonationSearchForm(FlaskForm):
    search_term = StringField('Search by Donor Name, Email, or Reference Number')
    purpose_filter = SelectField('Purpose Filter', choices=[('all', 'All Purposes')])
    status_filter = SelectField('Status Filter', choices=[
        ('all', 'All Donations'),
        ('verified', 'Verified'),
        ('pending', 'Pending Verification')
    ])
    date_from = StringField('From Date')
    date_to = StringField('To Date')