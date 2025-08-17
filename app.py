#!/usr/bin/env python3
"""
Flask Web Application for Personal Task & Habit Tracker
A modern web interface for the task and habit tracking system.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from main import TaskTracker, Priority, TaskStatus
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Global tracker instance
tracker = TaskTracker("web_tracker_data.json")

@app.route('/')
def index():
    """Main sticky notes page"""
    return render_template('index.html', tasks=tracker.tasks)

# API Endpoints
@app.route('/api/task', methods=['POST'])
def add_task():
    """Add a new task"""
    try:
        data = request.json
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        priority = Priority(data.get('priority', Priority.MEDIUM.value))
        tags = [tag.strip() for tag in data.get('tags', '').split(',') if tag.strip()]
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        tracker.add_task(title, description, priority, tags)
        return jsonify({'success': True, 'message': 'Task added successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed"""
    try:
        for task in tracker.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                tracker.save_data()
                return jsonify({'success': True, 'message': 'Task completed'})
        
        return jsonify({'error': 'Task not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        tracker.tasks = [t for t in tracker.tasks if t.id != task_id]
        tracker.save_data()
        return jsonify({'success': True, 'message': 'Task deleted'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/habit', methods=['POST'])
def add_habit():
    """Add a new habit"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        target_days = int(data.get('target_days', 30))
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        tracker.add_habit(name, description, target_days)
        return jsonify({'success': True, 'message': 'Habit added successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/habit/<habit_name>/complete', methods=['POST'])
def complete_habit(habit_name):
    """Mark a habit as completed for today"""
    try:
        today = datetime.now().date().isoformat()
        
        for habit in tracker.habits:
            if habit.name.lower() == habit_name.lower():
                if today in habit.completed_dates:
                    return jsonify({'error': 'Already completed today'}), 400
                
                habit.completed_dates.append(today)
                habit.current_streak += 1
                habit.longest_streak = max(habit.longest_streak, habit.current_streak)
                tracker.save_data()
                return jsonify({'success': True, 'message': 'Habit completed', 'streak': habit.current_streak})
        
        return jsonify({'error': 'Habit not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/habit/<habit_name>/delete', methods=['DELETE'])
def delete_habit(habit_name):
    """Delete a habit"""
    try:
        tracker.habits = [h for h in tracker.habits if h.name != habit_name]
        tracker.save_data()
        return jsonify({'success': True, 'message': 'Habit deleted'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Form-based routes for non-JS browsers
@app.route('/add_task', methods=['POST'])
def add_task_form():
    """Add task via form submission"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority_value = request.form.get('priority', Priority.MEDIUM.value)
    tags = [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()]
    
    if title:
        priority = Priority(priority_value)
        tracker.add_task(title, description, priority, tags)
        flash('Task added successfully!', 'success')
    else:
        flash('Title is required!', 'error')
    
    return redirect(url_for('tasks'))

@app.route('/add_habit', methods=['POST'])
def add_habit_form():
    """Add habit via form submission"""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    target_days = int(request.form.get('target_days', 30))
    
    if name:
        tracker.add_habit(name, description, target_days)
        flash('Habit added successfully!', 'success')
    else:
        flash('Name is required!', 'error')
    
    return redirect(url_for('habits'))

@app.route('/complete_task/<int:task_id>')
def complete_task_form(task_id):
    """Complete task via URL"""
    for task in tracker.tasks:
        if task.id == task_id:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            tracker.save_data()
            flash(f'Task "{task.title}" completed!', 'success')
            break
    return redirect(url_for('tasks'))

@app.route('/complete_habit/<habit_name>')
def complete_habit_form(habit_name):
    """Complete habit via URL"""
    today = datetime.now().date().isoformat()
    
    for habit in tracker.habits:
        if habit.name.lower() == habit_name.lower():
            if today not in habit.completed_dates:
                habit.completed_dates.append(today)
                habit.current_streak += 1
                habit.longest_streak = max(habit.longest_streak, habit.current_streak)
                tracker.save_data()
                flash(f'Habit "{habit.name}" completed! Streak: {habit.current_streak} days', 'success')
            else:
                flash(f'Habit "{habit.name}" already completed today!', 'warning')
            break
    return redirect(url_for('habits'))

if __name__ == '__main__':
    # Add some sample data if none exists
    if not tracker.tasks and not tracker.habits:
        print("🎉 Setting up sample data...")
        tracker.add_task("Learn Flask", "Build a web application with Flask", Priority.HIGH, ["learning", "python", "web"])
        tracker.add_task("Exercise for 30 minutes", "Go for a run or gym", Priority.MEDIUM, ["health"])
        tracker.add_task("Read a book chapter", "Continue reading current book", Priority.LOW, ["learning", "reading"])
        
        tracker.add_habit("Daily coding", "Write code for at least 30 minutes", 30)
        tracker.add_habit("Exercise", "Any form of physical activity", 21)
        tracker.add_habit("Read", "Read for 15 minutes", 14)
    
    print("🚀 Starting Task & Habit Tracker Web App...")
    print("📱 Open http://localhost:5001 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5001)