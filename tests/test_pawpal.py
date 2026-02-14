from datetime import date, timedelta

from pawpal_system import Pet, Scheduler, Task


def test_task_completion_marks_completed() -> None:
	# Arrange
	task = Task(
		name="Morning walk",
		description="Quick walk",
		duration=15,
		priority=1,
		status=Task.STATUS_PENDING,
	)

	# Act
	task.mark_completed()

	# Assert
	assert task.status == Task.STATUS_COMPLETED


def test_pet_task_addition_increases_count() -> None:
	# Arrange
	pet = Pet(name="Milo")
	initial_count = len(pet.list_tasks())
	task = Task(
		name="Breakfast",
		description="Feed at 8 AM",
		duration=10,
		priority=2,
		status=Task.STATUS_PENDING,
	)

	# Act
	pet.add_task(task)

	# Assert
	assert len(pet.list_tasks()) == initial_count + 1


def test_recurring_task_due_daily() -> None:
	pet = Pet(name="Milo")
	task = Task(
		name="Medication",
		description="Daily pill",
		duration=5,
		priority=3,
		status=Task.STATUS_COMPLETED,
		recurrence="daily",
		last_completed_date=date.today() - timedelta(days=1),
	)
	pet.add_task(task)
	scheduler = Scheduler(availability=60, pets=[pet])
	plan = scheduler.generate_daily_plan(on_date=date.today())
	assert len(plan) == 1


def test_conflict_detection_flags_overlap() -> None:
	pet = Pet(name="Luna")
	task_a = Task(
		name="Walk",
		description="Morning walk",
		duration=30,
		priority=2,
		status=Task.STATUS_PENDING,
		due_time=60,
	)
	task_b = Task(
		name="Breakfast",
		description="Feed",
		duration=20,
		priority=3,
		status=Task.STATUS_PENDING,
		due_time=70,
	)
	pet.add_task(task_a)
	pet.add_task(task_b)
	scheduler = Scheduler(availability=120, pets=[pet])
	plan = scheduler.generate_daily_plan()
	conflicts = scheduler.detect_conflicts(plan)
	assert len(conflicts) == 1