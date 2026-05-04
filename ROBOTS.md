# ROBOTS

## Project Structure

- Root folder:
  - `streamlit_app.py` — active Streamlit web application entry point.
  - `requirements.txt` — dependency list for the web app.
  - `README.md` — human-facing project overview and usage instructions.
  - `ROBOTS.md` — AI-facing project description and logic flow.
- `datadivas/` package:
  - `assignment.py` — core parsing, validation, scoring, and optimization logic.
  - `__init__.py` — package exports for importing from `datadivas`.
- `tests/` folder:
  - Contains unit tests for parsing, validation, assignment constraints, and performance.

## Logic Flow

- `streamlit_app.py` is the application entry point for the web app.
- It imports validation and optimization functions from `datadivas/assignment.py`.
- The Streamlit app collects project and student input, optionally loads CSV data, and parses it into Python dictionaries.
- The app calls `assign_students_to_projects()` to run the OR-Tools CP-SAT solver.
- Results are displayed in tables and provided as downloadable CSV.
- An admin diagnostics panel can run the test suite and surface pass/fail metrics.

## Technical Stack

- Python
- Streamlit for the web UI
- pandas for CSV parsing and input handling
- Google OR-Tools CP-SAT solver for the optimization model
- Standard library `csv`, `io`, and `re` for file export and diagnostics parsing

## Optimization Summary

- Uses a CP-SAT solver to minimize overall student unhappiness.
- Enforces hard constraints:
  - project capacity limits
  - major eligibility
  - Nixing Rule: projects must have 0 or 4-6 students
- Uses soft penalties for preference rankings and team composition.
- Builds project composition summaries and assignment quality metrics for reporting.
