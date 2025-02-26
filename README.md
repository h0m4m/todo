# To-Do List Application

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
