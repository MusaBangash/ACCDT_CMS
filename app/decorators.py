"""
Custom decorators for authorization and role-based access control.
"""

from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user


def roles_required(*roles):
    """
    Decorator to require specific roles.
    
    Usage:
        @app.route('/admin-only')
        @roles_required('admin')
        def admin_page():
            ...
        
        @app.route('/financial')
        @roles_required('admin', 'accountant')
        def financial_page():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Require admin role - shorthand for @roles_required('admin')"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def teacher_required(f):
    """Require teacher role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.is_teacher() and not current_user.is_admin():
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def accountant_required(f):
    """Require accountant role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.is_accountant() and not current_user.is_admin():
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function
