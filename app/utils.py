"""
Helper functions and utilities for the application.
"""

import os
import secrets
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def save_upload_file(file, folder='uploads'):
    """
    Save uploaded file securely to uploads folder.
    
    Args:
        file: FileStorage object from Flask
        folder: subfolder within UPLOAD_FOLDER
    
    Returns:
        filename if successful, None otherwise
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    # Generate secure filename with random suffix to avoid collisions
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{secrets.token_hex(4)}{ext}"
    
    # Create upload folder if it doesn't exist
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_path, filename)
    file.save(filepath)
    
    # Return relative path for database storage
    return f"{folder}/{filename}"


def delete_upload_file(filepath):
    """
    Delete uploaded file safely.
    
    Args:
        filepath: relative path to file (e.g., 'photos/file_abc123.jpg')
    
    Returns:
        True if deleted, False otherwise
    """
    if not filepath:
        return False
    
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
    
    # Security check - ensure path is within UPLOAD_FOLDER
    upload_folder = os.path.abspath(current_app.config['UPLOAD_FOLDER'])
    full_path_abs = os.path.abspath(full_path)
    
    if not full_path_abs.startswith(upload_folder):
        return False
    
    try:
        if os.path.exists(full_path_abs):
            os.remove(full_path_abs)
            return True
    except Exception as e:
        print(f"Error deleting file: {e}")
    
    return False


def format_date(date_obj, format='%Y-%m-%d'):
    """Format date object to string"""
    if date_obj:
        return date_obj.strftime(format)
    return None


def format_currency(amount):
    """Format amount as currency (Rs.)"""
    return f"Rs. {amount:,.2f}"


def paginate_query(query, page=1, per_page=None):
    """
    Paginate SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: page number (1-indexed)
        per_page: items per page (uses config if None)
    
    Returns:
        tuple of (items, total, pages)
    """
    if per_page is None:
        per_page = current_app.config.get('ITEMS_PER_PAGE', 10)
    
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return items, total, pages
