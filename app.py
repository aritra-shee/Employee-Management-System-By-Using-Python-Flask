from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/employee_management_db'
app.config['SECRET_KEY'] = 'employee_management_system'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None and user_id != '':
        return User.query.get(int(user_id))
    return None


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(70), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.Column(db.String(100), nullable=False)

    organization_rel = db.relationship('Organization', backref='users')


    def is_hr(self):
        # Implement the logic to determine if the user is from HR department
        # For example, check if the user's organization is 'HR'
        if isinstance(self.organization, str):
            return False
        return self.organization.name == 'HR'


class RegisterForm(FlaskForm):
    first_name = StringField(validators=[
        InputRequired(), Length(min=3, max=70)], render_kw={"placeholder": "First Name"})
    
    last_name = StringField(validators=[
        InputRequired(), Length(min=3, max=50)], render_kw={"placeholder": "Last Name"})

    email = StringField(validators=[
        InputRequired(), Length(min=10, max=50)], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    
    organization = StringField(validators=[
        InputRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Organization Name"})

    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    email = StringField(validators=[
        InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Login')


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))


class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employees = db.relationship('Employee', backref='organization', lazy=True)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch employees based on the organization of the current user
    employees = Employee.query.filter_by(organization_id=current_user.organization_id).all()
    return render_template('dashboard.html', employees=employees)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error_message = None

    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            error_message = 'Email is already registered.'

        else:
            # Check if the organization already exists
            existing_organization = Organization.query.filter_by(name=form.organization.data).first()

            if existing_organization:
                # If the organization exists, use its ID
                organization_id = existing_organization.id
            else:
                # If the organization doesn't exist, create a new one
                new_organization = Organization(name=form.organization.data)
                db.session.add(new_organization)
                db.session.commit()
                organization_id = new_organization.id

            # Hash the password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            # Create a new user and associate it with the organization
            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hashed_password,
                organization_id=organization_id,
                organization=form.organization.data  # Store organization name in user table
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form, error_message=error_message)




@app.route('/add_new_employee', methods=['GET', 'POST'])
@login_required
def add_new_employee():
    # Fetch employees based on the organization of the current user
    employees = Employee.query.filter_by(organization_id=current_user.organization_id).all()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        joining_date = request.form['joining_date']
        designation = request.form['designation']
        organization_id = current_user.organization_id

        new_employee = Employee(name=name, email=email, phone=phone, address=address, joining_date=joining_date, designation=designation, organization_id=organization_id)
        db.session.add(new_employee)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('addnewemployee.html', current_user=current_user, employees=employees)


@app.route('/update_employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.phone = request.form['phone']
        employee.address = request.form['address']
        employee.designation = request.form['designation']

        db.session.commit()
        return redirect(url_for('dashboard'))

    # Pass the employee's name to the template
    employee_name = employee.name

    return render_template('updateemployee.html', employee_name=employee_name)


@app.route('/delete_emp/<int:id>', methods=['POST'])
def delete_emp(id):
    if request.form.get('_method') == 'delete':
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully.', 'success')
        return redirect(url_for('dashboard'))

@app.route('/singleemployeeprofile/<int:id>')
def singleemployeeprofile(id):
    employee = Employee.query.get_or_404(id)
    if employee.joining_date is not None:
        # Format the joining date in the desired format (dd-mm-yyyy)
        employee.joining_date = employee.joining_date.strftime('%d-%m-%Y')
        last_updated_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('singleemployeeprofile.html', employee=employee, last_updated_date=last_updated_date)


if __name__ == "__main__":
    app.run(debug=True)