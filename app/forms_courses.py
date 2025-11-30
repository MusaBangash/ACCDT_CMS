from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, NumberRange


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
