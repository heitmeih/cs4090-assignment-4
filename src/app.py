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
    complete_all_tasks,
    filter_tasks_by_category,
    filter_tasks_by_priority,
    generate_unique_id,
    load_tasks,
    save_tasks,
    sort_tasks,
)
from tests import html, test_advanced, test_basic

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

        label = f"**Results for `{test_name}`:**"
        message = [
            f"{len(passed)} tests passed!\n{len(failed)} tests failed!",
        ]

        if failed:
            lines = ["Failing tests:\n"]
            for node in failed:
                lines.append(f"- `{node}`")
            message.append("\n".join(lines))

            status.update(label=label, state="error", expanded=True)
        else:
            status.update(label=label, state="complete", expanded=True)

        st.markdown("\n\n".join(message))


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
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"]
            + list(set([task["category"] for task in tasks if "category" in task])),
        )
        show_completed = st.checkbox("Show Completed Tasks")
    with col2:
        filter_priority = st.selectbox(
            "Filter by Priority", ["All", "High", "Medium", "Low"]
        )

    with col3:
        sort_by = st.selectbox(
            "Sort By",
            [None] + list({key for task in tasks for key in task.keys()}),
            placeholder="Choose an Option",
        )
        ascending = st.checkbox("Sort Ascending", value=True)

    if st.button(
        "Complete All Tasks",
        disabled=all(task.get("completed", False) for task in tasks),
    ):
        tasks = complete_all_tasks(tasks)
        save_tasks(tasks)
        st.rerun()

    # Apply filters
    filtered_tasks = [task.copy() for task in tasks]
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    filtered_tasks = sort_tasks(filtered_tasks, sort_by, ascending)

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task.get("completed", False):
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task.get("description", "No Description"))
            st.caption(
                f"Due: {task.get('due_date', 'N/A')} | Priority: {task.get('priority', 'N/A')} | Category: {task.get('category', 'N/A')}"
            )
        with col2:
            if st.button(
                "Complete" if not task.get("completed", False) else "Undo",
                key=f"complete_{task.get('id', None)}",
            ):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task.get('id', None)}"):
                tasks = [
                    t for t in tasks if task.get("id", None) != task.get("id", None)
                ]
                save_tasks(tasks)
                st.rerun()

    st.header("Tests")

    if st.button("Run Basic Tests"):
        run_tests(test_basic.run_tests, "Basic Unit Tests")

    if st.button("Run Advanced Tests"):
        run_tests(test_advanced.run_tests, "Advanced Tests")

    if st.button("Generate HTML Report"):

        with st.status("Running Tests...") as status:
            report_content = html.generate_html_report()
            if report_content:
                status.update(label="Report Created!", state="complete", expanded=True)
                st.download_button(
                    "Download HTML Report",
                    data=report_content,
                    file_name="report.html",
                    mime="text/html",
                    icon=":material/download:",
                )
            else:
                status.update(label="Report creation failed!", state="error")

    if st.button("Get Test Coverage"):
        with st.status("Running Tests...") as status:
            report = code_coverage.get_code_coverage()

            message = "\n\n".join(
                [
                    "**NOTE:** Coverage for app.py is not accurate when coverage is run through the streamlit app. All other stats are correct."
                ]
                + [f"`{name}: {coverage:.2f}%`" for name, coverage in report]
            )

            status.update(
                label="Coverage Calculation Complete", state="complete", expanded=True
            )
            st.markdown(message)


if __name__ == "__main__":
    main()
