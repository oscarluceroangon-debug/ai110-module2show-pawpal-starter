"""PawPal+ system.

Classes generated from diagrams/uml_draft.mmd. Objects like Task, Pet, and
Owner use dataclasses to keep the data-holding code clean; Scheduler is a plain
service class since it acts on tasks rather than holding structured data.
"""

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Task:
    description: str
    date: date
    due_time: time
    is_complete: bool = False
    # Per-task scheduling data (moved off Scheduler so each task carries its own).
    priority: int = 0
    preference: str = ""

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

    def todays_schedule(self, today: date) -> list[Task]:
        """Tasks due today, ordered by due time then priority (higher first)."""
        due_today = [t for t in self.scheduled_tasks if t.date == today]
        return sorted(due_today, key=lambda t: (t.due_time, -t.priority))