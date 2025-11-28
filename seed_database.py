"""
Database initialization and seed data script.
Run: python seed_database.py
"""

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

def seed_database():
    """Create database and add sample data"""
    from app import create_app
    from app.models import db, User, Student, Course, Enrollment, Attendance, Payment
    
    app = create_app('development')
    
    with app.app_context():
        # Drop all tables (careful - this deletes all data!)
        # db.drop_all()
        
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✅ Tables created")
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\nCreating sample users...")
            
            # Create admin
            admin = User(username='admin', email='admin@school.local', role='admin', is_active=True)
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create teacher
            teacher = User(username='teacher1', email='teacher@school.local', role='teacher', is_active=True)
            teacher.set_password('teacher123')
            db.session.add(teacher)
            
            # Create accountant
            accountant = User(username='accountant1', email='accountant@school.local', role='accountant', is_active=True)
            accountant.set_password('account123')
            db.session.add(accountant)
            
            db.session.commit()
            print("✅ Users created (admin, teacher1, accountant1)")
        
        # Check if courses exist
        courses_count = Course.query.count()
        if courses_count == 0:
            print("\nCreating sample courses...")
            
            courses_data = [
                ('English', 'English Language & Literature', 5000, 30),
                ('Mathematics', 'Mathematics & Algebra', 5000, 30),
                ('Science', 'Physics, Chemistry & Biology', 5500, 25),
                ('Social Studies', 'History & Geography', 4500, 30),
                ('Computer Science', 'CS & Programming', 6000, 25),
            ]
            
            courses = []
            for name, desc, fee, seats in courses_data:
                course = Course(name=name, description=desc, fee=fee, seats=seats)
                db.session.add(course)
                courses.append(course)
            
            db.session.commit()
            print(f"✅ {len(courses)} courses created")
        
        # Check if students exist
        students_count = Student.query.count()
        if students_count == 0:
            print("\nCreating sample students...")
            
            students_data = [
                ('Ali', 'Khan', 'M', 'day_scholar', '2010-01-15', 'regular'),
                ('Fatima', 'Ahmed', 'F', 'day_scholar', '2010-03-22', 'needy'),
                ('Hassan', 'Ali', 'M', 'hostel', '2009-11-10', 'regular'),
                ('Ayesha', 'Khan', 'F', 'hostel', '2010-05-18', 'orphan'),
                ('Muhammad', 'Hassan', 'M', 'day_scholar', '2010-02-28', 'sponsored'),
                ('Zainab', 'Ibrahim', 'F', 'day_scholar', '2010-04-05', 'staff_child'),
                ('Ahmed', 'Malik', 'M', 'hostel', '2009-12-20', 'regular'),
                ('Hina', 'Siddiqui', 'F', 'day_scholar', '2010-06-12', 'regular'),
            ]
            
            students = []
            today = datetime.now().date()
            
            for fname, lname, gender, adm_type, dob_str, category in students_data:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                student = Student(
                    first_name=fname,
                    last_name=lname,
                    gender=gender,
                    admission_type=adm_type,
                    date_of_birth=dob,
                    admission_date=today - timedelta(days=30),  # Admitted 30 days ago
                    phone='03001234567',
                    address='123 Main Street',
                    city='Lahore',
                    category=category,
                    status='active'
                )
                db.session.add(student)
                students.append(student)
            
            db.session.commit()
            print(f"✅ {len(students)} students created")
            
            # Enroll students in courses
            print("\nCreating enrollments...")
            courses = Course.query.all()
            for student in students:
                # Enroll each student in 2-3 random courses
                import random
                selected_courses = random.sample(courses, random.randint(2, 3))
                for course in selected_courses:
                    enrollment = Enrollment(student_id=student.id, course_id=course.id)
                    db.session.add(enrollment)
            
            db.session.commit()
            print(f"✅ Enrollments created")
            
            # Add sample attendance
            print("\nCreating attendance records...")
            teacher_user = User.query.filter_by(role='teacher').first()
            if teacher_user:
                for student in students[:4]:  # First 4 students
                    for enrollment in student.enrollments.all():
                        # Mark attendance for last 5 days
                        for i in range(5):
                            date = today - timedelta(days=i)
                            status = random.choice(['present', 'present', 'present', 'absent', 'leave'])
                            try:
                                attendance = Attendance(
                                    student_id=student.id,
                                    course_id=enrollment.course_id,
                                    date=date,
                                    status=status,
                                    marked_by_user_id=teacher_user.id
                                )
                                db.session.add(attendance)
                            except:
                                pass  # Skip duplicate records
                
                db.session.commit()
                print(f"✅ Attendance records created")
            
            # Add sample payments
            print("\nCreating payment records...")
            accountant_user = User.query.filter_by(role='accountant').first()
            if accountant_user:
                for student in students[:3]:  # First 3 students paid
                    courses_enrolled = student.enrollments.all()
                    if courses_enrolled:
                        course = courses_enrolled[0].course
                        payment = Payment(
                            student_id=student.id,
                            course_id=course.id,
                            amount=course.fee * 0.5,  # Half payment
                            payment_date=today - timedelta(days=5),
                            method='cash',
                            reference_no=f'REF-{student.id}-001',
                            recorded_by_user_id=accountant_user.id,
                            notes='First installment'
                        )
                        db.session.add(payment)
                
                db.session.commit()
                print(f"✅ Payment records created")
        
        print("\n" + "="*50)
        print("Database seeding complete!")
        print("="*50)
        print("\nSample accounts created:")
        print("  Admin:      username=admin, password=admin123")
        print("  Teacher:    username=teacher1, password=teacher123")
        print("  Accountant: username=accountant1, password=account123")
        print("\nDatabase statistics:")
        print(f"  Users:       {User.query.count()}")
        print(f"  Students:    {Student.query.count()}")
        print(f"  Courses:     {Course.query.count()}")
        print(f"  Enrollments: {Enrollment.query.count()}")
        print(f"  Attendance:  {Attendance.query.count()}")
        print(f"  Payments:    {Payment.query.count()}")


if __name__ == '__main__':
    import random
    seed_database()
