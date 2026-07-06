"""PawPal+ system.

Classes generated from diagrams/uml_draft.mmd. Objects like Task, Pet, and
Owner use dataclasses to keep the data-holding code clean; Scheduler is a plain
service class since it acts on tasks rather than holding structured data.
"""

from dataclasses import dataclass, field, replace
from datetime import date, datetime, time, timedelta


@dataclass
class Task:
    description: str
    date: date
    due_time: time
    is_complete: bool = False
    # Per-task scheduling data (moved off Scheduler so each task carries its own).
    priority: int = 0
    preference: str = ""
    # How long the task is expected to take; used for conflict detection.
    duration_minutes: int = 15
    # How often the task repeats: "none", "daily", or "weekly".
    recurrence: str = "none"

    def get_description(self) -> str:
        """Return this task's description text."""
        return self.description

    def get_date(self) -> date:
        """Return the date this task is scheduled for."""
        return self.date

    def check_complete(self) -> bool:
        """Return whether this task has been completed."""
        return self.is_complete

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True

    def end_time(self) -> time:
        """Return the clock time this task is expected to finish."""
        start = datetime.combine(self.date, self.due_time)
        return (start + timedelta(minutes=self.duration_minutes)).time()

    def status(self, now: datetime) -> str:
        """Return 'done', 'overdue', or 'pending' relative to now."""
        if self.is_complete:
            return "done"
        if datetime.combine(self.date, self.due_time) < now:
            return "overdue"
        return "pending"

    def next_occurrence(self) -> "Task | None":
        """Build the next occurrence of a recurring task.

        Returns a fresh, incomplete copy with the date advanced by one day
        ("daily") or one week ("weekly"); all other fields are preserved.
        Returns None for a one-off task (recurrence == "none").
        """
        if self.recurrence == "daily":
            delta = timedelta(days=1)
        elif self.recurrence == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None
        return replace(self, date=self.date + delta, is_complete=False)


@dataclass
class Pet:
    name: str
    animal_type: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet, ignoring it if not present."""
        if task in self.tasks:
            self.tasks.remove(task)

    def display_info(self) -> None:
        """Print this pet's name, type, breed, and age."""
        print(f"{self.name} ({self.animal_type}, {self.breed}, age {self.age})")


@dataclass
class Owner:
    name: str
    age: int
    address: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner, ignoring it if not present."""
        if pet in self.pets:
            self.pets.remove(pet)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def filter_tasks(
        self,
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks across all pets, optionally narrowed by criteria.

        Pass ``completed=True``/``False`` to keep only done/pending tasks, and
        ``pet_name`` to keep only tasks belonging to that pet. A criterion left
        as ``None`` is ignored, so calling with no arguments returns every task.
        """
        results: list[Task] = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.is_complete != completed:
                    continue
                results.append(task)
        return results

    def display_pets(self) -> None:
        """Print info for each of this owner's pets."""
        for pet in self.pets:
            pet.display_info()

    def display_info(self) -> None:
        """Print this owner's name, age, and address."""
        print(f"{self.name}, age {self.age} — {self.address}")


class Scheduler:
    def __init__(self) -> None:
        """Create a scheduler with an empty list of scheduled tasks."""
        self.scheduled_tasks: list[Task] = []

    def create_schedule(self, task: Task) -> None:
        """Add a task to the schedule, skipping duplicates."""
        if task not in self.scheduled_tasks:
            self.scheduled_tasks.append(task)

    def cancel_schedule(self, task: Task) -> None:
        """Remove a task from the schedule, ignoring it if not present."""
        if task in self.scheduled_tasks:
            self.scheduled_tasks.remove(task)

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and auto-schedule its next occurrence if it recurs.

        Returns the newly scheduled next-occurrence Task, or None for a
        one-off task. The new instance is registered on this scheduler so it
        shows up in future schedules automatically.
        """
        task.mark_complete()
        upcoming = task.next_occurrence()
        if upcoming is not None:
            self.create_schedule(upcoming)
        return upcoming

    def sort_by_time(self) -> list[Task]:
        """Return the scheduled tasks ordered by due time, earliest first.

        Uses a lambda as the sort ``key``: each task's ``due_time`` is rendered
        as an ``"HH:MM"`` string and the tasks are ordered by those strings.
        Because the hours and minutes are zero-padded, lexicographic (string)
        ordering matches chronological ordering (e.g. ``"07:30" < "12:15" <
        "18:00"``), so no time arithmetic is needed.

        The comparison ignores the date, so tasks on different days interleave
        purely by clock time. Tasks sharing a due time keep their existing
        relative order, since :func:`sorted` is stable.

        Returns:
            A new list of the scheduled tasks sorted by due time. The
            scheduler's own ``scheduled_tasks`` list is left unchanged.
        """
        # key = the "HH:MM" text of each task's due time; sorted() calls it once
        # per task, then orders the tasks by comparing those strings.
        return sorted(self.scheduled_tasks, key=lambda t: t.due_time.strftime("%H:%M"))

    def todays_schedule(self, today: date) -> list[Task]:
        """Tasks due today, ordered by due time then priority (higher first)."""
        due_today = [t for t in self.scheduled_tasks if t.date == today]
        return sorted(due_today, key=lambda t: (t.due_time, -t.priority))

    def conflicts(self, today: date) -> list[tuple[Task, Task]]:
        """Pairs of consecutive tasks today whose times overlap.

        Two tasks conflict when the earlier one is still running (its
        end_time) after the later one is due to start.
        """
        tasks = self.todays_schedule(today)
        return [
            (earlier, later)
            for earlier, later in zip(tasks, tasks[1:])
            if earlier.end_time() > later.due_time
        ]

    def time_clashes(self) -> list[list[Task]]:
        """Groups of tasks scheduled for the exact same date and time.

        Any group with two or more tasks is a clash: the owner is expected in
        two places at once. This spans all scheduled tasks, so it catches
        clashes whether the tasks belong to the same pet or different pets.
        Each returned group keeps the order the tasks were scheduled in.
        """
        groups: dict[tuple[date, time], list[Task]] = {}
        for task in self.scheduled_tasks:
            groups.setdefault((task.date, task.due_time), []).append(task)
        return [tasks for tasks in groups.values() if len(tasks) > 1]

    def clash_warnings(self) -> list[str]:
        """Lightweight conflict check: return warning strings, never raise.

        Turns each same-time clash into a readable message a UI or terminal
        can print directly. If anything unexpected goes wrong it degrades to a
        single explanatory warning instead of crashing the program, so callers
        can rely on always getting a (possibly empty) list of strings back.
        """
        try:
            warnings: list[str] = []
            for group in self.time_clashes():
                when = group[0]
                names = ", ".join(task.description for task in group)
                warnings.append(
                    f"WARNING: {len(group)} tasks at the same time "
                    f"({when.date:%b %d} {when.due_time:%H:%M}): {names}"
                )
            return warnings
        except Exception as exc:  # defensive: a warning is safer than a crash
            return [f"WARNING: could not check for conflicts ({exc})"]