"""
Admin panel routes for user management and system administration.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user

from app.models import db, User
from app.decorators import admin_required
from app.utils import paginate_query

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard - overview of system"""
    total_users = User.query.count()
    admins = User.query.filter_by(role='admin').count()
    accountants = User.query.filter_by(role='accountant').count()
    teachers = User.query.filter_by(role='teacher').count()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         admins=admins,
                         accountants=accountants,
                         teachers=teachers)


@admin_bp.route('/users')
@admin_required
def users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    query = User.query.order_by(User.created_at.desc())
    
    users_list, total, pages = paginate_query(query, page)
    
    return render_template('admin_users.html',
                         users=users_list,
                         page=page,
                         total=total,
                         pages=pages)


@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'teacher')
        
        # Validation
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters.', 'warning')
            return redirect(url_for('admin.create_user'))
        
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters.', 'warning')
            return redirect(url_for('admin.create_user'))
        
        if role not in ['admin', 'accountant', 'teacher']:
            flash('Invalid role selected.', 'warning')
            return redirect(url_for('admin.create_user'))
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
            return redirect(url_for('admin.create_user'))
        
        # Create user
        user = User(
            username=username,
            email=email if email else None,
            role=role
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'User {username} created successfully with role: {role}', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')
            return redirect(url_for('admin.create_user'))
    
    return render_template('admin_user_form.html', user=None)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user details and role"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'teacher')
        is_active = request.form.get('is_active') == 'on'
        password = request.form.get('password', '').strip()
        
        # Validation
        if role not in ['admin', 'accountant', 'teacher']:
            flash('Invalid role selected.', 'warning')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Prevent disabling the only admin
        if user.role == 'admin' and not is_active:
            admin_count = User.query.filter_by(role='admin', is_active=True).count()
            if admin_count <= 1:
                flash('Cannot disable the only active admin.', 'danger')
                return redirect(url_for('admin.edit_user', user_id=user_id))
        
        user.email = email if email else None
        user.role = role
        user.is_active = is_active
        
        # Update password if provided
        if password:
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'warning')
                return redirect(url_for('admin.edit_user', user_id=user_id))
            user.set_password(password)
        
        try:
            db.session.commit()
            flash(f'User {user.username} updated successfully.', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
    
    return render_template('admin_user_form.html', user=user)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting the only admin
    if user.role == 'admin':
        admin_count = User.query.filter_by(role='admin').count()
        if admin_count <= 1:
            flash('Cannot delete the only admin.', 'danger')
            return redirect(url_for('admin.users'))
    
    # Prevent self-deletion
    if user.id == current_user.id:
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    username = user.username
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {username} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/api/users', methods=['GET'])
@admin_required
def api_users():
    """API endpoint - get users as JSON"""
    page = request.args.get('page', 1, type=int)
    role = request.args.get('role', None)
    
    query = User.query
    if role:
        query = query.filter_by(role=role)
    
    query = query.order_by(User.created_at.desc())
    users_list, total, pages = paginate_query(query, page)
    
    return jsonify({
        'users': [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'role': u.role,
                'is_active': u.is_active,
                'created_at': u.created_at.isoformat()
            } for u in users_list
        ],
        'total': total,
        'page': page,
        'pages': pages
    })
