"""
Payment recording routes.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from app.models import db, Payment, Student
from app.decorators import accountant_required

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


@payments_bp.route('/')
@accountant_required
def record_payment():
    """Record student payment"""
    return render_template('payments.html')


@payments_bp.route('/receipt/<int:payment_id>')
@login_required
def view_receipt(payment_id):
    """View payment receipt (PDF stub)"""
    payment = Payment.query.get_or_404(payment_id)
    return render_template('receipt.html', payment=payment)
