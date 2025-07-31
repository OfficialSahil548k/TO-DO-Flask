from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# In-memory "database" for storing to-do items
# Each item is a dictionary with 'id', 'task', 'completed', and 'created_at' keys
todos = []
task_id_counter = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page, which displays the to-do list and allows adding new tasks.
    """
    global task_id_counter
    
    # If the request is a POST, it means a new task is being added.
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content:  # Ensure the content is not empty
            new_todo = {
                'id': task_id_counter,
                'task': task_content,
                'completed': False,
                'created_at': datetime.utcnow()
            }
            todos.append(new_todo)
            task_id_counter += 1
        return redirect(url_for('index'))

    # For a GET request, render the page with the list of tasks.
    # Sort tasks to show uncompleted ones first
    sorted_todos = sorted(todos, key=lambda x: x['completed'])
    
    # Check if there are any tasks and if all of them are completed.
    all_tasks_done = False
    if todos:  # Check if the list is not empty
        all_tasks_done = all(todo['completed'] for todo in todos)

    return render_template('index.html', todos=sorted_todos, all_tasks_done=all_tasks_done)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """
    Deletes a task based on its ID.
    """
    global todos
    # Find the task with the given id and remove it
    todos = [todo for todo in todos if todo['id'] != task_id]
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """
    Marks a task as complete or incomplete.
    """
    # Find the task and toggle its 'completed' status
    for todo in todos:
        if todo['id'] == task_id:
            todo['completed'] = not todo['completed']
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 4. Run this script (python app.py).
    # 5. Open your browser and go to http://127.0.0.1:5000
    app.run(debug=True)
