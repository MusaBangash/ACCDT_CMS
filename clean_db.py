"""
Clean database script - deletes all data except admin user
"""

from app import create_app, db
from app.models import User, Student, Course, Enrollment, Attendance, Payment, PaymentCategory, Setting

app = create_app('development')

with app.app_context():
    print("=" * 60)
    print("CLEANING DATABASE - KEEPING ONLY ADMIN USER")
    print("=" * 60)
    
    try:
        # Delete all data
        print("\nDeleting all Payment records...")
        Payment.query.delete()
        db.session.commit()
        print("✓ Payments deleted")
        
        print("Deleting all Attendance records...")
        Attendance.query.delete()
        db.session.commit()
        print("✓ Attendance deleted")
        
        print("Deleting all Enrollment records...")
        Enrollment.query.delete()
        db.session.commit()
        print("✓ Enrollments deleted")
        
        print("Deleting all Course records...")
        Course.query.delete()
        db.session.commit()
        print("✓ Courses deleted")
        
        print("Deleting all PaymentCategory records...")
        PaymentCategory.query.delete()
        db.session.commit()
        print("✓ Payment Categories deleted")
        
        print("Deleting all Student records...")
        Student.query.delete()
        db.session.commit()
        print("✓ Students deleted")
        
        # Keep only admin user, delete other users
        print("Deleting non-admin users...")
        non_admin_users = User.query.filter(User.username != 'admin').delete()
        db.session.commit()
        print(f"✓ {non_admin_users} non-admin users deleted")
        
        # Verify admin exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"\n✓ Admin user retained: {admin.username} ({admin.role})")
        else:
            print("\n⚠ Admin user not found! Creating admin user...")
            admin = User(
                username='admin',
                email='admin@accdt.edu.pk',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created: admin / admin123")
        
        # Verify settings are preserved
        settings_count = Setting.query.count()
        print(f"✓ System settings preserved: {settings_count} records")
        
        print("\n" + "=" * 60)
        print("DATABASE CLEANUP COMPLETE")
        print("=" * 60)
        print("\nAdmin Login:")
        print("  Username: admin")
        print("  Password: admin123")
        print("  Role: Admin")
        print("\nDatabase is now clean and ready for new data upload!")
        print("=" * 60)
        
    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error during cleanup: {str(e)}")
        import traceback
        traceback.print_exc()
