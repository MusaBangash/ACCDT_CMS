#!/usr/bin/env python
"""Database seeding script with registration numbers"""
import os
import sys
from datetime import date
import random

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, User, Student, Course, Enrollment, Setting

def seed_database():
    """Seed the database with initial data"""
    app = create_app()
    
    with app.app_context():
        # Initialize default settings
        Setting.set('reg_number_prefix', 'ACCDT', 'Registration number prefix')
        Setting.set('reg_number_format', '{prefix}-{year}-{count:05d}', 'Registration number format')
        Setting.set('school_name', 'ACCDT (Academy/College Management System)', 'School name')
        print('✓ Default settings initialized')
        
        # Check if admin exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@accdt.edu.pk', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print('✓ Admin user created: admin / admin123')
        
        # Create courses if not exist
        if Course.query.count() == 0:
            courses_data = [
                {
                    'name': 'Fashion Designing',
                    'description': 'Learn the fundamentals of fashion design, including sketching, pattern making, and garment construction.',
                    'instructor_name': 'Ms. Ayesha Khan',
                    'instructor_contact': '03001234501',
                    'fee': 18000,
                    'seats': 30
                },
                {
                    'name': 'Tailoring',
                    'description': 'Professional tailoring course covering stitching techniques, measurements, and custom clothing production.',
                    'instructor_name': 'Mr. Muhammad Ali',
                    'instructor_contact': '03002234502',
                    'fee': 12000,
                    'seats': 35
                },
                {
                    'name': 'Web Designing',
                    'description': 'Master modern web design principles, UX/UI, and frontend technologies. Create responsive and beautiful websites.',
                    'instructor_name': 'Mr. Hassan Raza',
                    'instructor_contact': '03003234503',
                    'fee': 20000,
                    'seats': 25
                },
                {
                    'name': 'Graphic Designing',
                    'description': 'Professional graphic design course covering Adobe Creative Suite, branding, and visual communication.',
                    'instructor_name': 'Ms. Zainab Ahmed',
                    'instructor_contact': '03004234504',
                    'fee': 19000,
                    'seats': 28
                },
                {
                    'name': 'Artificial Intelligence',
                    'description': 'Comprehensive AI course covering machine learning, deep learning, and practical AI applications.',
                    'instructor_name': 'Dr. Ahmed Hassan',
                    'instructor_contact': '03005234505',
                    'fee': 25000,
                    'seats': 20
                },
                {
                    'name': 'Digital Marketing',
                    'description': 'Learn digital marketing strategies, SEO, social media marketing, and analytics for online business growth.',
                    'instructor_name': 'Mr. Bilal Khan',
                    'instructor_contact': '03006234506',
                    'fee': 15000,
                    'seats': 32
                },
                {
                    'name': 'E-Commerce',
                    'description': 'Complete e-commerce course including platform setup, payment gateways, inventory management, and sales optimization.',
                    'instructor_name': 'Ms. Fatima Ali',
                    'instructor_contact': '03007234507',
                    'fee': 17000,
                    'seats': 30
                },
                {
                    'name': 'Basics of Computer',
                    'description': 'Introductory course covering computer fundamentals, operating systems, MS Office, and internet basics.',
                    'instructor_name': 'Mr. Imran Khan',
                    'instructor_contact': '03008234508',
                    'fee': 8000,
                    'seats': 50
                },
            ]
            for course_data in courses_data:
                course = Course(
                    name=course_data['name'],
                    description=course_data['description'],
                    instructor_name=course_data['instructor_name'],
                    instructor_contact=course_data['instructor_contact'],
                    fee=course_data['fee'],
                    seats=course_data['seats']
                )
                db.session.add(course)
            db.session.commit()
            print(f'✓ {len(courses_data)} courses created with instructors')
        
        # Create sample students if not exist
        if Student.query.count() == 0:
            students_data = [
                ('Ali', 'Khan', 'M', 'day_scholar', '12345-1234567-1', 'Regular'),
                ('Fatima', 'Ahmed', 'F', 'hostel', '12345-1234568-5', 'Regular'),
                ('Hassan', 'Ali', 'M', 'day_scholar', '12345-1234569-3', 'Needy'),
                ('Ayesha', 'Hassan', 'F', 'day_scholar', '12345-1234570-0', 'Regular'),
                ('Muhammad', 'Farooq', 'M', 'hostel', '12345-1234571-8', 'Orphan'),
                ('Zainab', 'Malik', 'F', 'day_scholar', '12345-1234572-6', 'Sponsored'),
                ('Ahmed', 'Raza', 'M', 'hostel', '12345-1234573-4', 'Staff Child'),
                ('Hira', 'Khan', 'F', 'hostel', '12345-1234574-2', 'Regular'),
                ('Omar', 'Sheikh', 'M', 'day_scholar', '12345-1234575-0', 'Regular'),
                ('Nida', 'Saeed', 'F', 'day_scholar', '12345-1234576-8', 'Regular'),
                ('Bilal', 'Ahmed', 'M', 'hostel', '12345-1234577-6', 'Needy'),
                ('Rabia', 'Iqbal', 'F', 'day_scholar', '12345-1234578-4', 'Regular'),
                ('Imran', 'Hassan', 'M', 'day_scholar', '12345-1234579-2', 'Regular'),
                ('Maryam', 'Aziz', 'F', 'hostel', '12345-1234580-0', 'Regular'),
                ('Samir', 'Hussain', 'M', 'hostel', '12345-1234581-8', 'Orphan'),
                ('Leila', 'Ahmed', 'F', 'day_scholar', '12345-1234582-6', 'Regular'),
            ]
            for first, last, gender, adm_type, cnic, category in students_data:
                student = Student(
                    first_name=first, 
                    last_name=last, 
                    gender=gender, 
                    date_of_birth=date(2003, 5, 15), 
                    phone='03001234567', 
                    address='123 Main Street, Karachi', 
                    city='Karachi', 
                    category=category, 
                    admission_type=adm_type, 
                    cnic=cnic, 
                    blood_group='O+', 
                    nationality='Pakistani', 
                    permanent_address='456 Permanent Street', 
                    guardian_name='Father', 
                    guardian_cnic='98765-9876543-1', 
                    last_qualification='Matriculation', 
                    current_qualification='Intermediate', 
                    status='active'
                )
                db.session.add(student)
                db.session.flush()
                student.generate_registration_number()
            
            db.session.commit()
            print(f'✓ {len(students_data)} students created with registration numbers')
            
            # Create enrollments
            all_courses = Course.query.all()
            students = Student.query.all()
            enrollment_count = 0
            for student in students:
                num_courses = random.randint(2, 3)
                selected_courses = random.sample(all_courses, num_courses)
                for course in selected_courses:
                    if course.student_count < course.seats:
                        db.session.add(Enrollment(student_id=student.id, course_id=course.id))
                        enrollment_count += 1
            
            db.session.commit()
            print(f'✓ {enrollment_count} enrollments created')
        
        # Print summary
        print('\n' + '='*50)
        print('DATABASE SUMMARY')
        print('='*50)
        print(f'Students: {Student.query.count()}')
        print(f'Courses: {Course.query.count()}')
        print(f'Enrollments: {Enrollment.query.count()}')
        
        # Show first few registration numbers
        print('\nFirst 5 Students with Registration Numbers:')
        for student in Student.query.limit(5).all():
            print(f'  {student.full_name}: {student.registration_number}')
        print(f'  ... and {Student.query.count() - 5} more students')
        
        # Show current settings
        print('\nCurrent Settings:')
        prefix = Setting.get('reg_number_prefix')
        print(f'  Registration Prefix: {prefix}')
        print(f'  School Name: {Setting.get("school_name")}')

if __name__ == '__main__':
    seed_database()
