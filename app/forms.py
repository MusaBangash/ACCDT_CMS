from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SelectField, RadioField, TextAreaField, SubmitField, SelectMultipleField, FloatField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional, ValidationError, NumberRange
from app.models import Student, Course


class StudentRegistrationForm(FlaskForm):
    """Form for student registration matching the admission form"""
    
    # Personal Information
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2-50 characters')
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2-50 characters')
    ])
    
    gender = RadioField('Gender', choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], validators=[DataRequired(message='Gender is required')])
    
    date_of_birth = DateField('Date of Birth', validators=[
        DataRequired(message='Date of birth is required')
    ])
    
    cnic = StringField('CNIC / B-Form', validators=[
        DataRequired(message='CNIC/B-Form is required'),
        Regexp(r'^\d{5}-\d{7}-\d{1}$', message='Invalid CNIC format. Use: 12345-1234567-1')
    ])
    
    blood_group = SelectField('Blood Group', choices=[
        ('', 'Select Blood Group'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-')
    ], validators=[Optional()])
    
    nationality = StringField('Nationality', validators=[
        DataRequired(message='Nationality is required'),
        Length(min=2, max=30, message='Nationality must be between 2-30 characters')
    ])
    
    phone = StringField('Mobile No', validators=[
        DataRequired(message='Mobile number is required'),
        Regexp(r'^03\d{9}$', message='Invalid mobile number. Use: 03001234567')
    ])
    
    emergency_contact = StringField('Emergency Contact', validators=[
        Optional(),
        Regexp(r'^03\d{9}$', message='Invalid mobile number format')
    ])
    
    # Address Information
    address = TextAreaField('Postal Address', validators=[
        DataRequired(message='Postal address is required'),
        Length(min=5, max=200, message='Address must be between 5-200 characters')
    ])
    
    permanent_address = TextAreaField('Permanent Address', validators=[
        DataRequired(message='Permanent address is required'),
        Length(min=5, max=200, message='Address must be between 5-200 characters')
    ])
    
    city = StringField('City', validators=[
        DataRequired(message='City is required'),
        Length(min=2, max=30, message='City name must be between 2-30 characters')
    ])
    
    # Guardian Information
    guardian_name = StringField("Father's / Guardian Name", validators=[
        DataRequired(message='Guardian name is required'),
        Length(min=2, max=50, message='Guardian name must be between 2-50 characters')
    ])
    
    guardian_cnic = StringField("Father's / Guardian CNIC", validators=[
        DataRequired(message='Guardian CNIC is required'),
        Regexp(r'^\d{5}-\d{7}-\d{1}$', message='Invalid CNIC format. Use: 12345-1234567-1')
    ])
    
    guardian_occupation = StringField('Occupation', validators=[Optional()])
    guardian_monthly_income = IntegerField('Monthly Income', validators=[Optional()])
    
    # Course & Category Selection
    course_id = SelectMultipleField('Select Courses', coerce=int, validators=[
        DataRequired(message='At least one course must be selected')
    ])
    
    admission_type = RadioField('Admission Type', choices=[
        ('day_scholar', 'Day Scholar'),
        ('hostel', 'Hostel')
    ], validators=[DataRequired(message='Admission type is required')])
    
    category = SelectField('Student Category', choices=[
        ('', 'Select Category'),
        ('regular', 'Regular'),
        ('needy', 'Needy'),
        ('orphan', 'Orphan'),
        ('sponsored', 'Sponsored'),
        ('staff_child', 'Staff Child'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    shift = RadioField('Shift', choices=[
        ('morning', 'Morning'),
        ('evening', 'Evening')
    ], validators=[DataRequired(message='Shift selection is required')])
    
    # Status Management
    registration_number = StringField('Registration Number (Leave empty to auto-generate)', validators=[Optional()])
    
    admission_date = DateField('Admission Date', validators=[Optional()])
    
    status = SelectField('Student Status', choices=[
        ('', 'Select Status'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('leave', 'On Leave')
    ], validators=[Optional()])
    
    # Qualifications
    last_qualification = StringField('Last Qualification', validators=[Optional()])
    current_qualification = StringField('Current Qualification', validators=[Optional()])
    
    # Additional Questions
    computer_skills = TextAreaField('Computer Skills', validators=[Optional()])
    course_goal = TextAreaField('Course Goal', validators=[Optional()])
    has_internet = RadioField('Has Internet', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ], validators=[Optional()])
    
    disability_type = StringField('Type of Disability', validators=[Optional()])
    special_needs = TextAreaField('Special Needs', validators=[Optional()])
    
    # Document Upload
    photo = FileField('Student Photo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only! (JPG/PNG)')
    ])
    
    character_certificate = FileField('Character Certificate', validators=[
        Optional(),
        FileAllowed(['pdf'], 'PDF only!')
    ])
    
    cnic_copy = FileField('CNIC Copy', validators=[
        Optional(),
        FileAllowed(['pdf'], 'PDF only!')
    ])
    
    qualification_certificate = FileField('Qualification Certificate', validators=[
        Optional(),
        FileAllowed(['pdf'], 'PDF only!')
    ])
    
    submit = SubmitField('Submit Registration')
    
    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        # Populate course choices dynamically for multiple selection
        self.course_id.choices = [
            (course.id, f"{course.name} (Rs. {course.fee:,.0f})")
            for course in Course.query.all()
        ]
    
    def validate_cnic(self, field):
        """Check if CNIC is not already registered"""
        existing = Student.query.filter_by(cnic=field.data).first()
        if existing:
            raise ValidationError('This CNIC is already registered.')
    
    def validate_phone(self, field):
        """Validate phone number format"""
        if not field.data.startswith('03'):
            raise ValidationError('Mobile number must start with 03')
        if len(field.data) != 11:
            raise ValidationError('Mobile number must be 11 digits')


class StudentStatusForm(FlaskForm):
    """Form for updating student status"""
    
    status = SelectField('Student Status', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('leave', 'On Leave')
    ], validators=[DataRequired(message='Status is required')])
    
    notes = TextAreaField('Status Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Status')


class CourseForm(FlaskForm):
    """Form for adding/editing courses"""
    
    name = StringField('Course Name', validators=[
        DataRequired(message='Course name is required'),
        Length(min=3, max=100, message='Course name must be between 3-100 characters')
    ])
    
    description = TextAreaField('Course Description', validators=[
        Optional(),
        Length(max=1000, message='Description must not exceed 1000 characters')
    ])
    
    instructor_name = StringField('Instructor Name', validators=[
        Optional(),
        Length(min=2, max=100, message='Instructor name must be between 2-100 characters')
    ])
    
    instructor_contact = StringField('Instructor Contact', validators=[
        Optional(),
        Regexp(r'^03\d{9}$|^$', message='Invalid mobile number. Use: 03001234567')
    ])
    
    fee = FloatField('Course Fee (Rs.)', validators=[
        DataRequired(message='Course fee is required'),
        NumberRange(min=0, message='Fee must be a positive number')
    ])
    
    seats = IntegerField('Number of Seats', validators=[
        DataRequired(message='Number of seats is required'),
        NumberRange(min=1, max=1000, message='Seats must be between 1-1000')
    ])
    
    course_outline = FileField('Course Outline (PDF)', validators=[
        Optional(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    
    submit = SubmitField('Save Course')


class AttendanceForm(FlaskForm):
    """Form for marking attendance"""
    
    course = SelectField('Select Course', coerce=int, validators=[
        DataRequired(message='Course selection is required')
    ])
    
    date = DateField('Attendance Date', validators=[
        DataRequired(message='Date is required')
    ])
    
    submit = SubmitField('Load Students')


class AttendanceRecordForm(FlaskForm):
    """Form for recording individual student attendance"""
    
    status = SelectField('Attendance Status', choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'On Leave')
    ], validators=[DataRequired(message='Status is required')])
    
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    
    submit = SubmitField('Save Attendance')


class PaymentCategoryForm(FlaskForm):
    """Form for managing payment categories"""
    
    name = StringField('Category Name', validators=[
        DataRequired(message='Category name is required'),
        Length(min=2, max=100, message='Category name must be 2-100 characters')
    ])
    
    description = TextAreaField('Description', validators=[
        Optional(), Length(max=500)
    ])
    
    default_amount = FloatField('Default Amount (Rs.)', validators=[
        DataRequired(message='Default amount is required'),
        NumberRange(min=0, message='Amount cannot be negative')
    ])
    
    is_active = SelectField('Status', choices=[
        ('True', 'Active'),
        ('False', 'Inactive')
    ], default='True')
    
    submit = SubmitField('Save Category')


class PaymentForm(FlaskForm):
    """Form for recording student payments"""
    
    student = SelectField('Student', coerce=int, validators=[
        DataRequired(message='Student selection is required')
    ])
    
    course = SelectField('Course (Optional)', coerce=int, validators=[
        Optional()
    ])
    
    amount_due = FloatField('Amount Due (Rs.)', validators=[
        DataRequired(message='Amount due is required'),
        NumberRange(min=0, message='Amount cannot be negative')
    ])
    
    amount_paid = FloatField('Amount Paid (Rs.)', validators=[
        DataRequired(message='Amount paid is required'),
        NumberRange(min=0, message='Amount cannot be negative')
    ])
    
    security_fees = FloatField('Security Fees (Rs.) - Optional', validators=[
        Optional(),
        NumberRange(min=0, message='Amount cannot be negative')
    ])
    
    admission_fees = FloatField('Admission Fees (Rs.) - Optional', validators=[
        Optional(),
        NumberRange(min=0, message='Amount cannot be negative')
    ])
    
    status = SelectField('Payment Status', choices=[
        ('pending', 'Pending'),
        ('partial_paid', 'Partial Paid'),
        ('paid', 'Paid')
    ], validators=[DataRequired(message='Status is required')])
    
    method = SelectField('Payment Method', choices=[
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online'),
        ('other', 'Other')
    ], validators=[DataRequired(message='Payment method is required')])
    
    reference_no = StringField('Reference No.', validators=[
        Optional(), Length(max=100)
    ])
    
    notes = TextAreaField('Notes', validators=[
        Optional(), Length(max=500)
    ])
    
    submit = SubmitField('Record Payment')

