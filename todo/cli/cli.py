#!/usr/bin/python3

"""
cli.py - This module hadles the command lines interface.
"""

import argparse
from ..tasks.tasks_manager import TaskManager
from ..db.database import Database


def cli_main():
    """
    Main fuction
    """
    parser = argparse.ArgumentParser(
        description="Todo CLI App",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help="subcommands",
    )

    # Subcommand for setting up the database
    subparsers.add_parser(
        "setup_db",
        help="Set up database",
    )

    # Subcommands for adding a task
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task",
    )
    add_parser.add_argument(
        "-t",
        "--title",
        required=True,
        help="Title of task",
    )
    add_parser.add_argument(
        "-des",
        "--description",
        help="Description of task",
    )
    add_parser.add_argument(
        "-p",
        "--priority",
        type=int,
        choices=range(1, 6),
        help="Priority of the task (1-5)",
    )
    add_parser.add_argument(
        "--due_date",
        help="Due date of the task (YYYY-MM-DD)",
    )
    # Subcommands for listing tasks
    list_parser = subparsers.add_parser(
        "list",
        help="List tasks",
    )
    list_parser.add_argument(
        "-s",
        "--status",
        choices=["all", "completed", "incomplete"],
        default="all",
        help="Filter tasks by status",
    )

    # Subcommands for updating a task
    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing task",
    )
    update_parser.add_argument(
        "--id",
        required=True,
        type=int,
        help="ID of the task",
    )
    update_parser.add_argument(
        "-t",
        "--title",
        help="New title of the task",
    )
    update_parser.add_argument(
        "-des",
        "--description",
        help="New description of task",
    )
    update_parser.add_argument(
        "-c",
        "--completed",
        action="store_true",
        help="Mark task as completed",
    )
    update_parser.add_argument(
        "-p",
        "--priority",
        type=int,
        choices=range(1, 6),
        help="New priority of the task (1-5)",
    )
    update_parser.add_argument(
        "--due_date",
        help="New date of the task (YYYY-MM-DD)",
    )

    # Subcommand for deleting a task
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task",
    )
    delete_parser.add_argument(
        "--id",
        required=True,
        type=int,
        help="ID of the task to delete",
    )

    args = parser.parse_args()

    if args.command == "setup_db":
        d_base = Database()
        if d_base.table_exists("tasks"):
            print("Table already exists. Skipping setup.")
            return
        error = d_base.create_db_table("data/db_setup.sql")
        if error is not None:
            d_base.close()
            return
        d_base.close()
        print("Database setup complete.")
        return

    task_man = TaskManager()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "add":
        add_task_dictionary = {
            "title": args.title,
            "description": args.description,
            "priority": args.priority,
            "due_date": args.due_date,
        }
        task_man.add_task(**add_task_dictionary)
    elif args.command == "list":
        task_man.list_task(args.status)
    elif args.command == "update":
        update_task_dictionary = {
            "title": args.title,
            "description": args.description,
            "completed": args.completed,
            "priority": args.priority,
            "due_date": args.due_date,
        }
        task_man.update_task(task_id=args.id, **update_task_dictionary)
    elif args.command == "delete":
        task_man.delete_task(args.id)
    else:
        print("\n")
        parser.print_help()
        print("\n")
    task_man.close()
