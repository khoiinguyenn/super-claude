#!/usr/bin/env python3
"""
Demo script to showcase the Personal Task & Habit Tracker functionality
"""

from main import TaskTracker, Priority

def demo():
    print("🚀 Personal Task & Habit Tracker Demo")
    print("=" * 50)
    
    # Create tracker instance
    tracker = TaskTracker("demo_data.json")
    
    # Add some tasks
    print("\n📋 Adding tasks...")
    tracker.add_task("Learn Python decorators", "Study how decorators work", Priority.HIGH, ["learning", "python"])
    tracker.add_task("Exercise for 30 minutes", "Go for a run or gym", Priority.MEDIUM, ["health"])
    tracker.add_task("Read a book chapter", "Continue reading current book", Priority.LOW, ["learning", "reading"])
    
    # Add some habits
    print("\n🎯 Adding habits...")
    tracker.add_habit("Daily coding", "Write code for at least 30 minutes", 30)
    tracker.add_habit("Exercise", "Any form of physical activity", 21)
    tracker.add_habit("Read", "Read for 15 minutes", 14)
    
    # Show tasks
    print("\n" + "="*50)
    tracker.list_tasks()
    
    # Show habits
    print("\n" + "="*50)
    tracker.show_habits()
    
    # Complete a task
    print("\n📝 Completing task #1...")
    tracker.complete_task(1)
    
    # Complete a habit
    print("\n🔥 Completing 'Daily coding' habit...")
    tracker.complete_habit("Daily coding")
    
    # Show updated tasks
    print("\n" + "="*50)
    print("📋 UPDATED TASKS:")
    tracker.list_tasks(show_completed=True)
    
    # Show updated habits
    print("\n" + "="*50)
    print("🎯 UPDATED HABITS:")
    tracker.show_habits()
    
    # Show stats
    print("\n" + "="*50)
    total_tasks = len(tracker.tasks)
    completed_tasks = sum(1 for t in tracker.tasks if t.status.value == "✅")
    total_habits = len(tracker.habits)
    
    print("📊 STATISTICS")
    print("=" * 30)
    print(f"📋 Tasks: {completed_tasks}/{total_tasks} completed")
    print(f"🎯 Habits: {total_habits} being tracked")
    
    if tracker.habits:
        avg_streak = sum(h.current_streak for h in tracker.habits) / len(tracker.habits)
        print(f"🔥 Average streak: {avg_streak:.1f} days")
    
    print("\n✨ Demo complete! The interactive app supports:")
    print("   • help - Show all commands")
    print("   • list - View tasks")
    print("   • add task - Create new task")
    print("   • complete <id> - Mark task done")
    print("   • habits - View habit progress")
    print("   • add habit - Create new habit")
    print("   • done <habit> - Mark habit complete")
    print("   • stats - View statistics")
    print("   • quit - Exit")
    
    print(f"\n💾 Data saved to: {tracker.data_file}")

if __name__ == "__main__":
    demo()