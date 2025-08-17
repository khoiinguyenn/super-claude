#!/usr/bin/env python3
"""
Personal Task & Habit Tracker
A fun CLI application to demonstrate Claude's capabilities!

Features:
- Task management with priorities
- Habit tracking with streaks
- Data persistence with JSON
- Interactive CLI with colors
- Statistics and insights
"""

import json
import os
import subprocess
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class Priority(Enum):
    LOW = "🟢"
    MEDIUM = "🟡" 
    HIGH = "🔴"


class TaskStatus(Enum):
    PENDING = "⏳"
    IN_PROGRESS = "🔄"
    COMPLETED = "✅"
    CANCELLED = "❌"


@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: Priority
    status: TaskStatus
    created_at: str
    completed_at: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class Habit:
    name: str
    description: str
    target_days: int
    current_streak: int
    longest_streak: int
    completed_dates: List[str]
    created_at: str


class GitHubIntegration:
    """GitHub CLI integration for managing issues and pull requests"""
    
    def __init__(self):
        self.authenticated = self._check_auth()
    
    def _check_auth(self) -> bool:
        """Check if user is authenticated with GitHub CLI"""
        try:
            result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def _run_gh_command(self, args: List[str]) -> Optional[Dict[str, Any]]:
        """Run a gh command and return JSON output"""
        if not self.authenticated:
            print("❌ Not authenticated with GitHub. Run 'gh auth login' first.")
            return None
        
        try:
            cmd = ['gh'] + args + ['--json']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout) if result.stdout.strip() else {}
        except subprocess.CalledProcessError as e:
            print(f"❌ GitHub command failed: {e}")
            return None
        except json.JSONDecodeError:
            print("❌ Failed to parse GitHub response")
            return None
    
    def create_issue(self, title: str, body: str = "", labels: List[str] = None) -> bool:
        """Create a new GitHub issue"""
        if not self.authenticated:
            print("❌ Not authenticated with GitHub. Run 'gh auth login' first.")
            return False
        
        try:
            cmd = ['gh', 'issue', 'create', '--title', title]
            if body:
                cmd.extend(['--body', body])
            if labels:
                cmd.extend(['--label', ','.join(labels)])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue_url = result.stdout.strip()
            print(f"✅ Issue created: {issue_url}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create issue: {e}")
            return False
    
    def list_issues(self, state: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
        """List GitHub issues"""
        if not self.authenticated:
            print("❌ Not authenticated with GitHub. Run 'gh auth login' first.")
            return []
        
        try:
            cmd = ['gh', 'issue', 'list', '--state', state, '--limit', str(limit), '--json', 'number,title,state,labels,assignees,createdAt']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issues = json.loads(result.stdout) if result.stdout.strip() else []
            
            if not issues:
                print(f"📝 No {state} issues found")
                return []
            
            print(f"\n🐛 GITHUB ISSUES ({state.upper()})")
            print("=" * 60)
            
            for issue in issues:
                labels_str = f" [{', '.join([l['name'] for l in issue.get('labels', [])])}]" if issue.get('labels') else ""
                assignees_str = f" 👤 {', '.join([a['login'] for a in issue.get('assignees', [])])}" if issue.get('assignees') else ""
                print(f"#{issue['number']} {issue['title']}{labels_str}{assignees_str}")
            
            return issues
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"❌ Failed to list issues: {e}")
            return []
    
    def create_pr(self, title: str, body: str = "", base: str = "main") -> bool:
        """Create a new pull request"""
        if not self.authenticated:
            print("❌ Not authenticated with GitHub. Run 'gh auth login' first.")
            return False
        
        try:
            cmd = ['gh', 'pr', 'create', '--title', title, '--base', base]
            if body:
                cmd.extend(['--body', body])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            pr_url = result.stdout.strip()
            print(f"✅ Pull request created: {pr_url}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create PR: {e}")
            return False
    
    def list_prs(self, state: str = "open", limit: int = 10) -> List[Dict[str, Any]]:
        """List GitHub pull requests"""
        if not self.authenticated:
            print("❌ Not authenticated with GitHub. Run 'gh auth login' first.")
            return []
        
        try:
            cmd = ['gh', 'pr', 'list', '--state', state, '--limit', str(limit), '--json', 'number,title,state,author,createdAt,headRefName']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            prs = json.loads(result.stdout) if result.stdout.strip() else []
            
            if not prs:
                print(f"📝 No {state} pull requests found")
                return []
            
            print(f"\n🔀 PULL REQUESTS ({state.upper()})")
            print("=" * 60)
            
            for pr in prs:
                author = pr.get('author', {}).get('login', 'Unknown')
                branch = pr.get('headRefName', '')
                print(f"#{pr['number']} {pr['title']} (by {author} from {branch})")
            
            return prs
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"❌ Failed to list PRs: {e}")
            return []
    
    def sync_task_to_issue(self, task: 'Task') -> bool:
        """Convert a task to a GitHub issue"""
        labels = task.tags + [f"priority-{task.priority.name.lower()}"]
        body = f"**Description:** {task.description}\n\n**Priority:** {task.priority.value} {task.priority.name}\n\n**Created:** {task.created_at}"
        
        return self.create_issue(task.title, body, labels)


