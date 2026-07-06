# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
=== PawPal+ ===
Oscar, age 28 — 123 Maple St

Pets:
Rex (Dog, Labrador, age 4)
Milo (Cat, Tabby, age 2)

Today's Schedule (Sunday, July 05):
  07:30  Morning walk  [pending]
  12:15  Litter box cleaning  [pending]
  18:00  Dinner  [pending]
```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

The tests live in `tests/test_pawpal.py` and exercise the core scheduling
logic in `pawpal_system.py`:

- **Sorting** — `sort_by_time()` returns tasks in chronological order
  (earliest first), interleaves tasks across different dates purely by clock
  time, is stable for equal times, and leaves the stored schedule unchanged;
  `todays_schedule()` filters to one day and breaks ties by priority.
- **Recurrence** — completing a daily or weekly task auto-schedules its next
  occurrence (next day / next week) as a fresh, incomplete copy with all other
  fields preserved; one-off and unrecognized recurrence values spawn nothing.
- **Conflict detection** — `time_clashes()` flags tasks booked for the exact
  same date and time (across any pet), and `conflicts()` flags *overlapping*
  tasks — including overlaps between non-adjacent tasks and overlaps that cross
  midnight.
- **Filtering & tasks** — `filter_tasks()` narrows by completion status and/or
  pet, plus basic task behavior (completion, duration/end time, and status
  reporting: pending / overdue / done).

Sample test output:

```
$ python -m pytest
============================= test session starts =============================
collected 25 items

tests/test_pawpal.py ......................... [100%]

============================= 25 passed in 0.05s ==============================
```

## 📐 Smarter Scheduling

PawPal+ goes beyond a flat task list with the scheduling logic below. All of it
lives in `pawpal_system.py` and is covered by `tests/test_pawpal.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time(),Scheduler.todays_schedule(today)| Order tasks chronologically |
| Filtering | Owner.filter_tasks(completed=, pet_name=) | By completion status and/or pet |
| Conflict detection | Scheduler.time_clashes(), Scheduler.conflicts(today), Scheduler.clash_warnings()` | Same-time & overlapping tasks |
| Recurring tasks | Task.next_occurrence(), Scheduler.complete_task(task) | Daily / weekly repeats |

### Sorting behavior

- **Scheduler.sort_by_time()** returns all scheduled tasks ordered by due
  time, earliest first. It uses a lambda key that renders each task's
  due_time as an "HH:MM" string; because those are zero-padded,
  lexicographic ordering matches chronological ordering. It returns a new list
  and leaves the scheduler's stored order untouched.
- **Scheduler.todays_schedule(today)** filters to a single day and sorts by
  due time, then by priority (higher first) as a tiebreaker.

### Filtering behavior

- **Owner.filter_tasks(completed=, pet_name=)** returns tasks across all
  of the owner's pets, narrowed by the criteria you pass. Use completed=True
  or completed=False to keep only done or pending tasks, and pet_name to
  keep only one pet's tasks. Either criterion left as None is ignored, so
  calling it with no arguments returns every task.

### Conflict detection logic

- **Scheduler.time_clashes()** groups scheduled tasks by (date, due_time) and
  returns any group with two or more tasks — i.e. tasks booked for the exact
  same moment, whether they belong to the same pet or different pets. Runs in a
  single O(n) pass.
- **Scheduler.conflicts(today)** catches *overlapping* tasks on a given day: it
  pairs consecutive tasks and flags any where the earlier task is still running
  (its Task.end_time(), derived from duration_minutes) when the next is due.
- **Scheduler.clash_warnings()** is a lightweight wrapper that turns each
  same-time clash into a readable warning string and never raises — on any
  unexpected error it returns an explanatory warning instead of crashing, so a
  UI or the CLI can print the result directly.

### Recurring task logic

- Each Task carries a recurrence field ("none", "daily", or "weekly").
- **Task.next_occurrence()** builds a fresh, incomplete copy of a recurring
  task with the date advanced by one day or one week (all other fields
  preserved), or returns None for a one-off task.
- **Scheduler.complete_task(task)** marks a task complete and, if it recurs,
  automatically creates its next occurrence via next_occurrence() and
  registers it on the scheduler so it appears in future schedules.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
