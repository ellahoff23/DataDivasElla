# DataDivasLena

DataDivasLena is a student-to-project mapper for capstone planning. It helps ECCS organizers assign students to projects using ranked preferences, major eligibility, and team-size constraints.

## Overview

- Student-to-project matching app built for capstone team planning.
- Web interface powered by Streamlit for browser-based access.
- Optimization logic powered by Google OR-Tools CP-SAT.
- Enforces the Nixing Rule, major eligibility, and diversity/monoculture penalties.

## Setup Instructions

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the app:

```bash
python -m streamlit run streamlit_app.py
```

Then open the browser page shown by Streamlit.

## Input Formatting

### Projects
Each project line must use:

```
Project Name,capacity,major1,major2,...
```

Example:

```
Project Apollo,4,CS,CpE,EE
Project Atlas,4,CS,EE
Project Beacon,5,CS,CpE
Project Cypress,4,CpE,EE
```

### Students
Each student line must use:

```
Student Name (major): project1, project2
```

Example:

```
Alice (CS): Project Apollo, Project Atlas, Project Beacon
Ben (CpE): Project Atlas, Project Cypress, Project Apollo
Carmen (EE): Project Beacon, Project Apollo, Project Atlas
```

## Features

- **Nixing Rule**: A project must have either 0 students or 4-6 students.
- **Major eligibility**: Students can only be assigned to projects that accept their major.
- **Diversity / monoculture penalty**: The optimization favors mixed-major teams and penalizes single-major teams.
- **OR-Tools CP-SAT optimizer** for assignment decisions.
- **CSV upload** for projects and student rankings.
- **Downloadable CSV** for final assignments.
- **Clear error handling** for malformed or invalid input.

## How it works

The app parses project and student text input, validates the data, and runs an OR-Tools CP-SAT model to assign students to projects. Project capacity, major eligibility, and team composition are enforced as hard constraints, while student preference ranking and diversity are optimized.

## File layout

- `streamlit_app.py` — Streamlit entry point for the active web application.
- `requirements.txt` — Python dependencies for the app.
- `datadivas/assignment.py` — Core assignment logic and optimization model.
- `datadivas/__init__.py` — Package exports for the datadivas package.
- `tests/` — Unit tests for assignment parsing and validation.
- `README.md` — Human-facing project documentation.
- `ROBOTS.md` — AI-centric project structure and logic documentation.

## Testing

Run unit tests:

```bash
python -m unittest discover -s tests
```

