# Payment System Setup Guide

## Quick Start (5 Minutes)

### Step 1: Run Database Migrations
```bash
# From the project root directory:
flask db migrate -m "Add payment categories and extend payment model"
flask db upgrade
```

### Step 2: Seed Payment Categories
```bash
python seed_payment_categories.py
```

You should see output like:
```
✓ Added: Security Fee - Rs. 5000
✓ Added: Admission Fee - Rs. 3000
✓ Added: Monthly Fee - Rs. 15000
✓ Added: Lab Fee - Rs. 5000
✓ Added: Examination Fee - Rs. 2000
✓ Added: Library Fee - Rs. 1000

✓ Successfully seeded 6 payment categories!
```

### Step 3: Start the Application
```bash
python run.py
```

### Step 4: Access the Payment System
- Open browser to: `http://127.0.0.1:5000`
- Go to **Payments** menu or `/payments/`

---

## Main Payment System URLs

### Admin Features
- **Category Management**: `/payments/categories`
  - Create, edit, or delete payment categories
  - Set default amounts per category
  - Activate/deactivate categories

### Accountant Features (Primary)
- **Record Payment**: `/payments/record`
  - Record new student payments
  - Support partial payments and multiple payment methods
  
- **List Payments**: `/payments/`
  - View all payments with filtering
  - Filter by student and status
  - Paginated list (20 per page)

- **Edit Payment**: `/payments/<id>/edit`
  - Update payment details
  - Mark status changes
  
- **Payment Summary**: `/payments/summary`
  - View analytics and statistics
  - Category-wise breakdown
  - Date range filtering

### Everyone Can View
- **Student Dues**: `/payments/student/<id>/dues`
  - View student payment history
  - Print receipts
  
- **View Receipt**: `/payments/<id>/student-slip` (Student copy)
- **View Receipt**: `/payments/<id>/admin-slip` (Admin copy)

---

## Common Tasks

### Record a Student Payment

1. Click **"Record Payment"** button
2. Select student name
3. Select payment category (e.g., "Monthly Fee")
4. Enter **Amount Due**: 15000
5. Enter **Amount Paid**: 10000
6. Select **Status**: "Partial Paid"
7. Select **Payment Method**: "Cash"
8. Add optional notes
9. Click **"Record Payment"**
10. System shows payment details with balance: Rs. 5000

### Update Partial Payment

1. Go to the payment record
2. Click **"Edit"**
3. Update **Amount Paid** from 10000 to 15000
4. Change **Status** to "Paid"
5. Click **"Save"**
6. System recalculates balance to Rs. 0

### Print Payment Receipt

From the payment details view:
1. Click **"Student Slip"** - For student personal records
2. Or click **"Admin Slip"** - For administrative copy
3. Ctrl+P to print (or use print button)
4. Save as PDF for records

### View Student Dues

1. Go to Student profile
2. Click **"View Payment History"** (or navigate to `/payments/student/<id>/dues`)
3. See all payments for that student
4. See total amount due and outstanding balance
5. Print any receipt from here

### Create New Payment Category

1. Go to **Categories** (`/payments/categories`)
2. Click **"New Category"**
3. Enter category name (e.g., "Hostel Fee")
4. Enter default amount (e.g., 8000)
5. Select status (Active/Inactive)
6. Click **"Save Category"**
7. Now available in payment recording form

---

## Payment Status Explanation

| Status | Meaning | When to Use |
|--------|---------|------------|
| **Paid** | Full amount received | Payment complete |
| **Pending** | No payment received | Dues outstanding |
| **Partial Paid** | Some amount received | Installment or partial payment |

**Example Flow:**
- Initial: Amount Due = 5000, Amount Paid = 0, Status = "Pending"
- After 1st payment: Amount Due = 5000, Amount Paid = 3000, Status = "Partial Paid"
- After 2nd payment: Amount Due = 5000, Amount Paid = 5000, Status = "Paid"

---

## Payment Methods Supported

- **Cash**: Direct cash payment
- **Cheque**: Include cheque number in "Reference No"
- **Bank Transfer**: Include transaction ID in "Reference No"
- **Online**: Payment through online portal
- **Other**: Any other method

---

## Key Features to Explore

### 1. **Real-Time Balance Calculation**
When recording a payment, balance updates automatically as you type.

### 2. **Payment Summary Dashboard**
Shows:
- Total amount due/paid/pending
- Breakdown by payment status
- Breakdown by category
- Collection percentage

### 3. **Filtered Reporting**
Filter payments by:
- Student name
- Payment category
- Payment status
- Date range (for summary)

### 4. **Professional Receipts**
- School header with contact info
- Student/Admin details
- Payment breakdown table
- Print-ready formatting
- Digital record keeping

### 5. **Pagination**
- 20 records per page
- Fast loading even with many payments
- Easy navigation

---

## Troubleshooting

### Database Migration Issues
```bash
# Reset database (careful - deletes all data!)
rm instance/school_dev.db
flask db init
flask db migrate -m "Initial setup"
flask db upgrade

# Re-seed categories
python seed_payment_categories.py
```

### Categories Not Showing in Form
- Make sure categories are Active (not Inactive)
- Run `python seed_payment_categories.py` to create default categories
- Refresh the payment recording form

### Can't Delete Category
- Categories with payments cannot be deleted
- Only empty categories can be deleted
- This is a safety feature to prevent data loss

### Payment Shows Error When Recording
- Ensure all required fields are filled
- Student must be selected
- Category must be selected
- Amounts must be valid numbers
- Amount Paid should not exceed Amount Due

---

## Database Structure

### payment_categories table
```
id (primary key)
name (unique, indexed)
description
default_amount
is_active
created_at
updated_at
```

### payments table (extended)
```
id (primary key)
student_id (foreign key)
category_id (foreign key) [NEW]
course_id (foreign key)
amount_due [MODIFIED]
amount_paid [NEW]
status [MODIFIED - new values]
payment_date
method
reference_no
recorded_by_user_id (foreign key)
notes
created_at
updated_at
```

---

## Permission Matrix

| Feature | Admin | Accountant | Teacher | Student |
|---------|-------|-----------|---------|---------|
| Create Category | ✅ | ❌ | ❌ | ❌ |
| Edit Category | ✅ | ❌ | ❌ | ❌ |
| Delete Category | ✅ | ❌ | ❌ | ❌ |
| Record Payment | ✅ | ✅ | ❌ | ❌ |
| Edit Payment | ✅ | ✅ | ❌ | ❌ |
| Delete Payment | ✅ | ❌ | ❌ | ❌ |
| View Payments | ✅ | ✅ | ✅ | ❌ |
| View Summary | ✅ | ✅ | ✅ | ❌ |
| View Student Dues | ✅ | ✅ | ✅ | ❌ |
| Print Slip | ✅ | ✅ | ✅ | ❌ |

---

## Next Steps

1. ✅ Run migrations
2. ✅ Seed categories
3. ✅ Start application
4. ✅ Record a test payment
5. ✅ View payment summary
6. ✅ Print a receipt
7. 🚀 Use the system!

---

## Support & Tips

- **Always Print/Save** receipts for audit trail
- **Regular Backups** of the database
- **Review Summary** monthly to track collection
- **Use Notes** field for payment details
- **Track Dues** to send reminders to students

---

**For detailed documentation, see: PAYMENTS_SYSTEM_README.md**
