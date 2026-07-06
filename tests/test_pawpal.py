"""Tests for the PawPal+ system classes."""

from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    """Calling mark_complete() changes the task's status to complete."""
    task = Task("Morning walk", date(2026, 7, 5), time(7, 30))
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_task_addition():
    """Adding a task to a Pet increases that pet's task count."""
    pet = Pet("Rex", "Dog", "Labrador", 4)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Dinner", date(2026, 7, 5), time(18, 0)))
    assert len(pet.tasks) == 1


def test_end_time_adds_duration():
    """end_time() advances the due time by the task's duration."""
    task = Task("Walk", date(2026, 7, 5), time(7, 30), duration_minutes=45)
    assert task.end_time() == time(8, 15)


def test_status_reports_overdue_and_pending():
    """A past, incomplete task is overdue; a future one is pending; done wins."""
    day = date(2026, 7, 5)
    now = datetime(2026, 7, 5, 12, 0)

    overdue = Task("Morning walk", day, time(7, 30))
    pending = Task("Dinner", day, time(18, 0))
    done = Task("Litter box", day, time(7, 0), is_complete=True)

    assert overdue.status(now) == "overdue"
    assert pending.status(now) == "pending"
    assert done.status(now) == "done"


def test_filter_tasks_by_completion_and_pet():
    """filter_tasks() narrows by completion status, pet name, or both."""
    day = date(2026, 7, 5)
    rex = Pet("Rex", "Dog", "Labrador", 4)
    milo = Pet("Milo", "Cat", "Tabby", 2)
    walk = Task("Walk", day, time(7, 30))
    dinner = Task("Dinner", day, time(18, 0), is_complete=True)
    litter = Task("Litter box", day, time(12, 15))
    rex.add_task(walk)
    rex.add_task(dinner)
    milo.add_task(litter)
    owner = Owner("Oscar", 28, "123 Maple St", pets=[rex, milo])

    # No criteria -> everything.
    assert owner.filter_tasks() == [walk, dinner, litter]
    # By completion status.
    assert owner.filter_tasks(completed=True) == [dinner]
    assert owner.filter_tasks(completed=False) == [walk, litter]
    # By pet name.
    assert owner.filter_tasks(pet_name="Rex") == [walk, dinner]
    # Both together.
    assert owner.filter_tasks(completed=False, pet_name="Rex") == [walk]


def test_sort_by_time_orders_earliest_first():
    """sort_by_time() returns tasks ordered by their HH:MM due time."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    dinner = Task("Dinner", day, time(18, 0))
    walk = Task("Walk", day, time(7, 30))
    litter = Task("Litter box", day, time(12, 15))
    for t in (dinner, walk, litter):
        scheduler.create_schedule(t)

    assert scheduler.sort_by_time() == [walk, litter, dinner]


def test_complete_task_reschedules_recurring():
    """Completing a daily/weekly task auto-schedules the next occurrence."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    walk = Task("Walk", day, time(7, 30), recurrence="daily")
    bath = Task("Bath", day, time(10, 0), recurrence="weekly")
    scheduler.create_schedule(walk)
    scheduler.create_schedule(bath)

    next_walk = scheduler.complete_task(walk)
    next_bath = scheduler.complete_task(bath)

    # Original tasks are now complete...
    assert walk.is_complete is True
    assert bath.is_complete is True
    # ...and fresh, incomplete instances exist on the next occurrence.
    assert next_walk.date == date(2026, 7, 6) and next_walk.is_complete is False
    assert next_bath.date == date(2026, 7, 12) and next_bath.is_complete is False
    # Other fields carry over.
    assert next_walk.description == "Walk" and next_walk.due_time == time(7, 30)
    # Both new instances are registered on the scheduler.
    assert next_walk in scheduler.scheduled_tasks
    assert next_bath in scheduler.scheduled_tasks


def test_complete_task_ignores_one_off():
    """A non-recurring task completes without spawning a new instance."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    vet = Task("Vet visit", day, time(9, 0))  # recurrence defaults to "none"
    scheduler.create_schedule(vet)

    result = scheduler.complete_task(vet)

    assert result is None
    assert vet.is_complete is True
    assert scheduler.scheduled_tasks == [vet]


def test_time_clashes_groups_same_time_tasks():
    """time_clashes() groups tasks sharing a date and time, across any pet."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    walk = Task("Walk Rex", day, time(7, 30))
    feed = Task("Feed Milo", day, time(7, 30))  # same time, different pet
    dinner = Task("Dinner", day, time(18, 0))  # no clash
    next_day = Task("Walk Rex", date(2026, 7, 6), time(7, 30))  # same time, other day
    for t in (walk, feed, dinner, next_day):
        scheduler.create_schedule(t)

    clashes = scheduler.time_clashes()

    # Only the two 7:30 tasks on the same day clash.
    assert clashes == [[walk, feed]]


def test_clash_warnings_returns_message_not_exception():
    """clash_warnings() returns a readable warning string for a same-time clash."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    scheduler.create_schedule(Task("Walk Rex", day, time(7, 30)))
    scheduler.create_schedule(Task("Feed Milo", day, time(7, 30)))

    warnings = scheduler.clash_warnings()

    assert len(warnings) == 1
    assert "Walk Rex" in warnings[0] and "Feed Milo" in warnings[0]
    assert "07:30" in warnings[0]


def test_clash_warnings_empty_when_no_conflict():
    """A clean schedule yields an empty warning list, not an error."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    scheduler.create_schedule(Task("Walk", day, time(7, 30)))
    scheduler.create_schedule(Task("Dinner", day, time(18, 0)))

    assert scheduler.clash_warnings() == []


def test_no_time_clashes_when_all_distinct():
    """Tasks at distinct times report no clashes."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    scheduler.create_schedule(Task("Walk", day, time(7, 30)))
    scheduler.create_schedule(Task("Dinner", day, time(18, 0)))

    assert scheduler.time_clashes() == []


def test_conflicts_detects_overlap():
    """Two tasks overlap when the first is still running as the second starts."""
    day = date(2026, 7, 5)
    scheduler = Scheduler()
    walk = Task("Walk", day, time(7, 30), duration_minutes=45)  # ends 8:15
    vet = Task("Vet", day, time(8, 0), duration_minutes=30)  # overlaps
    dinner = Task("Dinner", day, time(18, 0))  # separate
    for t in (walk, vet, dinner):
        scheduler.create_schedule(t)

    conflicts = scheduler.conflicts(day)
    assert conflicts == [(walk, vet)]