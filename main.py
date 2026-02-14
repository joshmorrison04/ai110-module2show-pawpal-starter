"""Entry point for the PawPal demo schedule."""

from datetime import date, timedelta
from typing import Iterable, Optional

from pawpal_system import Owner, Pet, Scheduler, Task, sort_by_time


def format_due_time(due_time: Optional[int]) -> str:
	if due_time is None:
		return "unscheduled"
	hours, minutes = divmod(due_time, 60)
	return f"{hours:02d}:{minutes:02d}"


def print_task_list(title: str, tasks: Iterable[Task]) -> None:
	print(title)
	print("-" * len(title))
	for task in tasks:
		due_time = format_due_time(task.due_time)
		print(f"{task.name:<18} | due: {due_time:<12} | status: {task.status}")
	print()


def print_plan(title: str, plan: Iterable[tuple[Pet, Task]]) -> None:
	print(title)
	print("-" * len(title))
	for pet, task in plan:
		due_time = format_due_time(task.due_time)
		print(f"{pet.name:<6} | {task.name:<18} | due: {due_time:<12} | {task.status}")
	print()


def print_conflicts(title: str, conflicts: Iterable[tuple[Pet, Task, Pet, Task]]) -> None:
	print(title)
	print("-" * len(title))
	for pet_a, task_a, pet_b, task_b in conflicts:
		time_label = format_due_time(task_a.due_time)
		print(
			f"{time_label:<12} | {pet_a.name}: {task_a.name}"
			f"  <->  {pet_b.name}: {task_b.name}"
		)
	print()


def main() -> None:
	owner = Owner("Jordan")

	pet_1 = Pet("Milo")
	pet_2 = Pet("Luna")

	owner.add_pet(pet_1)
	owner.add_pet(pet_2)

	walk = Task(
		name="Morning walk",
		description="30-minute walk",
		duration=30,
		priority=2,
		status=Task.STATUS_PENDING,
		due_time=450,
	)
	breakfast = Task(
		name="Breakfast",
		description="Feed kibble",
		duration=10,
		priority=3,
		status=Task.STATUS_PENDING,
		due_time=480,
	)
	meds = Task(
		name="Medication",
		description="Daily pill",
		duration=5,
		priority=3,
		status=Task.STATUS_IN_PROGRESS,
		due_time=480,
	)
	playtime = Task(
		name="Playtime",
		description="20-minute play",
		duration=20,
		priority=1,
		status=Task.STATUS_PENDING,
		due_time=1080,
	)
	grooming = Task(
		name="Grooming",
		description="Brush fur",
		duration=15,
		priority=1,
		status=Task.STATUS_PENDING,
		due_time=540,
	)

	pet_1.add_task(walk)
	pet_1.add_task(breakfast)
	pet_1.add_task(meds)
	pet_2.add_task(playtime)
	pet_2.add_task(grooming)

	unsorted_tasks = [breakfast, playtime, walk, grooming, meds]
	print_task_list("Tasks before sorting", unsorted_tasks)

	if not hasattr(Scheduler, "sort_by_time"):
		Scheduler.sort_by_time = staticmethod(sort_by_time)
	sorted_tasks = Scheduler.sort_by_time(unsorted_tasks)
	print_task_list("Tasks after sorting", sorted_tasks)

	scheduler = Scheduler(availability=120, pets=owner.owned_pets)
	plan_for_milo = scheduler.generate_daily_plan(pet_name="Milo")
	print_plan("Filtered plan (pet = Milo)", plan_for_milo)

	pending_only = scheduler.generate_daily_plan(status=Task.STATUS_PENDING)
	print_plan("Filtered plan (status = pending)", pending_only)

	walk.recurrence = "daily"
	grooming.recurrence = "weekly"

	today = date.today()
	walk.mark_completed(today)
	grooming.mark_completed(today)

	plan_today = scheduler.generate_daily_plan(on_date=today)
	print_plan("Plan after completion (today)", plan_today)

	if scheduler.same_time_conflicts:
		print_conflicts(
			"Warning: tasks share the same due time",
			scheduler.same_time_conflicts,
		)

	plan_tomorrow = scheduler.generate_daily_plan(on_date=today + timedelta(days=1))
	print_plan("Plan for tomorrow (daily recurrence)", plan_tomorrow)

	plan_next_week = scheduler.generate_daily_plan(on_date=today + timedelta(days=7))
	print_plan("Plan for next week (weekly recurrence)", plan_next_week)


if __name__ == "__main__":
	main()
