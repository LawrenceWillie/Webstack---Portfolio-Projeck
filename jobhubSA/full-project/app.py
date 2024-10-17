from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, logout_user, current_user, LoginManager, login_required
from mongoengine import connect, StringField, BooleanField, EmailField, Document, ListField, URLField, DecimalField, ReferenceField, DateTimeField, IntField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = 'supersecretkey'

# Connecting to MongoDB Atlas
connect(db="jobhub_db", host="mongodb+srv://itumeleng:Itumeleng1.@cluster0.3klnl.mongodb.net/")

# Creating User model for storing data in MongoDB
class User(Document, UserMixin):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)
    skills = ListField(StringField())
    portfolio = URLField()
    courses_completed = ListField(StringField())
    reviews = ListField(StringField())
    is_mentor = BooleanField(default=False)
    mentor_bio = StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        user.save()
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('signup.html',  user=current_user)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.objects(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('profile'))
        flash("Invalid login details.")
    return render_template('login.html',  user=current_user)

# Profile route
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Defining JobPost model
class JobPost(Document):
    title = StringField(required=True)
    company = StringField(required=True)
    location = StringField(required=True)
    category = StringField(required=True)
    description = StringField()
    salary = DecimalField()

# Job listings route
@app.route('/jobs')
def job_listings():
    post_job =JobPost (
    title = "Junior Dev",
    company = "Limpopo Connexion",
    location = "Johannesburg",
    category = "Technical",
    description = "Assist Teams with developing softwares and mobile apps",
    salary = ('5000')

    )
    post_job.save()
    location = request.args.get('location')
    category = request.args.get('category')

    query = {}
    if location:
        query['location__icontains'] = location
    if category:
        query['category__icontains'] = category

    jobs = JobPost.objects(**query)
    return render_template('job_listings.html', jobs=jobs,  user=current_user)

# Creating Application model
class Application(Document):
    user = ReferenceField(User)
    job = ReferenceField(JobPost)
    applied_at = DateTimeField(default=datetime.utcnow)

# Apply job route
@app.route('/apply/<job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = JobPost.objects(id=job_id).first()
    if job:
        application = Application(user=current_user, job=job)
        application.save()
        return redirect(url_for('job_listings'))
    return 'Job not found', 404

# Mentorship route
@app.route('/mentors')
def mentors():
    mentors = User.objects(is_mentor=True)
    return render_template('mentors.html', mentors=mentors,  user=current_user)

# Defining Course model
class Course(Document):
    title = StringField(required=True)
    description = StringField()
    duration = IntField()

# Defining UserCourseProgress model
class UserCourseProgress(Document):
    user = ReferenceField(User)
    course = ReferenceField(Course)
    progress = DecimalField(min_value=0, max_value=100)

# Courses route
@app.route('/courses')
def courses():
    #creating Courses document
    course = Course(
        title="Software Engineer- Front-end",
        description="This course provides you with the knowledge and expose you to tools you can use to develop websites effectively.",
        duration=5
    )
    course.save()

    courses = Course.objects()
    return render_template('courses.html', courses=courses, user=current_user)

# Route to get specific course by id
@app.route('/course/<course_id>')
@login_required
def course_detail(course_id):
    course = Course.objects(id=course_id).first()
    progress = UserCourseProgress.objects(user=current_user, course=course).first()
    return render_template('course_detail.html', course=course, progress=progress,  user=current_user)

if __name__ == "__main__":
    app.run(debug=True)
