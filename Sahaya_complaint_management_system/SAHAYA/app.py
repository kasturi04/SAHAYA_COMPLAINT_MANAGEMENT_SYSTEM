from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, Complaint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sahaya-official-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vgrs.db'

# --- 1. RECTIFIED MAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kusuluriaparna@gmail.com' 
app.config['MAIL_PASSWORD'] = 'yhvq jeyi ngtt kjjb' 
app.config['MAIL_DEFAULT_SENDER'] = 'kusuluriaparna@gmail.com'

mail = Mail(app)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- 2. ADVANCED DEPARTMENT CLASSIFICATION (10+ Categories) ---
def ai_classify(text):
    text = text.lower()
    dept_map = {
        "Public Services (Panchayat/Municipal)": ["water", "drainage", "garbage", "sanitation", "street light"],
        "Infrastructure & Development (R&B)": ["road", "pothole", "bridge", "building", "construction"],
        "Health & Medical Services": ["hospital", "doctor", "medicine", "ambulance", "fever", "health"],
        "Education Department": ["school", "college", "scholarship", "exam", "teacher"],
        "Revenue & Land Records": ["land", "tax", "registration", "survey", "patta"],
        "Law & Order (Police)": ["police", "traffic", "safety", "crime", "security"],
        "Civil Supplies & Housing": ["ration", "housing", "ration card", "dbt", "subsidy"],
        "Agriculture & Environment": ["crop", "irrigation", "fertilizer", "seed", "pollution"],
        "Transport": ["bus", "transport", "bus pass"]
    }
    for dept, keywords in dept_map.items():
        if any(word in text for word in keywords): return dept
    return "General / Public Grievance"

# --- 3. MAIL SENDER FUNCTION ---
def send_officer_notification(complaint, department):
    try:
        msg = Message(f"Official Alert: New {department} Complaint",
                      recipients=["kusuluriaparna@gmail.com"]) 
        msg.body = f"Complaint ID: #{complaint.complaint_id}\nDept: {department}\nIssue: {complaint.description}\nLocation: {complaint.address}"
        mail.send(msg)
        print(f"📧 EMAIL SENT SUCCESSFULLY TO {department} OFFICER!")
    except Exception as e:
        print(f"❌ MAIL ERROR: {e}")

# --- 4. ROUTES ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        is_admin_flag = True if request.form.get('is_admin') == 'on' else False
        hashed_pw = generate_password_hash(request.form['password'])
        new_u = User(name=request.form['name'], phone=request.form['phone'], 
                     email=request.form['email'], password=hashed_pw,
                     is_admin=is_admin_flag)
        try:
            db.session.add(new_u)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash("User already exists or Phone number registered!")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        idn = request.form['identifier']
        u = User.query.filter((User.email == idn) | (User.phone == idn)).first()
        if u and check_password_hash(u.password, request.form['password']):
            login_user(u)
            if u.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        flash('Invalid Credentials!')
    return render_template('login.html')

@app.route('/submit_complaint', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if request.method == 'POST':
        dept = ai_classify(request.form['description'])
        new_c = Complaint(user_id=current_user.id, category=dept, 
                          description=request.form['description'], address=request.form.get('address'))
        db.session.add(new_c)
        db.session.commit()
        print(f"✅ COMPLAINT #{new_c.complaint_id} SUBMITTED!")
        send_officer_notification(new_c, dept)
        return redirect(url_for('track_complaint'))
    return render_template('submit_complaint.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin: return redirect(url_for('home'))
    complaints = Complaint.query.all()
    return render_template('admin_dashboard.html', complaints=complaints)

# BuildError FIX: Single instance of update_status
@app.route('/update_status/<int:complaint_id>', methods=['POST'])
@login_required
def update_status(complaint_id):
    if not current_user.is_admin: return redirect(url_for('home'))
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = request.form['new_status']
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/track_complaint')
@login_required
def track_complaint():
    complaints = Complaint.query.filter_by(user_id=current_user.id).all()
    return render_template('track_complaint.html', complaints=complaints)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)