import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tests import code_coverage

# need to monitor coverage during imports
code_coverage.cov.start()

from tasks import (
    DATE_FORMAT,
    TIME_FORMAT,
    filter_tasks_by_category,
    filter_tasks_by_priority,
    generate_unique_id,
    load_tasks,
    save_tasks,
)
from tests import test_basic

code_coverage.cov.stop()


def run_tests(run_func, test_name="Test"):
    with st.status("Running tests...", state="running") as status:
        reports = run_func()

        passed = []
        failed = []

        for nodeid, test_passed in reports:
            if test_passed:
                passed.append(nodeid)
            else:
                failed.append(nodeid)

        message = "\n\n".join(
            [
                f"**Results for `{test_name}`:**",
                f"{len(passed)} tests passed!",
                f"{len(failed)} tests failed!",
            ]
        )

        if failed:
            lines = ["Failing tests:\n"]
            for node in failed:
                lines.append(f"- {node}")

            error_report = "\n".join(lines)

            status.update(label=f"{message}\n\n{error_report}", state="error")
        else:
            status.update(label=message, state="complete")


def main():
    st.title("To-Do Application")

    # Load existing tasks
    tasks = load_tasks()

    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")

    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox(
            "Category", ["Work", "Personal", "School", "Other"]
        )
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime(DATE_FORMAT),
                "completed": False,
                "created_at": datetime.now().strftime(TIME_FORMAT),
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")

    # Main area to display tasks
    st.header("Your Tasks")

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"]
            + list(set([task["category"] for task in tasks if "category" in task])),
        )
    with col2:
        filter_priority = st.selectbox(
            "Filter by Priority", ["All", "High", "Medium", "Low"]
        )

    show_completed = st.checkbox("Show Completed Tasks")

    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(
                f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}"
            )
        with col2:
            if st.button(
                "Complete" if not task["completed"] else "Undo",
                key=f"complete_{task['id']}",
            ):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    st.header("Tests")

    if st.button("Run Basic Tests"):
        run_tests(test_basic.run_tests, "Basic Unit Tests")

    if st.button("Get Test Coverage"):
        with st.status("Running Tests...") as status:
            report = code_coverage.get_code_coverage()

            message = "\n\n".join(
                [
                    "**NOTE:** Coverage for app.py is not accurate when coverage is run through the streamlit app. All other stats are correct."
                ]
                + [f"`{name}: {coverage:.2f}%`" for name, coverage in report]
            )

            status.update(label=message, state="complete")


if __name__ == "__main__":
    main()
