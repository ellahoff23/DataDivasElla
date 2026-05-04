# DataDivasLena

DataDivasLena is a student-to-project mapper for capstone planning. It helps ECCS organizers assign students to projects using ranked preferences, major eligibility, and team-size constraints.

## Overview

- Student-to-project matching tool for capstone team formation.
- Browser-based interface built with Streamlit.
- Optimization engine uses Google OR-Tools CP-SAT.
- Supports flexible CSV upload for projects and student rankings.
- Enforces the Nixing Rule and major eligibility, and encourages mixed-major teams.

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

- **Nixing Rule**: Each project is either inactive (0 students) or active with 4-6 students.
- **Major eligibility**: Students can only be assigned to projects that accept their major.
- **Diversity penalty**: The solver favors mixed-major teams over mono-major teams.
- **Flexible CSV parsing** for both project and student files.
- **Downloadable CSV export** of final assignments.
- **Admin diagnostics** available from the Streamlit sidebar when admin access is enabled.

## How it works

The app parses project and student input, validates the data, and runs a CP-SAT optimization model to assign students to projects. Project capacity, eligibility, and team composition are hard constraints, while student preference ranking and diversity are optimized.

## File layout

- `streamlit_app.py` — Streamlit web application entry point.
- `requirements.txt` — Python dependencies for the app.
- `datadivas/assignment.py` — Core assignment logic, parsing, validation, and optimization.
- `datadivas/__init__.py` — Package exports for the datadivas package.
- `tests/` — Unit tests covering parsing, validation, and assignment behavior.
- `README.md` — Human-facing project documentation.
- `ROBOTS.md` — AI-facing description of project structure and behavior.

## Testing

Run the unit tests:

```bash
python -m unittest discover -s tests
```

