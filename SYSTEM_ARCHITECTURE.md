# Payment Management System - Architecture & Flow

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PAYMENT MANAGEMENT SYSTEM                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              USER INTERFACE (Templates)              │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │  Management Layer:         Printing Layer:          │   │
│  │  ┌─────────────────┐      ┌──────────────────┐      │   │
│  │  │ payments.html   │      │ student_slip.html│      │   │
│  │  │ payment_form    │      │ admin_slip.html  │      │   │
│  │  │ payment_detail  │      └──────────────────┘      │   │
│  │  │ payment_categ...│                                 │   │
│  │  │ student_dues    │      Reporting Layer:           │   │
│  │  │ payment_category│      ┌──────────────────┐      │   │
│  │  │ _form.html      │      │ payment_summary  │      │   │
│  │  └─────────────────┘      └──────────────────┘      │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ▲                                   │
│                           │                                   │
│  ┌────────────────────────┴──────────────────────────────┐   │
│  │          ROUTES / BUSINESS LOGIC LAYER               │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │  Category Routes:      Payment Routes:              │   │
│  │  • list_categories()   • list_payments()            │   │
│  │  • create_category()   • record_payment()           │   │
│  │  • edit_category()     • view_payment()             │   │
│  │  • delete_category()   • edit_payment()             │   │
│  │                        • mark_payment_status()      │   │
│  │                        • delete_payment()           │   │
│  │                                                      │   │
│  │  Receipt Routes:       Summary Routes:              │   │
│  │  • student_slip()      • payment_summary()          │   │
│  │  • admin_slip()        • student_dues()             │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ▲                                   │
│                           │                                   │
│  ┌────────────────────────┴──────────────────────────────┐   │
│  │              FORMS VALIDATION LAYER                   │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │  PaymentCategoryForm:     PaymentForm:              │   │
│  │  • name                   • student                 │   │
│  │  • description            • category                │   │
│  │  • default_amount         • course                  │   │
│  │  • is_active              • amount_due              │   │
│  │                           • amount_paid             │   │
│  │                           • status                  │   │
│  │                           • method                  │   │
│  │                           • reference_no            │   │
│  │                           • notes                   │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ▲                                   │
│                           │                                   │
│  ┌────────────────────────┴──────────────────────────────┐   │
│  │            ORM MODELS & DATABASE LAYER               │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │  PaymentCategory Model:    Payment Model:           │   │
│  │  ┌──────────────────┐      ┌──────────────────┐    │   │
│  │  │ id               │      │ id               │    │   │
│  │  │ name (unique)    │      │ student_id (FK)  │    │   │
│  │  │ description      │      │ category_id (FK) │    │   │
│  │  │ default_amount   │      │ course_id (FK)   │    │   │
│  │  │ is_active        │      │ amount_due       │    │   │
│  │  │ created_at       │      │ amount_paid      │    │   │
│  │  │ updated_at       │      │ status           │    │   │
│  │  │ (1:M relation)   │      │ payment_date     │    │   │
│  │  └──────────────────┘      │ method           │    │   │
│  │         │                   │ reference_no     │    │   │
│  │         │                   │ recorded_by_user_id   │    │
│  │         │                   │ notes            │    │   │
│  │         │                   │ created_at       │    │   │
│  │         │                   │ updated_at       │    │   │
│  │         │                   │                  │    │   │
│  │         │                   │ Properties:      │    │   │
│  │         │                   │ • amount_due_...│    │   │
│  │         │                   │ • percentage_...│    │   │
│  │         └─────────────────→ └──────────────────┘    │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ▲                                   │
│                           │                                   │
│  ┌────────────────────────┴──────────────────────────────┐   │
│  │          DATABASE (SQLite + SQLAlchemy)              │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │  Tables:                                            │   │
│  │  • payment_categories                               │   │
│  │  • payments (extended)                              │   │
│  │  • students (foreign key)                           │   │
│  │  • courses (foreign key)                            │   │
│  │  • users (for recorded_by)                          │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagrams

### 1. Recording a Payment Flow

