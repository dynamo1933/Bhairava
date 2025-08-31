from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
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
