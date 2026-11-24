# Seventh Contact Session – Python and PostgreSQL

This project contains the two tasks for the seventh contact session:

1. Implement a Fibonacci series generator using Python's `yield`.
2. Build a command-line To-Do List application using Python and PostgreSQL.

## Features

### Fibonacci generator
- Uses a Python generator function and `yield`.
- Generates the first `n` Fibonacci numbers.
- Validates the number entered by the user.

### To-Do List
- Add a task with a title and optional description.
- View all saved tasks.
- Mark a task as completed.
- Update a task's title or description.
- Delete a task.
- Store tasks persistently in PostgreSQL.

## Project structure

```text
seventh_contact_session/
├── database.py
├── fibonacci.py
├── todo.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- PostgreSQL installed and running
- pip

## Setup instructions

### 1. Clone the repository

```bash
git clone https://github.com/Damiemmy/seventh-contact-session.git
cd seventh_contact_session
```

### 2. Create and activate a virtual environment

Linux/macOS/WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a PostgreSQL database

Open the PostgreSQL shell (`psql`) and run:

```sql
CREATE DATABASE todo_database;
```

### 5. Configure environment variables

Copy `.env.example` to `.env`:

Linux/macOS/WSL:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and enter your own PostgreSQL username and password. The example uses individual settings. Alternatively, you can set a `DATABASE_URL` connection string and leave the individual settings unused.

**Do not commit your `.env` file or publish your database password.**

### 6. Run the Fibonacci generator

```bash
python fibonacci.py
```

Enter how many Fibonacci numbers you want to generate.

### 7. Run the To-Do List application

```bash
python todo.py
```

The application creates the `tasks` table automatically the first time it connects successfully. Use the displayed menu to manage your tasks.

## How the Fibonacci generator works

A generator function uses `yield` to return one value at a time instead of building and returning the entire sequence at once.

The next Fibonacci number is calculated by adding the previous two numbers:

```text
0, 1, 1, 2, 3, 5, 8, 13, ...
```

## Database table

The application creates a `tasks` table with these columns:

| Column | Purpose |
|---|---|
| `id` | Unique task identifier |
| `title` | Task title |
| `description` | Optional task details |
| `is_completed` | Whether the task is completed |
| `created_at` | Date and time the task was created |

## Database safety

The application uses parameterized SQL queries to pass user input to PostgreSQL safely. Database credentials are loaded from environment variables rather than being hard-coded in the source files.

## Assignment summary

This project demonstrates Python generator functions, PostgreSQL connectivity, SQL table creation, parameterized queries, and CRUD operations from a Python command-line application.
