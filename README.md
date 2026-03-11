# Habit Tracker Desktop App

This is a small, visual desktop program built with **Python** and **PyQt6**.  
It recreates a weekly habit progress tracker with:

- Week navigation (previous/next week)
- A progress summary (e.g. `0/35 completed (0%)`)
- A table of habits vs days, with checkbox cells
- Highlighting for the current day column

## Setup

1. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   python main.py
   ```

## Project Structure

- `main.py` – Application entry point.
- `ui/main_window.py` – Main window and layout composition.
- `ui/habit_table.py` – Habit table widget with checkboxes and highlighting.
- `models/habit_data.py` – Simple data structures and date/week helpers.

All modules are intentionally kept small and focused to keep the codebase easy to navigate.

