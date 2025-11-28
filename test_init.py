"""
Test script to verify the Flask application initializes correctly.
Run: python test_init.py
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

def test_app_creation():
    """Test that app can be created without errors"""
    try:
        from app import create_app
        app = create_app('testing')
        print("✅ App creation successful")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_models():
    """Test that models can be imported"""
    try:
        from app.models import db, User, Student, Course, Enrollment, Attendance, Payment
        print("✅ All models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_blueprints():
    """Test that all blueprints can be imported"""
    try:
        from app.routes.auth import auth_bp
        from app.routes.dashboard import dashboard_bp
        from app.routes.students import students_bp
        from app.routes.courses import courses_bp
        from app.routes.attendance import attendance_bp
        from app.routes.payments import payments_bp
        from app.routes.admin import admin_bp
        print("✅ All blueprints imported successfully")
        return True
    except Exception as e:
        print(f"❌ Blueprint import failed: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        from app import create_app
        from app.models import db, User
        
        app = create_app('testing')
        with app.app_context():
            # Create tables
            db.create_all()
            
            # Try to query
            user_count = User.query.count()
            print(f"✅ Database connection successful (Users: {user_count})")
            return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    print("=" * 50)
    print("School Management System - Initialization Tests")
    print("=" * 50)
    print()
    
    tests = [
        ("App Creation", test_app_creation),
        ("Models", test_models),
        ("Blueprints", test_blueprints),
        ("Database", test_database),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        results.append(test_func())
        print()
    
    print("=" * 50)
    if all(results):
        print("✅ ALL TESTS PASSED - App is ready to run!")
        print()
        print("Start the app with:")
        print("  python run.py")
        print()
        print("Then visit: http://localhost:5000")
    else:
        print("❌ Some tests failed - check errors above")
    print("=" * 50)

if __name__ == '__main__':
    main()
