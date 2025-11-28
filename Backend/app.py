from flask import Flask, render_template
from dotenv import load_dotenv
import os

# Import routes
from routes.auth_routes import auth_bp
from routes.course_routes import course_bp
from routes.enrollment_routes import enrollment_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(course_bp, url_prefix='/api/courses')
app.register_blueprint(enrollment_bp, url_prefix='/api/enrollments')

# 1. Landing Page (The ROOT URL)
@app.route('/')
def home():
    # This MUST match the filename in your templates folder exactly
    return render_template('index.html')

# 2. Login Page (Separate URL)
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# 3. Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/courses')
def courses():
    return render_template('courses.html')

# 5. Enrolled Courses Page
@app.route('/enrolled')
def enrolled():
    return render_template('enrolled.html')

# ==========================================
#  ERROR HANDLERS
# ==========================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="We couldn't find that page."), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)