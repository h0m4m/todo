import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import calendar
import google.generativeai as genai

app = Flask(__name__)

# SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://@Humam/test?"
    "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Model with status column
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.Integer, default=3)
    status = db.Column(db.String(20), nullable=False, default='not started')  # new column

    def __repr__(self):
        return f"<Task {self.id}: {self.content[:20]}...>"

@app.route('/', methods=['GET'])
def index():
    """Display tasks in a list view."""
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks, active_view="list")

@app.route('/calendar', methods=['GET'])
def calendar_view():
    """Display tasks in a calendar month grid view."""
    now = datetime.now()
    year, month = now.year, now.month
    month_matrix = calendar.monthcalendar(year, month)
    
    tasks = Task.query.filter(Task.due_date != None).all()
    tasks_by_day = {}
    for task in tasks:
        if task.due_date.year == year and task.due_date.month == month:
            tasks_by_day.setdefault(task.due_date.day, []).append(task)
    
    return render_template('calendar.html',
                           calendar=month_matrix,
                           tasks_by_day=tasks_by_day,
                           year=year,
                           month=month,
                           active_view="calendar")

@app.route('/kanban', methods=['GET'])
def kanban_view():
    """Display tasks in a Kanban board grouped by status."""
    # Query all tasks, then group by status.
    tasks = Task.query.order_by(Task.id).all()
    groups = {
        "not started": [],
        "in progress": [],
        "done": []
    }
    for task in tasks:
        groups.setdefault(task.status, []).append(task)
    return render_template('kanban.html', groups=groups, active_view="kanban")

@app.route('/add', methods=['POST'])
def add_task():
    """Create a new task with optional due date, priority, and status."""
    content = request.form.get('content')
    due_date_str = request.form.get('due_date')
    priority_str = request.form.get('priority')
    status = request.form.get('status', 'not started')  # default value

    if content:
        new_task = Task(content=content, status=status)
        if due_date_str:
            try:
                new_task.due_date = date.fromisoformat(due_date_str)
            except ValueError:
                pass
        if priority_str:
            try:
                new_task.priority = int(priority_str)
            except ValueError:
                pass

        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['GET'])
def toggle_task(task_id):
    """Toggle the completed status of a task."""
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['GET', 'PUT'])
def update_task(task_id):
    """Update an existing task's details including status."""
    task = Task.query.get_or_404(task_id)

    if request.method == 'PUT':
        content = request.form.get('content')
        due_date_str = request.form.get('due_date')
        priority_str = request.form.get('priority')
        status = request.form.get('status')
        if content:
            task.content = content
        if due_date_str:
            try:
                task.due_date = date.fromisoformat(due_date_str)
            except ValueError:
                pass
        else:
            task.due_date = None
        if priority_str:
            try:
                task.priority = int(priority_str)
            except ValueError:
                pass
        if status:
            task.status = status
        db.session.commit()
        return jsonify({"message": "Task updated"}), 200

    return render_template('update.html', task=task)

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by its ID."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200


# Set up Gemini API key
genai.configure(api_key="AIzaSyBEGnWRltGj4VDQTun3zCeccWiADLZtkBI")

@app.route('/ai_plan/<int:task_id>', methods=['GET'])
def ai_plan(task_id):
    """Generate an AI plan for a task using Google Gemini AI."""
    task = Task.query.get_or_404(task_id)
    prompt = f"Generate a very short, step-by-step plan to achieve the following task (do not use text markup): {task.content}"

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Ensure model is correct
        response = model.generate_content(prompt)
        plan = response.text if hasattr(response, "text") else "No plan generated."

        return jsonify({"plan": plan}), 200
    except Exception as e:
        print("Error generating AI plan:", e)
        return jsonify({"error": "Failed to generate AI plan."}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
