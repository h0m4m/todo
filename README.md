# To-Do List Application (with AI)

This is a web-based To-Do List application built with Flask and SQLAlchemy. It allows users to manage their tasks using different views: List, Calendar, and Kanban. The application also integrates with Google Gemini AI to generate task plans.

## Features

### Task Management
- **Add Task**: Users can add new tasks with optional due dates, priorities, and statuses.
- **Edit Task**: Users can edit existing tasks directly from the List and Kanban views.
- **Delete Task**: Users can delete tasks they no longer need.
- **Toggle Task Completion**: Users can mark tasks as complete or incomplete.

### Views
- **List View**: Displays all tasks in a list format. Users can see task details, mark tasks as complete, delete tasks, and generate AI plans.
- **Calendar View**: Displays tasks in a calendar month grid. Tasks are shown on their respective due dates.
- **Kanban View**: Displays tasks in a Kanban board format, grouped by their status (Not Started, In Progress, Done). Users can drag and drop tasks between columns to update their status.

### AI Integration
- **AI Plan Generation**: Users can generate AI-generated plans for tasks using Google Gemini AI. The AI plan provides a step-by-step guide to complete the task.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```sh
   flask run
   ```

## Usage

- Navigate to `http://127.0.0.1:5000/` in your web browser to access the application.
- Use the navigation bar to switch between List, Calendar, and Kanban views.
- Add, edit, delete, and manage tasks as needed.
- Generate AI plans for tasks by clicking the "AI Plan" button.

## File Structure

- app.py: Main application file containing routes and logic.
- templates: Directory containing HTML templates for different views.
  - index.html: Template for the List view.
  - calendar.html: Template for the Calendar view.
  - kanban.html: Template for the Kanban view.
## License

This project is licensed under the MIT License. See the LICENSE file for details.
