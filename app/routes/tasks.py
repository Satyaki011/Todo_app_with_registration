from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/', methods=['GET'])
def tasks_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('tasks.html', tasks=tasks)

@task_bp.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    title = request.form.get('title')
    if title:
        new_task = Task(user_id=user_id, title=title, status='Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')

    return redirect(url_for('tasks.tasks_list'))

@task_bp.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        # Toggle between Pending and Done
        task.status = 'Pending' if task.status == 'Done' else 'Done'
        db.session.commit()
        flash('Task updated successfully!', 'success')
    
    return redirect(url_for('tasks.tasks_list'))

@task_bp.route('/clear', methods=['POST'])
def clear_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    Task.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash('All tasks cleared!', 'success')
    
    return redirect(url_for('tasks.tasks_list'))