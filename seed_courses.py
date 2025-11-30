"""
Seed script to add ACCDT CMS specific courses.
Run: python seed_courses.py
"""

import os
from app import create_app
from app.models import db, Course

app = create_app(os.environ.get('FLASK_ENV', 'development'))

courses_data = [
    {
        'name': 'Fashion Designing',
        'description': 'Learn the art and science of fashion design, garment construction, and fashion sketching.',
        'fee': 15000.00,
        'seats': 30
    },
    {
        'name': 'Tailoring',
        'description': 'Master the techniques of tailoring, cutting, and stitching to create custom garments.',
        'fee': 10000.00,
        'seats': 35
    },
    {
        'name': 'Web Designing',
        'description': 'Create beautiful and responsive websites using HTML, CSS, and modern design principles.',
        'fee': 12000.00,
        'seats': 25
    },
    {
        'name': 'Graphic Designing',
        'description': 'Master visual communication and design using professional tools and techniques.',
        'fee': 12000.00,
        'seats': 25
    },
    {
        'name': 'Artificial Intelligence',
        'description': 'Explore AI concepts, machine learning, and practical AI applications.',
        'fee': 18000.00,
        'seats': 20
    },
    {
        'name': 'Digital Marketing',
        'description': 'Learn social media marketing, SEO, content marketing, and digital advertising.',
        'fee': 13000.00,
        'seats': 28
    },
    {
        'name': 'E-Commerce',
        'description': 'Build and manage online stores, e-commerce platforms, and digital businesses.',
        'fee': 14000.00,
        'seats': 25
    },
    {
        'name': 'Basics of Computer',
        'description': 'Fundamental computer skills including MS Office, internet, and basic troubleshooting.',
        'fee': 5000.00,
        'seats': 40
    }
]

with app.app_context():
    # Check if courses already exist
    existing_count = Course.query.count()
    
    if existing_count == 0:
        print("🎓 Adding ACCDT CMS courses...")
        
        for course_data in courses_data:
            course = Course(**course_data)
            db.session.add(course)
            print(f"✓ Added: {course.name}")
        
        db.session.commit()
        print(f"\n✅ Successfully added {len(courses_data)} courses!")
    else:
        print(f"⚠️  Courses already exist in database ({existing_count} courses found).")
        print("Skipping seed operation.")
        
        # Display existing courses
        courses = Course.query.all()
        print("\nExisting courses:")
        for course in courses:
            print(f"  - {course.name} (Fee: Rs. {course.fee}, Seats: {course.seats})")
