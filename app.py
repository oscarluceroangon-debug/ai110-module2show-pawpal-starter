from datetime import date, datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

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

st.subheader("Owner & Pets")

# --- Session vault ---------------------------------------------------------
# Create the Owner and Scheduler ONCE and store them in st.session_state.
# The guards below check the "vault" first so we reuse the existing objects
# on every rerun instead of wiping out pets and tasks each interaction.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", age=28, address="123 Maple St")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# Keep the stored owner in sync with the name field.
owner.name = st.text_input("Owner name", value=owner.name)

st.markdown("### Add a pet")
pcol1, pcol2, pcol3 = st.columns(3)
with pcol1:
    pet_name = st.text_input("Pet name", value="Mochi")
with pcol2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with pcol3:
    pet_age = st.number_input("Age", min_value=0, max_value=40, value=2)

if st.button("Add pet"):
    if any(p.name == pet_name for p in owner.pets):
        st.warning(f"{pet_name} is already one of {owner.name}'s pets.")
    else:
        owner.add_pet(Pet(name=pet_name, animal_type=species, breed="Unknown", age=int(pet_age)))
        st.success(f"Added {pet_name} to {owner.name}.")

if owner.pets:
    st.write(f"**{owner.name}'s pets:**")
    st.table(
        [
            {"name": p.name, "species": p.animal_type, "age": p.age, "tasks": len(p.tasks)}
            for p in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add Tasks")
if not owner.pets:
    st.info("Add a pet first, then you can assign tasks to it.")
else:
    tcol1, tcol2, tcol3, tcol4, tcol5 = st.columns(5)
    with tcol1:
        which_pet = st.selectbox("Pet", [p.name for p in owner.pets])
    with tcol2:
        task_title = st.text_input("Task title", value="Morning walk")
    with tcol3:
        due = st.time_input("Due time", value=time(7, 30))
    with tcol4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with tcol5:
        duration = st.number_input("Minutes", min_value=1, max_value=480, value=15)

    if st.button("Add task"):
        priority_map = {"low": 1, "medium": 2, "high": 3}
        target = next(p for p in owner.pets if p.name == which_pet)
        task = Task(
            description=task_title,
            date=date.today(),
            due_time=due,
            priority=priority_map[priority],
            preference=priority,
            duration_minutes=int(duration),
        )
        target.add_task(task)  # persists on the Pet inside the vaulted Owner
        scheduler.create_schedule(task)
        st.success(f"Added '{task_title}' for {which_pet}.")

st.divider()

st.subheader("Build Schedule")
st.caption("Calls Scheduler.todays_schedule() on the tasks stored this session.")

if st.button("Generate schedule"):
    today = date.today()
    now = datetime.now()
    todays = scheduler.todays_schedule(today)
    if not todays:
        st.info("No tasks scheduled for today yet. Add some above.")
    else:
        st.write(f"**Today's Schedule ({today:%A, %B %d})**")
        st.table(
            [
                {
                    "time": f"{t.due_time:%H:%M}–{t.end_time():%H:%M}",
                    "task": t.description,
                    "priority": t.preference,
                    "status": t.status(now),
                }
                for t in todays
            ]
        )

        conflicts = scheduler.conflicts(today)
        if conflicts:
            st.warning("⚠️ Overlapping tasks:")
            for earlier, later in conflicts:
                st.write(
                    f"- **{earlier.description}** (ends {earlier.end_time():%H:%M}) "
                    f"overlaps **{later.description}** (starts {later.due_time:%H:%M})"
                )
