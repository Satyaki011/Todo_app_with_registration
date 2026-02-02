from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

# User storage (in a real app, this would be a database)
USER_DATA = {
    "admin": "123",
    "satyaki": "1234"
}


@auth_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('tasks.tasks_list'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USER_DATA and USER_DATA[username] == password:
            session['user_id'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('tasks.tasks_list'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not username or not password or not confirm_password:
            flash('All fields are required', 'danger')
        elif len(username) < 3:
            flash('Username must be at least 3 characters long', 'danger')
        elif len(password) < 4:
            flash('Password must be at least 4 characters long', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        elif username in USER_DATA:
            flash('Username already exists. Please choose another one', 'danger')
        else:
            # Register the user
            USER_DATA[username] = password
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('auth.login'))