class TaskTracker:
    def __init__(self, data_file: str = "tracker_data.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.habits: List[Habit] = []
        self.next_task_id = 1
        self.github = GitHubIntegration()
        self.load_data()
    
    def save_data(self):
        """Save all data to JSON file"""
        # Convert tasks to dict with enum values as strings
        tasks_data = []
        for task in self.tasks:
            task_dict = asdict(task)
            task_dict["priority"] = task.priority.value
            task_dict["status"] = task.status.value
            tasks_data.append(task_dict)
        
        data = {
            "tasks": tasks_data,
            "habits": [asdict(habit) for habit in self.habits],
            "next_task_id": self.next_task_id
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load data from JSON file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Restore tasks
            for task_data in data.get("tasks", []):
                task_data["priority"] = Priority(task_data["priority"])
                task_data["status"] = TaskStatus(task_data["status"])
                self.tasks.append(Task(**task_data))
            
            # Restore habits
            for habit_data in data.get("habits", []):
                self.habits.append(Habit(**habit_data))
            
            self.next_task_id = data.get("next_task_id", 1)
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️ Error loading data: {e}")
    
    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM, tags: List[str] = None):
        """Add a new task"""
        task = Task(
            id=self.next_task_id,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING,
            created_at=datetime.now().isoformat(),
            tags=tags or []
        )
        self.tasks.append(task)
        self.next_task_id += 1
        self.save_data()
        print(f"✅ Task added: {task.title}")
    
    def complete_task(self, task_id: int):
        """Mark a task as completed"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                self.save_data()
                print(f"🎉 Task completed: {task.title}")
                return
        print(f"❌ Task {task_id} not found")
    
    def list_tasks(self, show_completed: bool = False):
        """List all tasks"""
        if not self.tasks:
            print("📝 No tasks yet! Add some with 'add task'")
            return
        
        print("\n📋 TASKS")
        print("=" * 50)
        
        for task in self.tasks:
            if not show_completed and task.status == TaskStatus.COMPLETED:
                continue
            
            tags_str = f" [{', '.join(task.tags)}]" if task.tags else ""
            print(f"{task.id:2d}. {task.status.value} {task.priority.value} {task.title}{tags_str}")
            if task.description:
                print(f"    📝 {task.description}")
    
    def add_habit(self, name: str, description: str = "", target_days: int = 30):
        """Add a new habit to track"""
        habit = Habit(
            name=name,
            description=description,
            target_days=target_days,
            current_streak=0,
            longest_streak=0,
            completed_dates=[],
            created_at=datetime.now().isoformat()
        )
        self.habits.append(habit)
        self.save_data()
        print(f"🎯 Habit added: {habit.name}")
    
    def complete_habit(self, habit_name: str):
        """Mark habit as completed for today"""
        today = datetime.now().date().isoformat()
        
        for habit in self.habits:
            if habit.name.lower() == habit_name.lower():
                if today in habit.completed_dates:
                    print(f"✨ Already completed {habit.name} today!")
                    return
                
                habit.completed_dates.append(today)
                habit.current_streak += 1
                habit.longest_streak = max(habit.longest_streak, habit.current_streak)
                self.save_data()
                print(f"🔥 {habit.name} completed! Streak: {habit.current_streak} days")
                return
        
        print(f"❌ Habit '{habit_name}' not found")
    
    def show_habits(self):
        """Show all habits with progress"""
        if not self.habits:
            print("🎯 No habits yet! Add some with 'add habit'")
            return
        
        print("\n🎯 HABITS")
        print("=" * 50)
        
        for habit in self.habits:
            progress = min(habit.current_streak / habit.target_days * 100, 100)
            bar_length = 20
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"🔥 {habit.name}")
            print(f"   {bar} {progress:.1f}% ({habit.current_streak}/{habit.target_days} days)")
            print(f"   🏆 Longest streak: {habit.longest_streak} days")
            if habit.description:
                print(f"   📝 {habit.description}")
            print()


def main():
    """Main application loop"""
    tracker = TaskTracker()
    
    print("🚀 Welcome to Personal Task & Habit Tracker!")
    print("Type 'help' for commands or 'quit' to exit")
    
    # Add some sample data if none exists
    if not tracker.tasks and not tracker.habits:
        print("\n🎉 Setting up sample data...")
        tracker.add_task("Learn Python decorators", "Study how decorators work", Priority.HIGH, ["learning", "python"])
        tracker.add_task("Exercise for 30 minutes", "Go for a run or gym", Priority.MEDIUM, ["health"])
        tracker.add_task("Read a book chapter", "Continue reading current book", Priority.LOW, ["learning", "reading"])
        
        tracker.add_habit("Daily coding", "Write code for at least 30 minutes", 30)
        tracker.add_habit("Exercise", "Any form of physical activity", 21)
        tracker.add_habit("Read", "Read for 15 minutes", 14)
    
    while True:
        try:
            command = input("\n💻 > ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Keep being productive!")
                break
            
            elif command == 'help':
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
  
  GitHub:
    gh issues            - List open GitHub issues
    gh issues all        - List all GitHub issues
    gh prs               - List open pull requests
    gh prs all           - List all pull requests
    create issue         - Create a new GitHub issue (interactive)
    create pr            - Create a pull request (interactive)
    sync task <id>       - Convert task to GitHub issue
  
  Other:
    stats                - Show statistics
    help                 - Show this help
    quit                 - Exit the application
                """)
            
            elif command == 'list':
                tracker.list_tasks()
            
            elif command == 'list all':
                tracker.list_tasks(show_completed=True)
            
            elif command == 'add task':
                title = input("Task title: ").strip()
                description = input("Description (optional): ").strip()
                
                print("Priority: 1=Low 🟢, 2=Medium 🟡, 3=High 🔴")
                priority_choice = input("Priority (1-3): ").strip()
                priority_map = {'1': Priority.LOW, '2': Priority.MEDIUM, '3': Priority.HIGH}
                priority = priority_map.get(priority_choice, Priority.MEDIUM)
                
                tags_input = input("Tags (comma-separated, optional): ").strip()
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                
                tracker.add_task(title, description, priority, tags)
            
            elif command.startswith('complete '):
                try:
                    task_id = int(command.split()[1])
                    tracker.complete_task(task_id)
                except (IndexError, ValueError):
                    print("❌ Usage: complete <task_id>")
            
            elif command == 'habits':
                tracker.show_habits()
            
            elif command == 'add habit':
                name = input("Habit name: ").strip()
                description = input("Description (optional): ").strip()
                try:
                    target_days = int(input("Target days (default 30): ").strip() or "30")
                except ValueError:
                    target_days = 30
                
                tracker.add_habit(name, description, target_days)
            
            elif command.startswith('done '):
                habit_name = ' '.join(command.split()[1:])
                tracker.complete_habit(habit_name)
            
            elif command == 'stats':
                total_tasks = len(tracker.tasks)
                completed_tasks = sum(1 for t in tracker.tasks if t.status == TaskStatus.COMPLETED)
                total_habits = len(tracker.habits)
                
                print("\n📊 STATISTICS")
                print("=" * 30)
                print(f"📋 Tasks: {completed_tasks}/{total_tasks} completed")
                print(f"🎯 Habits: {total_habits} being tracked")
                
                if tracker.habits:
                    avg_streak = sum(h.current_streak for h in tracker.habits) / len(tracker.habits)
                    print(f"🔥 Average streak: {avg_streak:.1f} days")
            
            else:
                print("❓ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
