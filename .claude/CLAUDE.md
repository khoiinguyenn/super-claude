# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Personal Task & Habit Tracker** - A fun, interactive CLI application designed to demonstrate Claude's capabilities while being genuinely useful. Perfect for quick iteration and testing various Python concepts.

### Features
- 📋 Task management with priorities and tags
- 🎯 Habit tracking with streak counters
- 💾 Data persistence using JSON files
- 🎨 Interactive CLI with emojis and progress bars
- 📊 Statistics and insights
- 🔄 Real-time data updates

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv (recommended)
uv sync

# Alternative: Install with pip
pip install -e .
```

### Running the Application

**Web Application (Recommended):**
```bash
# Start the web server
python app.py

# Or using uv
uv run python app.py

# Then open http://localhost:5001 in your browser
```

**CLI Application:**
```bash
# Run the interactive tracker
python main.py

# Or using uv
uv run python main.py
```

### Development Tools
```bash
# Install development dependencies
uv add --dev pytest black flake8 mypy

# Format code
black main.py

# Type checking
mypy main.py

# Linting
flake8 main.py

# Run tests (when added)
pytest
pytest -v  # verbose output
pytest -k "test_task"  # run specific tests
```

### Quick Testing & Iteration
```bash
# Test the app quickly
python main.py
# Then try: help, list, add task, habits, stats, quit

# Reset data for fresh testing
rm tracker_data.json && python main.py
```

## Architecture

### Project Structure
- **`app.py`**: Flask web application with modern UI (230+ lines)
- **`main.py`**: Complete CLI application (320+ lines)
- **`templates/`**: HTML templates with Bootstrap styling
  - `base.html`: Base template with navigation and styling
  - `index.html`: Dashboard with overview and quick actions
  - `tasks.html`: Task management with modals and forms
  - `habits.html`: Habit tracking with progress bars
  - `stats.html`: Statistics and analytics page
- **`demo.py`**: Non-interactive demo script
- **`interactive_demo.py`**: Simulated interactive session
- **Data Files**: Auto-generated JSON persistence
  - `web_tracker_data.json`: Web app data
  - `tracker_data.json`: CLI app data
- **`pyproject.toml`**: Project configuration and dependencies
- **`uv.lock`**: Dependency lock file for reproducible builds

### Core Components

#### Data Models
- **`Task`**: Dataclass with id, title, description, priority, status, timestamps, tags
- **`Habit`**: Dataclass with name, description, target_days, streaks, completion dates
- **`Priority`**: Enum (LOW 🟢, MEDIUM 🟡, HIGH 🔴)
- **`TaskStatus`**: Enum (PENDING ⏳, IN_PROGRESS 🔄, COMPLETED ✅, CANCELLED ❌)

#### Main Class
- **`TaskTracker`**: Central class managing all data operations
  - JSON persistence (save/load)
  - Task CRUD operations
  - Habit tracking and streak calculation
  - Interactive CLI loop

#### Key Methods to Understand
- `save_data()` / `load_data()`: JSON serialization with enum handling
- `add_task()` / `complete_task()`: Task lifecycle management
- `add_habit()` / `complete_habit()`: Habit tracking with streak logic
- `main()`: Interactive command loop with error handling

### Python Concepts Demonstrated
- **Dataclasses**: Clean data modeling with `@dataclass`
- **Enums**: Type-safe constants with emoji values
- **Type Hints**: Full typing with `List`, `Optional`, `Dict`
- **JSON Persistence**: Serialization with custom enum handling
- **CLI Interaction**: Input parsing and user-friendly interface
- **Error Handling**: Graceful exception management
- **Date/Time**: ISO format timestamps and date comparisons
- **List Comprehensions**: Efficient data filtering and transformation

## Common Development Tasks

### Adding New Features
```python
# Example: Add task editing functionality
def edit_task(self, task_id: int, **kwargs):
    for task in self.tasks:
        if task.id == task_id:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.save_data()
            return
```

### Testing New Features
1. Add sample data generation in `main()`
2. Test interactively with the CLI
3. Check JSON persistence in `tracker_data.json`
4. Verify data loads correctly after restart

### Data Model Extensions
- Add new fields to `Task` or `Habit` dataclasses
- Update `save_data()` / `load_data()` if needed
- Consider migration logic for existing data

### CLI Command Extensions
- Add new command patterns in the main loop
- Follow existing patterns for user input and validation
- Include help text updates

## Quick Iteration Tips

### Fast Development Cycle
1. **Make changes** to `main.py`
2. **Test immediately** with `python main.py`
3. **Use sample data** automatically generated on first run
4. **Reset data** with `rm tracker_data.json` for clean testing
5. **Check persistence** by restarting the app

### Common Enhancement Ideas
- Export data to CSV/Excel
- Add task due dates and reminders
- Implement task categories or projects
- Add habit visualization (charts/graphs)
- Create a web interface with Flask
- Add data import/export features
- Implement user authentication
- Add notifications or scheduling

### Debugging Tips
- Data persists in `tracker_data.json` - inspect it directly
- All errors are caught and displayed with ❌ emoji
- Use `print()` statements for quick debugging
- Check enum serialization if JSON errors occur

This project is designed for experimentation - feel free to break things and rebuild!