```
User (Accountant)
    │
    ├─→ Click "Record Payment"
    │
    ├─→ GET /payments/record
    │       │
    │       ├─→ routes.py: record_payment() [GET]
    │       │       │
    │       │       ├─→ Populate form choices:
    │       │       │   • Students from DB
    │       │       │   • Categories from DB
    │       │       │   • Courses from DB
    │       │       │
    │       │       └─→ Render: payment_form.html
    │       │
    │       └─→ Display form to user
    │
    ├─→ User fills form:
    │   • Student: Ahmed Ali
    │   • Category: Monthly Fee
    │   • Amount Due: 15,000
    │   • Amount Paid: 10,000
    │   • Status: Partial Paid
    │   • Method: Cash
    │
    ├─→ User clicks "Record Payment"
    │
    ├─→ POST /payments/record
    │       │
    │       ├─→ routes.py: record_payment() [POST]
    │       │       │
    │       │       ├─→ PaymentForm validates:
    │       │       │   ✓ All required fields
    │       │       │   ✓ Valid student
    │       │       │   ✓ Valid category
    │       │       │   ✓ Positive amounts
    │       │       │
    │       │       ├─→ Create Payment object:
    │       │       │   {
    │       │       │     student_id: 1,
    │       │       │     category_id: 3,
    │       │       │     amount_due: 15000,
    │       │       │     amount_paid: 10000,
    │       │       │     status: 'partial_paid',
    │       │       │     payment_date: today,
    │       │       │     method: 'cash',
    │       │       │     recorded_by_user_id: current_user.id
    │       │       │   }
    │       │       │
    │       │       ├─→ db.session.add(payment)
    │       │       ├─→ db.session.commit()
    │       │       │
    │       │       └─→ Redirect to view_payment(payment.id)
    │       │
    │       └─→ Flash: "Payment recorded successfully!"
    │
    └─→ Display payment_detail.html
            │
            ├─→ Show all payment details
            ├─→ Show balance: Rs. 5,000
            ├─→ Show percentage: 66.7%
            └─→ Offer print options

```

### 2. Updating Partial Payment to Full Payment

```
User views payment where:
  amount_due: 15,000
  amount_paid: 10,000
  status: partial_paid

    │
    ├─→ Click "Edit"
    │
    ├─→ GET /payments/<id>/edit
    │       └─→ Display form with current values
    │
    ├─→ User updates:
    │   amount_paid: 10,000 → 15,000
    │   status: partial_paid → paid
    │
    ├─→ POST /payments/<id>/edit
    │       │
    │       └─→ Update database:
    │           payment.amount_paid = 15000
    │           payment.status = 'paid'
    │           db.session.commit()
    │
    └─→ View updated payment:
        amount_due: 15,000
        amount_paid: 15,000
        status: paid
        remaining_balance: 0
        percentage_paid: 100%
```

### 3. Viewing Payment Summary

```
User
    │
    ├─→ Click "Summary"
    │
    ├─→ GET /payments/summary
    │       │
    │       ├─→ routes.py: payment_summary()
    │       │       │
    │       │       ├─→ Query all payments:
    │       │       │   Payment.query.all()
    │       │       │
    │       │       ├─→ Calculate statistics:
    │       │       │   • total_due = sum(p.amount_due)
    │       │       │   • total_paid = sum(p.amount_paid)
    │       │       │   • total_pending = total_due - total_paid
    │       │       │
    │       │       ├─→ Group by status:
    │       │       │   • paid: count
    │       │       │   • pending: count
    │       │       │   • partial_paid: count
    │       │       │
    │       │       ├─→ Group by category:
    │       │       │   • For each category:
    │       │       │     - category.due
    │       │       │     - category.paid
    │       │       │     - category.collection%
    │       │       │
    │       │       └─→ Render: payment_summary.html
    │       │
    │       └─→ Pass data to template
    │
    └─→ Display analytics dashboard:
        • Statistics cards
        • Status distribution
        • Category breakdown
        • Recent payments
```

### 4. Printing Receipt Flow

```
User views payment
    │
    ├─→ Click "Student Slip"
    │
    ├─→ GET /payments/<id>/student-slip
    │       │
    │       ├─→ routes.py: student_slip()
    │       │       │
    │       │       ├─→ Query payment from DB
    │       │       │
    │       │       └─→ Render: payment_student_slip.html
    │       │           (with receipt data)
    │       │
    │       └─→ Display print-optimized receipt
    │
    └─→ User:
        • Reviews receipt
        • Presses Ctrl+P or clicks Print
        • Saves as PDF or prints to paper
```

---

## 🔄 Database Relationships

```
PaymentCategory (1)
    │
    └──────────── (M) Payment
                      │
                      ├─── Student (many-to-one)
                      ├─── Course (many-to-one, optional)
                      └─── User (recorded_by - many-to-one)
```

---

## 📈 Data Processing Pipeline

```
RAW INPUT (Form)
    │
    ├─→ WTF Form Validation
    │       • Check required fields
    │       • Validate data types
    │       • Check business rules
    │
    ├─→ MODEL LAYER
    │       • Create Payment object
    │       • Calculate properties:
    │         - amount_due_remaining
    │         - percentage_paid
    │       • Enforce constraints
    │
    ├─→ DATABASE LAYER
    │       • Add to session
    │       • Commit transaction
    │       • Store in SQLite
    │
    ├─→ QUERY LAYER
    │       • Retrieve from database
    │       • Apply filters
    │       • Calculate statistics
    │
    └─→ PRESENTATION LAYER
            • Format for display
            • Apply business logic in templates
            • Render HTML with data
            • Apply CSS styling
```

---

## 🎨 Template Hierarchy

