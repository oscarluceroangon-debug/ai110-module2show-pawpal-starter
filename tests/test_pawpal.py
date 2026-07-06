"""Tests for the PawPal+ system classes."""

from datetime import date, time

from pawpal_system import Pet, Task


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