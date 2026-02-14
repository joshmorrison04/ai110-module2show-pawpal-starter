from datetime import date

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")  # or a default name

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(availability=120)  # pick a default

if "pets" not in st.session_state:
    st.session_state.pets = {}


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.session_state.owner.name = owner_name

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add pet"):
    if pet_name.strip():
        pet = st.session_state.pets.get(pet_name)
        if not pet:
            pet = Pet(name=pet_name)
            st.session_state.owner.add_pet(pet)
            st.session_state.pets[pet_name] = pet
        st.session_state.scheduler.pets = list(st.session_state.pets.values())
    else:
        st.warning("Please enter a pet name before adding.")

if st.button("Add task"):
    if not pet_name.strip():
        st.warning("Please enter a pet name before adding a task.")
    else:
        pet = st.session_state.pets.get(pet_name)
        if not pet:
            pet = Pet(name=pet_name)
            st.session_state.owner.add_pet(pet)
            st.session_state.pets[pet_name] = pet
        priority_map = {"low": 1, "medium": 2, "high": 3}
        task = Task(
            name=task_title,
            description=f"{species} care task",
            duration=int(duration),
            priority=priority_map[priority],
            status=Task.STATUS_PENDING,
        )
        pet.add_task(task)
        st.session_state.scheduler.pets = list(st.session_state.pets.values())
        st.session_state.tasks.append(
            {
                "pet": pet.name,
                "title": task_title,
                "duration_minutes": int(duration),
                "priority": priority,
            }
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a sorted, filtered schedule using your Scheduler logic.")

schedule_col1, schedule_col2, schedule_col3 = st.columns(3)
with schedule_col1:
    schedule_date = st.date_input("Schedule date", value=date.today())
with schedule_col2:
    pet_filter_options = ["All pets"] + [pet.name for pet in st.session_state.scheduler.pets]
    selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options)
with schedule_col3:
    status_filter = st.selectbox(
        "Filter by status",
        ["All", Task.STATUS_PENDING, Task.STATUS_IN_PROGRESS, Task.STATUS_COMPLETED],
    )

if st.button("Generate schedule"):
    plan = st.session_state.scheduler.generate_daily_plan(
        pet_name=None if selected_pet_filter == "All pets" else selected_pet_filter,
        status=None if status_filter == "All" else status_filter,
        on_date=schedule_date,
    )
    if not plan:
        st.info("No schedulable tasks found. Try adjusting the filters or adding tasks.")
    else:
        total_minutes = sum(task.duration for _, task in plan)
        st.success(
            f"Generated {len(plan)} scheduled task(s) totaling {total_minutes} minutes."
        )

        st.write("Scheduled tasks:")
        st.table(
            [
                {
                    "pet": pet.name,
                    "task": task.name,
                    "duration_minutes": task.duration,
                    "priority": task.priority,
                    "due_time": "unscheduled"
                    if task.due_time is None
                    else f"{task.due_time // 60:02d}:{task.due_time % 60:02d}",
                    "status": task.status,
                }
                for pet, task in plan
            ]
        )

        same_time_conflicts = st.session_state.scheduler.same_time_conflicts
        overlap_conflicts = st.session_state.scheduler.detect_conflicts(plan)

        if same_time_conflicts:
            st.warning("Some tasks share the same due time.")
            st.table(
                [
                    {
                        "pet": conflict[0].name,
                        "task": conflict[1].name,
                        "conflicts_with_pet": conflict[2].name,
                        "conflicts_with_task": conflict[3].name,
                        "due_time": "unscheduled"
                        if conflict[1].due_time is None
                        else f"{conflict[1].due_time // 60:02d}:{conflict[1].due_time % 60:02d}",
                    }
                    for conflict in same_time_conflicts
                ]
            )

        if overlap_conflicts:
            st.warning("Some tasks overlap based on duration and start time.")
            st.table(
                [
                    {
                        "pet": conflict[0].name,
                        "task": conflict[1].name,
                        "overlaps_with_pet": conflict[2].name,
                        "overlaps_with_task": conflict[3].name,
                        "start_time": "unscheduled"
                        if conflict[1].due_time is None
                        else f"{conflict[1].due_time // 60:02d}:{conflict[1].due_time % 60:02d}",
                    }
                    for conflict in overlap_conflicts
                ]
            )
