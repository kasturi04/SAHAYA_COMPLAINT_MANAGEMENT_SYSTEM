# 🏛️ SAHAYA: Smart Grievance Management System

**SAHAYA** is a modern, Flask-powered web portal designed to streamline the communication between citizens and government departments. The system features an automated classification engine that routes public grievances to the appropriate authorities in real-time.

---

## ✨ Key Features

* **Smart Categorization**: Automatically classifies complaints into 10+ departments (Health, Roads, Revenue, etc.) using keyword-based logic.
* **Dual-Role Access**: Dedicated portals for **Citizens** (to file & track) and **Admins/Officers** (to manage & resolve).
* **Automated Email Alerts**: Triggers instant SMTP email notifications to department heads upon grievance submission.
* **Premium Dark UI**: A high-contrast "Black & Electric Blue" theme designed for modern usability.
* **Data Security**: Implements secure password hashing using the Werkzeug library.

---

## 🛠️ Technical Stack

### **Backend**
* **Python 3.10+**: Core logic implementation.
* **Flask**: Web framework for routing and session management.
* **SQLAlchemy**: Database ORM for SQLite.
* **Flask-Mail**: SMTP integration for automated alerts.

### **Frontend**
* **HTML5 & CSS3**: Custom structured layouts and premium styling.
* **Bootstrap 5**: Responsive grid system and professional components.
* **Jinja2**: Dynamic server-side templating.

---

## 📂 Project Structure

```text
SAHAYA/
├── app.py              # Application logic and routes
├── models.py           # Database models (User & Complaint)
├── requirements.txt    # Project dependencies
├── static/             # Assets (CSS, Uploads, Icons)
│   ├── css/
│   └── uploads/
└── templates/          # HTML Templates
    ├── home.html
    ├── login.html
    ├── admin_dashboard.html
    └── track_complaint.html
