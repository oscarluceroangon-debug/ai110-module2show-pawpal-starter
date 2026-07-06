"""PawPal+ demo: build an owner with pets and tasks, then print today's schedule."""

from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    today = date.today()

    # 1. Create an owner.
    owner = Owner(name="Oscar", age=28, address="123 Maple St")

    # 2. Create at least two pets and give them to the owner.
    rex = Pet(name="Rex", animal_type="Dog", breed="Labrador", age=4)
    milo = Pet(name="Milo", animal_type="Cat", breed="Tabby", age=2)
    owner.add_pet(rex)
    owner.add_pet(milo)

    # 3. Add at least three tasks with different times to those pets.
    rex.add_task(Task("Morning walk", today, time(7, 30), priority=2))
    rex.add_task(Task("Dinner", today, time(18, 0), priority=1))
    milo.add_task(Task("Litter box cleaning", today, time(12, 15), priority=3))

    # Register every task with the scheduler.
    scheduler = Scheduler()
    for task in owner.all_tasks():
        scheduler.create_schedule(task)

    # 4. Print "Today's Schedule".
    print("=== PawPal+ ===")
    owner.display_info()
    print("\nPets:")
    owner.display_pets()

    print(f"\nToday's Schedule ({today:%A, %B %d}):")
    for task in scheduler.todays_schedule(today):
        status = "done" if task.check_complete() else "pending"
        print(f"  {task.due_time:%H:%M}  {task.description}  [{status}]")


if __name__ == "__main__":
    main()