```
base.html (Bootstrap 5 layout)
    │
    ├─→ payments.html
    │       ├─ Header (navigation)
    │       ├─ Statistics cards (CSS)
    │       ├─ Filter form
    │       └─ Data table (with pagination)
    │
    ├─→ payment_form.html
    │       ├─ Card header
    │       ├─ Form fields
    │       │   └─ JavaScript for balance calc
    │       └─ Submit buttons
    │
    ├─→ payment_detail.html
    │       ├─ Multiple cards
    │       ├─ Progress bars
    │       └─ Action buttons
    │
    ├─→ payment_student_slip.html
    │       ├─ Print header
    │       ├─ Receipt content
    │       ├─ Print CSS media queries
    │       └─ Print buttons (no-print)
    │
    ├─→ payment_admin_slip.html
    │       ├─ Similar to student slip
    │       ├─ Admin-specific sections
    │       └─ Administrative details
    │
    ├─→ payment_summary.html
    │       ├─ Statistics cards
    │       ├─ Filter controls
    │       ├─ Data tables
    │       └─ Charts/Progress bars
    │
    ├─→ payment_categories.html
    │       ├─ Categories table
    │       └─ CRUD action buttons
    │
    ├─→ payment_category_form.html
    │       ├─ Form fields
    │       └─ Example reference
    │
    └─→ student_dues.html
            ├─ Student summary
            ├─ Dues cards
            ├─ Payment history
            └─ Action buttons
```

---

## 🔐 Security & Access Control

```
Request
    │
    ├─→ Authentication Check
    │       @login_required
    │
    ├─→ Authorization Check
    │       @admin_required      (for category management)
    │       @accountant_required (for payment recording)
    │       (anyone for viewing)
    │
    ├─→ Validation
    │       • Form validation
    │       • Business logic validation
    │       • Database constraints
    │
    └─→ Process
            • Access granted
            • Operation executed
            • Results returned
```

---

## 📊 Status Transition Diagram

```
PAYMENT LIFECYCLE:

   Initial State
        │
        ├─→ status = 'pending'
        │   amount_paid = 0
        │
        ├─→ User makes payment
        │
        ├─→ IF amount_paid == amount_due:
        │   └─→ status = 'paid'
        │
        ├─→ ELSE IF 0 < amount_paid < amount_due:
        │   └─→ status = 'partial_paid'
        │
        ├─→ ELSE IF amount_paid == 0:
        │   └─→ status = 'pending'
        │
        ├─→ [User makes another payment]
        │   └─→ amount_paid increases
        │
        └─→ Final State
            status = 'paid'
            amount_paid = amount_due
            remaining_balance = 0
```

---

## 🔄 Request/Response Cycle

```
HTTP REQUEST
    │
    ├─→ Flask routing
    │   GET/POST /payments/...
    │
    ├─→ View function in routes.py
    │   • Authenticate user
    │   • Validate request
    │   • Query/modify database
    │   • Calculate data
    │
    ├─→ Template rendering
    │   • Pass context data
    │   • Apply Jinja2 templating
    │   • Generate HTML
    │
    └─→ HTTP RESPONSE
        • Status code (200, 302, 404, etc.)
        • HTML content or redirect
        • Headers (flash messages, etc.)
```

---

## 💾 Data Persistence

```
Memory (Application Runtime)
    │
    ├─→ Create/Modify objects
    │   payment = Payment(...)
    │
    ├─→ db.session.add(payment)
    │   (Add to transaction)
    │
    ├─→ db.session.commit()
    │   │
    │   └─→ Persist to SQLite
    │
    └─→ Database File
        school_dev.db
        └─→ Tables:
            • payment_categories
            • payments
```

---

## 📱 Client-Server Architecture

```
CLIENT (Browser)
    │
    ├─→ Submit HTML Form
    │   POST /payments/record
    │
    ├─→ Receive HTML Response
    │
    ├─→ Display rendered page
    │
    └─→ Execute JavaScript
        └─→ Real-time calculations
            (balance updates, etc.)

        ↕ (HTTP)

SERVER (Flask Application)
    │
    ├─→ Receive request
    │
    ├─→ Route to handler
    │
    ├─→ Query/Process database
    │
    ├─→ Render template
    │
    └─→ Send HTML response
```

---

## 🎯 Key Processing Points

### Point 1: Form Submission
```python
if form.validate_on_submit():
    # All validation passed
    # Safe to process
```

### Point 2: Database Transaction
```python
db.session.add(payment)
db.session.commit()
# Data persisted
```

### Point 3: Status Auto-Calculation
```python
if amount_paid == amount_due:
    status = 'paid'
elif 0 < amount_paid < amount_due:
    status = 'partial_paid'
else:
    status = 'pending'
```

### Point 4: Balance Calculation
```python
@property
def amount_due_remaining(self):
    return self.amount_due - self.amount_paid
```

---

This architecture ensures:
- ✅ Separation of concerns
- ✅ Data integrity
- ✅ Security
- ✅ Scalability
- ✅ Maintainability
- ✅ User experience
