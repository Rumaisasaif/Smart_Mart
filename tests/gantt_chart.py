import plotly.express as px
from datetime import datetime, timedelta

# Task data as list of tuples for variation
task_list = [
    # (Task name, Start date, Duration in days, Phase)
    ("Set up Trello board", "2025-05-22", 1, "Planning"),
    ("Create Gantt chart", "2025-05-23", 1, "Planning"),
    ("Draw UML diagrams", "2025-05-24", 3, "Planning"),
    ("Justify Architecture", "2025-05-27", 1, "Planning"),

    ("Login UI design", "2025-05-28", 1, "GUI Design"),
    ("Admin panel UI", "2025-05-29", 2, "GUI Design"),
    ("Cashier panel UI", "2025-05-31", 2, "GUI Design"),

    ("product_model.py", "2025-06-02", 1, "Implementation"),
    ("user_model.py", "2025-06-03", 1, "Implementation"),
    ("bill_model.py", "2025-06-04", 1, "Implementation"),
    ("main_controller.py", "2025-06-05", 2, "Implementation"),
    ("GUI integration", "2025-06-07", 2, "Implementation"),

    ("Handle Exceptions", "2025-06-09", 1, "Testing"),
    ("Unit Tests (PyTest)", "2025-06-10", 2, "Testing"),

    (".exe Packaging", "2025-06-12", 1, "Deployment"),
    ("Push to GitHub", "2025-06-13", 1, "Deployment"),
    ("GitHub Release", "2025-06-14", 1, "Deployment"),
    ("Peer Review", "2025-06-15", 1, "Deployment"),
]

# Convert tasks to Gantt-ready dicts
timeline_data = []
for task, start_str, days, category in task_list:
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = start_date + timedelta(days=days)
    timeline_data.append({
        "Task Name": task,
        "Start Date": start_date,
        "End Date": end_date,
        "Category": category
    })

# Create Gantt chart
fig = px.timeline(
    timeline_data,
    x_start="Start Date",
    x_end="End Date",
    y="Task Name",
    color="Category",
    title="SmartMart Project Timeline",
    height=750
)

fig.update_yaxes(autorange="reversed")
fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
fig.show()
