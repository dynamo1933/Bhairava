from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from models import db, User
from forms import LoginForm, RegistrationForm, AdminApprovalForm, UserSearchForm
from datetime import datetime
import os

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        
        if not user.can_login():
            if not user.is_approved and not user.is_admin():
                flash('Your account is pending approval. Please wait for admin approval.', 'warning')
            elif not user.is_active:
                flash('Your account has been suspended. Please contact admin.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('home')
        
        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Login', form=form, page_title='Login - Daiva Anughara')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check for existing username
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'error')
            return render_template('auth/register.html', title='Register', form=form)
        
        # Check for existing email
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use a different one.', 'error')
            return render_template('auth/register.html', title='Register', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            spiritual_name=form.spiritual_name.data,
            guru_name=form.guru_name.data,
            practice_level=form.practice_level.data,
            purpose=form.purpose.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please wait for admin approval before you can login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form, page_title='Register - Daiva Anughara')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@auth.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    search_form = UserSearchForm()
    approval_form = AdminApprovalForm()
    
    # Get search parameters
    search_term = request.args.get('search_term', '')
    status_filter = request.args.get('status_filter', 'all')
    role_filter = request.args.get('role_filter', 'all')
    
    # Build query
    query = User.query
    
    if search_term:
        query = query.filter(
            db.or_(
                User.username.contains(search_term),
                User.email.contains(search_term),
                User.full_name.contains(search_term)
            )
        )
    
    if status_filter != 'all':
        if status_filter == 'pending':
            query = query.filter_by(is_approved=False, is_active=True)
        elif status_filter == 'approved':
            query = query.filter_by(is_approved=True, is_active=True)
        elif status_filter == 'rejected':
            query = query.filter_by(is_approved=False, is_active=False)
        elif status_filter == 'suspended':
            query = query.filter_by(is_active=False)
    
    if role_filter != 'all':
        query = query.filter_by(role=role_filter)
    
    users = query.order_by(User.created_at.desc()).all()
    
    return render_template('admin/users.html', 
                         title='User Management',
                         page_title='User Management - Daiva Anughara',
                         users=users,
                         search_form=search_form,
                         approval_form=approval_form)

@auth.route('/admin/approve_user', methods=['POST'])
@login_required
def approve_user():
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    form = AdminApprovalForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        action = form.action.data
        notes = form.notes.data
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        if action == 'approve':
            user.is_approved = True
            user.approved_at = datetime.utcnow()
            user.approved_by = current_user.id
            user.is_active = True
            message = f'User {user.username} has been approved successfully.'
        elif action == 'reject':
            user.is_approved = False
            user.is_active = False
            message = f'User {user.username} has been rejected.'
        elif action == 'suspend':
            user.is_active = False
            message = f'User {user.username} has been suspended.'
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': message})
    
    return jsonify({'success': False, 'message': 'Invalid form data'}), 400

@auth.route('/admin/user/<int:user_id>')
@login_required
def admin_user_detail(user_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', title='User Detail', page_title='User Detail - Daiva Anughara', user=user)

@auth.route('/admin/user/<int:user_id>/mandala-access', methods=['POST'])
@login_required
def update_mandala_access(user_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('auth.admin_users'))
    
    user = User.query.get_or_404(user_id)
    
    # Get mandala access updates from form
    mandala_2_access = request.form.get('mandala_2_access') == 'on'
    mandala_3_access = request.form.get('mandala_3_access') == 'on'
    
    # Update mandala access
    user.mandala_2_access = mandala_2_access
    user.mandala_3_access = mandala_3_access
    
    db.session.commit()
    
    flash(f'Mandala access updated for {user.username}', 'success')
    return redirect(url_for('auth.admin_user_detail', user_id=user_id))

@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', title='Profile', page_title='Profile - Daiva Anughara')

@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # This would be implemented for users to edit their own profile
    pass
