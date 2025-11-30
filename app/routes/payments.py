"""
Payment recording and management routes.
Handles payment categories, recording payments, marking status, and printing receipts.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date
from sqlalchemy import and_, func

from app.models import db, Payment, PaymentCategory, Student, Course, User
from app.decorators import accountant_required, admin_required
from app.forms import PaymentForm, PaymentCategoryForm

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


# ==================== PAYMENT CATEGORIES ====================

@payments_bp.route('/categories')
@admin_required
def list_categories():
    """List all payment categories"""
    categories = PaymentCategory.query.order_by(PaymentCategory.name).all()
    return render_template('payment_categories.html', categories=categories)


@payments_bp.route('/categories/create', methods=['GET', 'POST'])
@admin_required
def create_category():
    """Create new payment category"""
    form = PaymentCategoryForm()
    
    if form.validate_on_submit():
        # Check if category already exists
        existing = PaymentCategory.query.filter_by(name=form.name.data).first()
        if existing:
            flash('Payment category already exists', 'warning')
            return redirect(url_for('payments.list_categories'))
        
        category = PaymentCategory(
            name=form.name.data,
            description=form.description.data,
            default_amount=form.default_amount.data,
            is_active=form.is_active.data == 'True'
        )
        
        db.session.add(category)
        db.session.commit()
        flash(f'Payment category "{form.name.data}" created successfully!', 'success')
        return redirect(url_for('payments.list_categories'))
    
    return render_template('payment_category_form.html', form=form, title='Create Payment Category')


@payments_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_category(category_id):
    """Edit payment category"""
    category = PaymentCategory.query.get_or_404(category_id)
    form = PaymentCategoryForm()
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.default_amount = form.default_amount.data
        category.is_active = form.is_active.data == 'True'
        
        db.session.commit()
        flash(f'Payment category "{form.name.data}" updated successfully!', 'success')
        return redirect(url_for('payments.list_categories'))
    
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
        form.default_amount.data = category.default_amount
        form.is_active.data = 'True' if category.is_active else 'False'
    
    return render_template('payment_category_form.html', form=form, title='Edit Payment Category')


@payments_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@admin_required
def delete_category(category_id):
    """Delete payment category"""
    category = PaymentCategory.query.get_or_404(category_id)
    
    # Check if category has payments
    if category.payments.count() > 0:
        flash('Cannot delete category with existing payments', 'error')
        return redirect(url_for('payments.list_categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash(f'Payment category "{category.name}" deleted successfully!', 'success')
    return redirect(url_for('payments.list_categories'))


# ==================== PAYMENT RECORDS ====================

@payments_bp.route('/')
@login_required
def list_payments():
    """List all payment records with advanced filtering"""
    page = request.args.get('page', 1, type=int)
    student_id = request.args.get('student_id', type=int)
    status = request.args.get('status', '')
    category_id = request.args.get('category_id', type=int)
    method = request.args.get('method', '')
    course_id = request.args.get('course_id', type=int)
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    
    query = Payment.query
    
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if method:
        query = query.filter_by(method=method)
    
    if course_id:
        query = query.filter_by(course_id=course_id)
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date >= start_date)
        except ValueError:
            pass
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date <= end_date)
        except ValueError:
            pass
    
    payments = query.order_by(Payment.created_at.desc()).paginate(page=page, per_page=20)
    students = Student.query.order_by(Student.first_name, Student.last_name).all()
    categories = PaymentCategory.query.filter_by(is_active=True).order_by(PaymentCategory.name).all()
    courses = Course.query.order_by(Course.name).all()
    
    # Calculate statistics for filtered results
    filtered_query = Payment.query
    if student_id:
        filtered_query = filtered_query.filter_by(student_id=student_id)
    if status:
        filtered_query = filtered_query.filter_by(status=status)
    if category_id:
        filtered_query = filtered_query.filter_by(category_id=category_id)
    if method:
        filtered_query = filtered_query.filter_by(method=method)
    if course_id:
        filtered_query = filtered_query.filter_by(course_id=course_id)
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            filtered_query = filtered_query.filter(Payment.payment_date >= start_date)
        except ValueError:
            pass
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            filtered_query = filtered_query.filter(Payment.payment_date <= end_date)
        except ValueError:
            pass
    
    total_amount_due = filtered_query.with_entities(func.sum(Payment.amount_due)).scalar() or 0
    total_amount_paid = filtered_query.with_entities(func.sum(Payment.amount_paid)).scalar() or 0
    total_pending = total_amount_due - total_amount_paid
    
    return render_template('payments.html', 
                         payments=payments, 
                         students=students,
                         categories=categories,
                         courses=courses,
                         selected_student_id=student_id,
                         selected_status=status,
                         selected_category_id=category_id,
                         selected_method=method,
                         selected_course_id=course_id,
                         selected_start_date=start_date_str,
                         selected_end_date=end_date_str,
                         stats={
                             'total_due': total_amount_due,
                             'total_paid': total_amount_paid,
                             'total_pending': total_pending
                         })


@payments_bp.route('/record', methods=['GET', 'POST'])
@accountant_required
def record_payment():
    """Record a new payment"""
    form = PaymentForm()
    
    # Populate choices
    form.student.choices = [(0, 'Select Student')] + [
        (s.id, f'{s.full_name} - {s.registration_number}') 
        for s in Student.query.order_by(Student.first_name, Student.last_name).all()
    ]
    
    form.course.choices = [(0, 'Select Course (Optional)')] + [
        (c.id, c.name) 
        for c in Course.query.order_by(Course.name).all()
    ]
    
    if form.validate_on_submit():
        # Get a default category if none selected
        default_category = PaymentCategory.query.filter_by(is_active=True).first()
        
        payment = Payment(
            student_id=form.student.data,
            category_id=default_category.id if default_category else 1,
            course_id=form.course.data if form.course.data != 0 else None,
            amount_due=form.amount_due.data,
            amount_paid=form.amount_paid.data,
            security_fees=form.security_fees.data or 0,
            admission_fees=form.admission_fees.data or 0,
            status=form.status.data,
            payment_date=date.today(),
            method=form.method.data,
            reference_no=form.reference_no.data,
            recorded_by_user_id=current_user.id,
            notes=form.notes.data
        )
        
        db.session.add(payment)
        db.session.commit()
        flash('Payment recorded successfully!', 'success')
        return redirect(url_for('payments.view_payment', payment_id=payment.id))
    
    return render_template('payment_form.html', form=form, title='Record Payment')


@payments_bp.route('/<int:payment_id>')
@login_required
def view_payment(payment_id):
    """View payment details"""
    payment = Payment.query.get_or_404(payment_id)
    return render_template('payment_detail.html', payment=payment)


@payments_bp.route('/<int:payment_id>/edit', methods=['GET', 'POST'])
@accountant_required
def edit_payment(payment_id):
    """Edit payment record"""
    payment = Payment.query.get_or_404(payment_id)
    form = PaymentForm()
    
    # Populate choices
    form.student.choices = [(0, 'Select Student')] + [
        (s.id, f'{s.full_name} - {s.registration_number}') 
        for s in Student.query.order_by(Student.first_name, Student.last_name).all()
    ]
    
    form.course.choices = [(0, 'Select Course (Optional)')] + [
        (c.id, c.name) 
        for c in Course.query.order_by(Course.name).all()
    ]
    
    if form.validate_on_submit():
        payment.student_id = form.student.data
        payment.course_id = form.course.data if form.course.data != 0 else None
        payment.amount_due = form.amount_due.data
        payment.amount_paid = form.amount_paid.data
        payment.security_fees = form.security_fees.data or 0
        payment.admission_fees = form.admission_fees.data or 0
        payment.status = form.status.data
        payment.method = form.method.data
        payment.reference_no = form.reference_no.data
        payment.notes = form.notes.data
        
        db.session.commit()
        flash('Payment updated successfully!', 'success')
        return redirect(url_for('payments.view_payment', payment_id=payment.id))
    
    elif request.method == 'GET':
        form.student.data = payment.student_id
        form.course.data = payment.course_id or 0
        form.amount_due.data = payment.amount_due
        form.amount_paid.data = payment.amount_paid
        form.security_fees.data = payment.security_fees or 0
        form.admission_fees.data = payment.admission_fees or 0
        form.status.data = payment.status
        form.method.data = payment.method
        form.reference_no.data = payment.reference_no
        form.notes.data = payment.notes
    
    return render_template('payment_form.html', form=form, title='Edit Payment', payment=payment)


@payments_bp.route('/<int:payment_id>/mark-status', methods=['POST'])
@accountant_required
def mark_payment_status(payment_id):
    """Mark payment status (paid, pending, partial_paid)"""
    try:
        payment = Payment.query.get_or_404(payment_id)
        data = request.get_json()
        
        status = data.get('status')
        amount_paid = data.get('amount_paid', payment.amount_paid)
        
        if status not in ['paid', 'pending', 'partial_paid']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        payment.status = status
        payment.amount_paid = float(amount_paid)
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Payment status updated',
            'status': payment.status,
            'amount_paid': payment.amount_paid,
            'remaining': payment.amount_due_remaining
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@payments_bp.route('/<int:payment_id>/delete', methods=['POST'])
@admin_required
def delete_payment(payment_id):
    """Delete payment record"""
    payment = Payment.query.get_or_404(payment_id)
    student_name = payment.student.full_name
    
    db.session.delete(payment)
    db.session.commit()
    
    flash(f'Payment for {student_name} deleted successfully!', 'success')
    return redirect(url_for('payments.list_payments'))


# ==================== PAYMENT RECEIPTS & PRINTING ====================

@payments_bp.route('/<int:payment_id>/student-slip')
@login_required
def student_slip(payment_id):
    """Print payment slip (student copy)"""
    payment = Payment.query.get_or_404(payment_id)
    return render_template('payment_student_slip.html', payment=payment)


@payments_bp.route('/<int:payment_id>/admin-slip')
@admin_required
def admin_slip(payment_id):
    """Print payment slip (admin copy)"""
    payment = Payment.query.get_or_404(payment_id)
    return render_template('payment_admin_slip.html', payment=payment)


@payments_bp.route('/summary')
@login_required
def payment_summary():
    """Payment summary and statistics with advanced filtering"""
    # Date range filtering
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    category_id = request.args.get('category_id', type=int)
    student_id = request.args.get('student_id', type=int)
    status = request.args.get('status', '')
    method = request.args.get('method', '')
    course_id = request.args.get('course_id', type=int)
    
    query = Payment.query
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date >= start_date)
        except ValueError:
            pass
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date <= end_date)
        except ValueError:
            pass
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if method:
        query = query.filter_by(method=method)
    
    if course_id:
        query = query.filter_by(course_id=course_id)
    
    payments = query.order_by(Payment.payment_date.desc()).all()
    
    # Calculate statistics
    total_due = sum(p.amount_due for p in payments)
    total_paid = sum(p.amount_paid for p in payments)
    total_pending = total_due - total_paid
    
    # Group by status
    status_summary = {
        'paid': len([p for p in payments if p.status == 'paid']),
        'pending': len([p for p in payments if p.status == 'pending']),
        'partial_paid': len([p for p in payments if p.status == 'partial_paid'])
    }
    
    # Group by category
    category_summary = {}
    for payment in payments:
        cat_name = payment.category.name if payment.category else 'Uncategorized'
        if cat_name not in category_summary:
            category_summary[cat_name] = {'due': 0, 'paid': 0, 'count': 0}
        category_summary[cat_name]['due'] += payment.amount_due
        category_summary[cat_name]['paid'] += payment.amount_paid
        category_summary[cat_name]['count'] += 1
    
    categories = PaymentCategory.query.order_by(PaymentCategory.name).all()
    students = Student.query.order_by(Student.first_name, Student.last_name).all()
    courses = Course.query.order_by(Course.name).all()
    
    return render_template('payment_summary.html',
                         payments=payments,
                         categories=categories,
                         students=students,
                         courses=courses,
                         selected_start_date=start_date_str,
                         selected_end_date=end_date_str,
                         selected_category_id=category_id,
                         selected_student_id=student_id,
                         selected_status=status,
                         selected_method=method,
                         selected_course_id=course_id,
                         stats={
                             'total_due': total_due,
                             'total_paid': total_paid,
                             'total_pending': total_pending,
                             'status_summary': status_summary,
                             'category_summary': category_summary
                         })


@payments_bp.route('/print-records')
@login_required
def print_records():
    """Print filtered payment records"""
    student_id = request.args.get('student_id', type=int)
    status = request.args.get('status', '')
    category_id = request.args.get('category_id', type=int)
    method = request.args.get('method', '')
    course_id = request.args.get('course_id', type=int)
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    
    query = Payment.query
    
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if method:
        query = query.filter_by(method=method)
    
    if course_id:
        query = query.filter_by(course_id=course_id)
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date >= start_date)
        except ValueError:
            pass
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Payment.payment_date <= end_date)
        except ValueError:
            pass
    
    payments = query.order_by(Payment.payment_date.desc()).all()
    
    # Calculate statistics
    total_due = sum(p.amount_due for p in payments)
    total_paid = sum(p.amount_paid for p in payments)
    total_pending = total_due - total_paid
    
    return render_template('print_payment_records.html',
                         payments=payments,
                         stats={
                             'total_due': total_due,
                             'total_paid': total_paid,
                             'total_pending': total_pending
                         },
                         print_date=datetime.now())


@payments_bp.route('/student/<int:student_id>/dues')
@login_required
def student_dues(student_id):
    """View student dues and payment history"""
    student = Student.query.get_or_404(student_id)
    payments = Payment.query.filter_by(student_id=student_id).order_by(Payment.created_at.desc()).all()
    
    # Calculate total dues
    total_due = sum(p.amount_due for p in payments)
    total_paid = sum(p.amount_paid for p in payments)
    total_pending = total_due - total_paid
    
    return render_template('student_dues.html',
                         student=student,
                         payments=payments,
                         stats={
                             'total_due': total_due,
                             'total_paid': total_paid,
                             'total_pending': total_pending
                         })

