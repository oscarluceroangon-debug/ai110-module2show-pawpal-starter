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

    # 3. Add tasks OUT OF ORDER on purpose, so the sort has something to do.
    #    (Dinner is latest but added first; morning walk is earliest but last.)
    rex.add_task(Task("Dinner", today, time(18, 0), priority=1))
    milo.add_task(Task("Litter box cleaning", today, time(12, 15), priority=3))
    rex.add_task(Task("Morning walk", today, time(7, 30), priority=2))
    # Deliberate clash: Milo needs breakfast at the same time Rex is walked.
    milo.add_task(Task("Breakfast", today, time(7, 30), priority=2))

    # Mark one task done so the completion filter has something to separate.
    rex.tasks[0].mark_complete()  # Dinner

    # Register every task with the scheduler.
    scheduler = Scheduler()
    for task in owner.all_tasks():
        scheduler.create_schedule(task)

    print("=== PawPal+ ===")
    owner.display_info()
    print("\nPets:")
    owner.display_pets()

    # 4a. Sorting: tasks were added out of order; sort_by_time() fixes that.
    print("\nAll tasks sorted by time (Scheduler.sort_by_time()):")
    for task in scheduler.sort_by_time():
        status = "done" if task.check_complete() else "pending"
        print(f"  {task.due_time:%H:%M}  {task.description}  [{status}]")

    # 4b. Filtering by completion status (Owner.filter_tasks()).
    pending = owner.filter_tasks(completed=False)
    print(f"\nStill to do today ({len(pending)} pending):")
    for task in pending:
        print(f"  {task.due_time:%H:%M}  {task.description}")

    done = owner.filter_tasks(completed=True)
    print(f"\nAlready done ({len(done)}):")
    for task in done:
        print(f"  {task.due_time:%H:%M}  {task.description}")

    # 4c. Filtering by pet name (Owner.filter_tasks()).
    print("\nRex's tasks only:")
    for task in owner.filter_tasks(pet_name="Rex"):
        print(f"  {task.due_time:%H:%M}  {task.description}")

    # 4d. Lightweight conflict detection (Scheduler.clash_warnings()).
    print("\nConflict check:")
    warnings = scheduler.clash_warnings()
    if warnings:
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("  No scheduling conflicts. \\o/")


if __name__ == "__main__":
    main()