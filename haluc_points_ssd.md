# 📄 Háluc Points System – Odoo Module Specification

## 🔖 Project Name
`haluc_points`

## 🎯 Objective
To create an internal Odoo module for the Hasomer Hacair Jewish youth movement that tracks and manages Háluc Points — a non-monetary reward system for volunteer youth leaders (madrichim). Points are earned by taking on extra community tasks and can be spent on shared experiences, equipment, or reducing seminar participation costs.

This module will:
- Log all point transactions (additions and spending)
- Calculate current point balances per madrich
- Display points in the madrich’s profile
- Restrict editing access to coordinators (slihon)
- Support future features like group-based purchases (kupa) and dashboard reports

## 🧩 Functional Components

| Feature                        | Description |
|-------------------------------|-------------|
| Point transaction tracking    | Each point movement is logged as a separate entry |
| Balance computation           | Live total of available points per madrich |
| User visibility               | Madrichim can view their point history and balance |
| Permission control            | Only specific roles can enter or modify points |
| Categorization and filtering  | Admins can filter by task type, date, madrich, etc. |

## 📌 Data Models

### 1. `haluc.point.transaction`
Tracks all point movements (earning or spending).

| Field           | Type      | Required | Description |
|----------------|-----------|----------|-------------|
| `name`         | Char      | ✔        | Description of the transaction |
| `partner_id`   | Many2one  | ✔        | Refers to the madrich (`res.partner`) |
| `date`         | Date      | ✔        | Transaction date |
| `points`       | Integer   | ✔        | Positive for earning, negative for spending |
| `category`     | Char      | ✖        | Activity type (e.g., School visit, Club purchase) |
| `notes`        | Text      | ✖        | Additional details |
| `state`        | Selection | ✔        | `'draft'` or `'confirmed'` |

### 2. `res.partner` extension
Adds a computed field `haluc_point_balance` to show the total points (sum of all confirmed transactions).

| Field               | Type               | Description |
|---------------------|--------------------|-------------|
| `haluc_point_balance` | Computed Integer | Live balance of confirmed transactions |

## ✅ TODO LIST – STEP-BY-STEP

### 🔧 1. Base Module Setup
- [x] Create a new module named `haluc_points`
- [x] Initialize folder structure: `models`, `views`, `security`, `data`, `__manifest__.py`, `__init__.py`

### 📊 2. Data Model – `haluc.point.transaction`
- [x] Define a new model `haluc.point.transaction`
- [x] Include all fields listed above with correct types and validations
- [x] Use default values where applicable (e.g., `date = fields.Date.today()`)
- [x] Add selection states (`draft`, `confirmed`)

### 👥 3. Extend `res.partner`
- [ ] Inherit `res.partner` model
- [ ] Add a computed field `haluc_point_balance`
- [ ] Compute method: sum of all confirmed transactions (`state = 'confirmed'`), where:
  - [ ] Positive `points` values are added to the total.
  - [ ] Negative `points` values are subtracted from the total.

### 🧩 4. Views – DETAILED

#### 4.1 Transaction Views (`haluc.point.transaction`)
- [ ] List view with columns: `name`, `partner_id`, `points`, `type`, `category`, `date`, `state`
- [ ] Filters: by partner, type, date range
- [ ] Group by: partner, category
- [ ] Form view: all fields shown, optional Confirm button, two tabs ("Details", "Notes")

#### 4.2 Partner Views (`res.partner`)
- [ ] Show `haluc_point_balance` on partner form
- [ ] Add one2many list tab for all related point transactions ("Háluc Points History")

#### 4.3 Menu Items
- [ ] Menu: **Community > Háluc Points > Transactions**
- [ ] Visible only to `haluc_admin` group

### 🔐 5. Access Control
- [ ] Group: `haluc_admin` – full access
- [ ] Group: `haluc_user` – read-only for own transactions
- [ ] Create access control entries in `ir.model.access.csv`

### 🌐 6. Portal View (optional)
- [ ] Add frontend page for madrichim to view their points and transactions

### 📦 7. Sample Data for Testing
- [ ] Create demo XML data with 2 madrichim, 5 sample transactions

## 📁 Suggested File Structure

```
haluc_points/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── point_transaction.py
│   └── partner_extension.py
├── views/
│   ├── point_transaction_views.xml
│   └── partner_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── data/
│   └── demo_data.xml
```

## 🔁 Extended Functionalities

### 📬 1. Automatic Email Alerts (via System Event)
- [ ] Add `notify` boolean field to `haluc.point.transaction` model.
- [ ] Create an automated action (or override `write` method of `haluc.point.transaction`) to detect confirmation of 'add' type transactions where `notify` is true.
- [ ] Create an email template (`mail.template`) for the notification.
  - [ ] Template should include: points earned, category, note, and new partner point balance.
- [ ] Implement logic to send the email to the partner associated with the transaction.

### 📊 2. User Dashboards & Statistics

#### Admin Dashboard
- [ ] Design the Admin Dashboard layout.
- [ ] Implement data retrieval for "Top contributors".
- [ ] Implement data retrieval for "Points trends (monthly)".
- [ ] Implement data retrieval for "Total earned vs spent".
- [ ] Implement data retrieval for "Most active categories".
- [ ] Create the view (e.g., using Odoo's dashboard or a custom view) to display this information.

#### Madrich Portal Summary
- [ ] Design the Madrich Portal Summary layout.
- [ ] Implement data retrieval for "Current balance" (reuse existing).
- [ ] Implement data retrieval for "Last 5 transactions".
- [ ] Implement data retrieval for "Upcoming point-earning events" (if applicable, may require new model/logic).
- [ ] Implement "Motivational status tag" (define logic for tags).
- [ ] Create the portal view to display this information.

### 🧙 3. Mass Point Addition Wizard

#### Transient Model: `haluc.point.mass.wizard`
- [ ] Define the `haluc.point.mass.wizard` transient model with all specified fields:
  - [ ] `partner_ids` (Many2many to `res.partner`)
  - [ ] `points` (Integer)
  - [ ] `category` (Char)
  - [ ] `notes` (Text)
  - [ ] `date` (Date, default today)
  - [ ] `notify` (Boolean)
  - [ ] `state` (Selection: `draft`, `confirmed`)
- [ ] Create the form view for the wizard.

#### Wizard Behavior
- [ ] Implement the wizard action/method to:
  - [ ] Loop through selected `partner_ids`.
  - [ ] Create a new `haluc.point.transaction` for each partner using the wizard's field values.
  - [ ] If `notify` is checked, trigger the email alert for each created transaction (reuse email alert functionality).
- [ ] Add an action menu item to open the wizard (e.g., from the `res.partner` tree view or a dedicated menu).

## ✅ Summary of Benefits

| Feature                      | Impact |
|-----------------------------|--------|
| System Event + Email Alert  | Builds motivation and awareness |
| Dashboards & Statistics     | Promotes transparency and encourages competition |
| Mass Add Wizard             | Saves time, ensures consistency, increases adoption |

## Execution
Prompt: Let's implement the haluc_points Odoo module as described in the haluc_points_ssd.md file. Please proceed with the following steps, and after each major step, wait for my confirmation before moving to the next. Register completed tasks in the markdown tasklist. Ensure that each step aligns with the specifications provided in the document, and notify me if any clarification is needed before proceeding. Additional Notes:
- Use clear commit messages for each implemented feature.
- Provide a brief summary of changes after completing each step.
- Ensure proper testing and validation for each module component before marking tasks as complete.
- Maintain modularity and adhere to Odoo development best practices.






