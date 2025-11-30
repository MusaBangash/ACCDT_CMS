"""
Seed script for payment categories.
Run this after running migrations to populate payment categories.
"""

from app import create_app
from app.models import db, PaymentCategory

app = create_app('development')

def seed_payment_categories():
    """Seed default payment categories"""
    with app.app_context():
        # Check if categories already exist
        if PaymentCategory.query.count() > 0:
            print("Payment categories already exist. Skipping seed.")
            return
        
        categories = [
            {
                'name': 'Security Fee',
                'description': 'One-time security deposit for admission',
                'default_amount': 5000.00,
                'is_active': True
            },
            {
                'name': 'Admission Fee',
                'description': 'One-time admission processing fee',
                'default_amount': 3000.00,
                'is_active': True
            },
            {
                'name': 'Monthly Fee',
                'description': 'Recurring monthly tuition and classes fee',
                'default_amount': 15000.00,
                'is_active': True
            },
            {
                'name': 'Lab Fee',
                'description': 'Laboratory and practical course fee (per semester)',
                'default_amount': 5000.00,
                'is_active': True
            },
            {
                'name': 'Examination Fee',
                'description': 'Per semester or per exam examination fee',
                'default_amount': 2000.00,
                'is_active': True
            },
            {
                'name': 'Library Fee',
                'description': 'Annual library membership and access fee',
                'default_amount': 1000.00,
                'is_active': True
            }
        ]
        
        for cat_data in categories:
            category = PaymentCategory(**cat_data)
            db.session.add(category)
            print(f"✓ Added: {category.name} - Rs. {category.default_amount}")
        
        db.session.commit()
        print(f"\n✓ Successfully seeded {len(categories)} payment categories!")

if __name__ == '__main__':
    seed_payment_categories()
