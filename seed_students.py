"""
Seed script to add sample students for testing ACCDT CMS dashboard.
Run: python seed_students.py
"""

import os
from datetime import datetime, timedelta
from app import create_app
from app.models import db, Student, Enrollment

app = create_app(os.environ.get('FLASK_ENV', 'development'))

# Sample students data
students_data = [
    # Day Scholars - Male
    {'first_name': 'Ahmed', 'last_name': 'Khan', 'gender': 'M', 'admission_type': 'day_scholar', 'category': 'regular', 'city': 'Karachi'},
    {'first_name': 'Hassan', 'last_name': 'Ali', 'gender': 'M', 'admission_type': 'day_scholar', 'category': 'regular', 'city': 'Lahore'},
    {'first_name': 'Muhammad', 'last_name': 'Usman', 'gender': 'M', 'admission_type': 'day_scholar', 'category': 'sponsored', 'city': 'Islamabad'},
    {'first_name': 'Faisal', 'last_name': 'Malik', 'gender': 'M', 'admission_type': 'day_scholar', 'category': 'needy', 'city': 'Rawalpindi'},
    {'first_name': 'Bilal', 'last_name': 'Ahmed', 'gender': 'M', 'admission_type': 'day_scholar', 'category': 'staff_child', 'city': 'Multan'},
    
    # Day Scholars - Female
    {'first_name': 'Fatima', 'last_name': 'Khan', 'gender': 'F', 'admission_type': 'day_scholar', 'category': 'regular', 'city': 'Karachi'},
    {'first_name': 'Ayesha', 'last_name': 'Ali', 'gender': 'F', 'admission_type': 'day_scholar', 'category': 'regular', 'city': 'Lahore'},
    {'first_name': 'Zainab', 'last_name': 'Hassan', 'gender': 'F', 'admission_type': 'day_scholar', 'category': 'orphan', 'city': 'Islamabad'},
    {'first_name': 'Hira', 'last_name': 'Malik', 'gender': 'F', 'admission_type': 'day_scholar', 'category': 'needy', 'city': 'Peshawar'},
    
    # Hostel Students - Male
    {'first_name': 'Ali', 'last_name': 'Hussain', 'gender': 'M', 'admission_type': 'hostel', 'category': 'regular', 'city': 'Quetta'},
    {'first_name': 'Saad', 'last_name': 'Sheikh', 'gender': 'M', 'admission_type': 'hostel', 'category': 'regular', 'city': 'Gilgit'},
    {'first_name': 'Tariq', 'last_name': 'Ahmad', 'gender': 'M', 'admission_type': 'hostel', 'category': 'sponsored', 'city': 'Hunza'},
    {'first_name': 'Kamran', 'last_name': 'Haider', 'gender': 'M', 'admission_type': 'hostel', 'category': 'orphan', 'city': 'Muzaffarabad'},
    
    # Hostel Students - Female
    {'first_name': 'Maryam', 'last_name': 'Fahad', 'gender': 'F', 'admission_type': 'hostel', 'category': 'regular', 'city': 'Quetta'},
    {'first_name': 'Rani', 'last_name': 'Khan', 'gender': 'F', 'admission_type': 'hostel', 'category': 'needy', 'city': 'Peshawar'},
    {'first_name': 'Nida', 'last_name': 'Ahmed', 'gender': 'F', 'admission_type': 'hostel', 'category': 'sponsored', 'city': 'Gilgit'},
]

with app.app_context():
    from app.models import Course
    
    print("🎓 Adding sample students...")
    
    for student_data in students_data:
        student = Student(**student_data)
        db.session.add(student)
        print(f"✓ Added: {student_data['first_name']} {student_data['last_name']} ({student_data['gender']}, {student_data['admission_type']})")
    
    db.session.commit()
    
    # Enroll students in random courses
    print("\n📚 Enrolling students in courses...")
    
    students = Student.query.all()
    courses = Course.query.all()
    
    import random
    random.seed(42)  # For reproducibility
    
    for student in students:
        # Each student enrolls in 2-4 courses
        num_courses = random.randint(2, 4)
        selected_courses = random.sample(courses, min(num_courses, len(courses)))
        
        for course in selected_courses:
            # Check if already enrolled
            existing = Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first()
            if not existing:
                enrollment = Enrollment(student_id=student.id, course_id=course.id)
                db.session.add(enrollment)
                print(f"  → {student.full_name} enrolled in {course.name}")
    
    db.session.commit()
    
    print(f"\n✅ Successfully added {len(students_data)} students and created enrollments!")
    
    # Print summary
    print("\n📊 Database Summary:")
    print(f"  Total Students: {Student.query.count()}")
    print(f"  Day Scholars: {Student.query.filter_by(admission_type='day_scholar').count()}")
    print(f"  Hostel Students: {Student.query.filter_by(admission_type='hostel').count()}")
    print(f"  Male: {Student.query.filter_by(gender='M').count()}")
    print(f"  Female: {Student.query.filter_by(gender='F').count()}")
    print(f"  Total Courses: {Course.query.count()}")
    print(f"  Total Enrollments: {Enrollment.query.count()}")
