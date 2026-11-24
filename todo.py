import psycopg

from database import get_connection, initialize_database


def add_task():
    title = input("Task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    description = input("Description (optional): ").strip()

    query = """
        INSERT INTO tasks (title, description)
        VALUES (%s, %s)
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (title, description or None))
            task_id = cursor.fetchone()["id"]

    print(f"Task added successfully. Task ID: {task_id}")


def view_tasks():
    query = """
        SELECT id, title, description, is_completed, created_at
        FROM tasks
        ORDER BY created_at DESC, id DESC;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            tasks = cursor.fetchall()

    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n" + "=" * 76)
    print(f"{'ID':<5} {'STATUS':<12} {'TITLE':<30} {'CREATED AT'}")
    print("-" * 76)

    for task in tasks:
        status = "Completed" if task["is_completed"] else "Pending"
        created = task["created_at"].strftime("%Y-%m-%d %H:%M")
        print(f"{task['id']:<5} {status:<12} {task['title'][:28]:<30} {created}")
        if task["description"]:
            print(f"      Description: {task['description']}")

    print("=" * 76)


def mark_task_completed():
    task_id = get_task_id()
    if task_id is None:
        return

    query = """
        UPDATE tasks
        SET is_completed = TRUE
        WHERE id = %s
        RETURNING id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (task_id,))
            updated = cursor.fetchone()

    print("Task marked as completed." if updated else "Task not found.")


def update_task():
    task_id = get_task_id()
    if task_id is None:
        return

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT title, description FROM tasks WHERE id = %s;",
                (task_id,),
            )
            task = cursor.fetchone()

            if not task:
                print("Task not found.")
                return

            print("Press Enter to keep the current value.")
            new_title = input(f"New title [{task['title']}]: ").strip()
            new_description = input(
                f"New description [{task['description'] or ''}]: "
            ).strip()

            title = new_title or task["title"]
            description = (
                new_description if new_description else task["description"]
            )

            cursor.execute(
                """
                UPDATE tasks
                SET title = %s, description = %s
                WHERE id = %s;
                """,
                (title, description, task_id),
            )

    print("Task updated successfully.")


def delete_task():
    task_id = get_task_id()
    if task_id is None:
        return

    confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ")
    if confirm.strip().lower() != "y":
        print("Deletion cancelled.")
        return

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id;",
                (task_id,),
            )
            deleted = cursor.fetchone()

    print("Task deleted successfully." if deleted else "Task not found.")


def get_task_id():
    try:
        task_id = int(input("Enter task ID: "))
        if task_id <= 0:
            raise ValueError
        return task_id
    except ValueError:
        print("Please enter a valid positive task ID.")
        return None


def display_menu():
    print(
        """
========== PYTHON TO-DO LIST ==========
1. Add a task
2. View all tasks
3. Mark a task as completed
4. Update a task
5. Delete a task
0. Exit
=======================================
"""
    )


def main():
    try:
        initialize_database()
        print("Connected to PostgreSQL. Tasks table is ready.")

        while True:
            display_menu()
            choice = input("Choose an option: ").strip()

            actions = {
                "1": add_task,
                "2": view_tasks,
                "3": mark_task_completed,
                "4": update_task,
                "5": delete_task,
            }

            if choice == "0":
                print("Goodbye!")
                break

            action = actions.get(choice)
            if action:
                try:
                    action()
                except Exception as error:
                    print(f"Could not complete that operation: {error}")
            else:
                print("Invalid option. Choose a number from 0 to 5.")

    except (psycopg.Error, RuntimeError) as error:
        print(f"Database setup/connection error: {error}")
    except KeyboardInterrupt:
        print("\nApplication closed.")


if __name__ == "__main__":
    main()
