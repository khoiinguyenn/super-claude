#!/usr/bin/env python3
"""
Interactive demo that simulates user commands for the Task & Habit Tracker
"""

from main import TaskTracker, Priority
import time

def simulate_command(command, description=""):
    """Simulate typing a command"""
    print(f"\n💻 > {command}")
    if description:
        print(f"   {description}")
    time.sleep(0.5)

def run_interactive_demo():
    print("🚀 Welcome to Personal Task & Habit Tracker!")
    print("Type 'help' for commands or 'quit' to exit")
    
    tracker = TaskTracker("interactive_demo.json")
    
    # Simulate the interactive session
    simulate_command("help", "Let's see what commands are available")
    
    print("""
📚 COMMANDS:
  Tasks:
    list                  - Show pending tasks
    list all             - Show all tasks (including completed)
    add task             - Add a new task (interactive)
    complete <id>        - Mark task as completed
  
  Habits:
    habits               - Show all habits
    add habit            - Add a new habit (interactive)
    done <habit_name>    - Mark habit as done for today
  
  Other:
    stats                - Show statistics
    help                 - Show this help
    quit                 - Exit the application
                """)
    
    # Add some sample data if empty
    if not tracker.tasks:
        print("\n🎉 Setting up sample data...")
        tracker.add_task("Learn Python decorators", "Study how decorators work", Priority.HIGH, ["learning", "python"])
        tracker.add_task("Exercise for 30 minutes", "Go for a run or gym", Priority.MEDIUM, ["health"])
        tracker.add_task("Read a book chapter", "Continue reading current book", Priority.LOW, ["learning", "reading"])
        
        tracker.add_habit("Daily coding", "Write code for at least 30 minutes", 30)
        tracker.add_habit("Exercise", "Any form of physical activity", 21)
        tracker.add_habit("Read", "Read for 15 minutes", 14)
    
    # Show current tasks
    simulate_command("list", "Let's see our current tasks")
    tracker.list_tasks()
    
    # Show habits
    simulate_command("habits", "Check our habit progress")
    tracker.show_habits()
    
    # Complete a task
    simulate_command("complete 1", "Mark the Python decorators task as done")
    tracker.complete_task(1)
    
    # Complete a habit
    simulate_command("done Daily coding", "Mark today's coding habit complete")
    tracker.complete_habit("Daily coding")
    
    # Add a new task (simulate the interactive input)
    simulate_command("add task", "Let's add a new task")
    print("Task title: Write unit tests")
    print("Description (optional): Add tests for the tracker functionality")
    print("Priority: 1=Low 🟢, 2=Medium 🟡, 3=High 🔴")
    print("Priority (1-3): 2")
    print("Tags (comma-separated, optional): testing, python")
    
    tracker.add_task("Write unit tests", "Add tests for the tracker functionality", Priority.MEDIUM, ["testing", "python"])
    
    # Show updated tasks
    simulate_command("list all", "Show all tasks including completed ones")
    tracker.list_tasks(show_completed=True)
    
    # Show stats
    simulate_command("stats", "Check our progress statistics")
    total_tasks = len(tracker.tasks)
    completed_tasks = sum(1 for t in tracker.tasks if t.status.value == "✅")
    total_habits = len(tracker.habits)
    
    print("\n📊 STATISTICS")
    print("=" * 30)
    print(f"📋 Tasks: {completed_tasks}/{total_tasks} completed")
    print(f"🎯 Habits: {total_habits} being tracked")
    
    if tracker.habits:
        avg_streak = sum(h.current_streak for h in tracker.habits) / len(tracker.habits)
        print(f"🔥 Average streak: {avg_streak:.1f} days")
    
    # Show JSON data was saved
    simulate_command("quit", "Exit the application")
    print("👋 Goodbye! Keep being productive!")
    
    print(f"\n💾 All data has been saved to: {tracker.data_file}")
    print("🔄 You can restart the app and your data will be restored!")

if __name__ == "__main__":
    run_interactive_demo()