# odoo-haluc-pontok

A Háluc-pont alapú jutalmazási és visszacsatolási rendszer célja, hogy motiválja a madrichokat a közösségi szerepvállalásra, a többletfeladatok önkéntes elvállalására, és megerősítse a mozgalmon belüli aktív, felelős jelenlétet. A „Háluc” (חלוץ) héber szó jelentése: úttörő – ezzel is kifejezve a madrichok példamutató szerepét.

## 🎯 Objective
To create an internal Odoo module for the Hasomer Hacair Jewish youth movement that tracks and manages Háluc Points — a non-monetary reward system for volunteer youth leaders (madrichim). Points are earned by taking on extra community tasks and can be spent on shared experiences, equipment, or reducing seminar participation costs.

This module will:
- Log all point transactions (additions and spending)
- Calculate current point balances per madrich
- Display points in the madrich’s profile
- Restrict editing access to coordinators (slihon)
- Support future features like group-based purchases (kupa) and dashboard reports

## ✨ Key Features
- **Point Transaction Tracking**: Each point movement (earning or spending) is logged as a separate entry.
- **Balance Computation**: Live calculation of available points for each madrich.
- **User Visibility**: Madrichim can view their point history and current balance.
- **Permission Control**: Only specific roles (coordinators/slihon) can enter or modify points.
- **Categorization and Filtering**: Administrators can filter transactions by task type, date, madrich, etc.
- **Portal View**: Madrichim can view their points and transaction history via the Odoo portal.

## 💾 Data Models

### 1. `haluc.point.transaction`
This model tracks all point movements, whether earned or spent.

| Field         | Type      | Required | Description                                     |
|---------------|-----------|----------|-------------------------------------------------|
| `name`        | Char      | ✔        | Description of the transaction                  |
| `partner_id`  | Many2one  | ✔        | Refers to the madrich (`res.partner`)           |
| `date`        | Date      | ✔        | Transaction date (defaults to today)            |
| `points`      | Integer   | ✔        | Positive for earning, negative for spending     |
| `category`    | Char      | ✖        | Activity type (e.g., School visit, Club purchase) |
| `notes`       | Text      | ✖        | Additional details                              |
| `state`       | Selection | ✔        | Transaction state: `\'draft\'` or `\'confirmed\'`   |

### 2. `res.partner` (Extension)
The standard `res.partner` model is extended to include a Háluc Points balance.

| Field                 | Type             | Description                                       |
|-----------------------|------------------|---------------------------------------------------|
| `haluc_point_balance` | Computed Integer | Live balance based on confirmed transactions      |

## 🛠️ Module Structure
The module `haluc_points` follows a standard Odoo module structure:

```
haluc_points/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── point_transaction.py  # Defines haluc.point.transaction
│   └── partner_extension.py  # Extends res.partner
├── views/
│   ├── point_transaction_views.xml # Views for transactions
│   ├── partner_views.xml         # Views for partner extension
│   └── portal_templates.xml      # Portal views for users
├── security/
│   ├── ir.model.access.csv     # Access control list
│   └── security.xml            # Security groups and rules
├── controllers/
│   ├── __init__.py
│   └── portal.py               # Controller for portal views
├── data/
│   └── demo_data.xml           # Optional: Sample data for testing
```

## 🚀 Extended Functionalities (Future Enhancements)

### 📬 1. Automatic Email Alerts
- **Notification System**: Send email alerts to madrichim upon confirmation of new points earned.
- **Customizable Templates**: Use email templates for consistent communication.

### 📊 2. User Dashboards & Statistics
- **Admin Dashboard**:
    - Top contributors
    - Points trends (monthly)
    - Total earned vs. spent
    - Most active categories
- **Madrich Portal Summary**:
    - Current balance
    - Last 5 transactions
    - Motivational status tag

### 🧙 3. Mass Point Addition Wizard
- **Efficient Data Entry**: Allow coordinators to add points for multiple madrichim simultaneously.
- **Streamlined Process**: Fields for partners, points, category, notes, date, and notification toggle.

## ⚙️ Installation
1. Add the `haluc_points` module to your Odoo addons path.
2. Navigate to **Apps** in Odoo.
3. Remove the "Apps" filter and search for `haluc_points`.
4. Click **Install**.

## 👤 User Roles and Access
- **Háluc User (`haluc_user`)**:
    - Can view their own point balance and transaction history (via portal and potentially within Odoo if granted read access to their `res.partner` record).
    - Cannot create or modify transactions.
- **Háluc Admin (`haluc_admin`)**:
    - Full access to create, read, update, and delete point transactions.
    - Can view all users\' point balances and histories.
    - Can manage categories and other administrative settings for the module.

The main menu "Háluc Points" is visible to both `haluc_user` and `haluc_admin`. The "Transactions" submenu under "Háluc Points > Transactions" is visible only to the `haluc_admin` group.

## ✅ TODO / Implementation Progress
The initial development followed this plan:

### 🔧 1. Base Module Setup
- [x] Create a new module named `haluc_points`
- [x] Initialize folder structure

### 📊 2. Data Model – `haluc.point.transaction`
- [x] Define `haluc.point.transaction` model with all fields
- [x] Use default values and selection states

### 👥 3. Extend `res.partner`
- [x] Inherit `res.partner` model
- [x] Add computed field `haluc_point_balance`

### 🧩 4. Views
- [x] Transaction Views (List, Form, Filters, Group by)
- [x] Partner Views (Show balance on form, add transaction history tab)
- [x] Menu Items (Community > Háluc Points > Transactions)

### 🔐 5. Access Control
- [x] Define `haluc_admin` (full access) and `haluc_user` (read-only for own) groups
- [x] Create access control entries in `ir.model.access.csv`

### 🌐 6. Portal View
- [x] Add frontend page for madrichim to view their points and transactions

### 📦 7. Sample Data for Testing
- [x] Create demo XML data (pending)

## 📄 License
This project is licensed under the [MIT License](LICENSE).
