from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task, sort_by_time


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


def test_task_updates_validate_duration_and_priority() -> None:
	# Arrange
	task = Task(
		name="Groom",
		description="Brush coat",
		duration=10,
		priority=1,
		status=Task.STATUS_PENDING,
	)

	# Act
	task.update_task_duration(25)
	task.update_task_priority(4)

	# Assert
	assert task.duration == 25
	assert task.priority == 4


def test_task_update_duration_rejects_non_positive() -> None:
	# Arrange
	task = Task(
		name="Trim",
		description="Nail trim",
		duration=10,
		priority=1,
		status=Task.STATUS_PENDING,
	)

	# Act / Assert
	try:
		task.update_task_duration(0)
		assert False, "Expected ValueError for non-positive duration"
	except ValueError:
		assert True


def test_task_update_priority_rejects_negative() -> None:
	# Arrange
	task = Task(
		name="Bath",
		description="Warm bath",
		duration=20,
		priority=1,
		status=Task.STATUS_PENDING,
	)

	# Act / Assert
	try:
		task.update_task_priority(-1)
		assert False, "Expected ValueError for negative priority"
	except ValueError:
		assert True


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


def test_pet_task_crud_roundtrip() -> None:
	# Arrange
	pet = Pet(name="Luna")
	task = Task(
		name="Playtime",
		description="Fetch session",
		duration=15,
		priority=2,
		status=Task.STATUS_PENDING,
	)

	# Act
	pet.add_task(task)
	found = pet.get_task("Playtime")
	pet.remove_task("Playtime")
	missing = pet.get_task("Playtime")

	# Assert
	assert found is task
	assert missing is None
	assert len(pet.list_tasks()) == 0


def test_owner_add_pet_sets_owner_and_aggregates_tasks() -> None:
	# Arrange
	owner = Owner(name="Avery")
	pet = Pet(name="Milo")
	task = Task(
		name="Dinner",
		description="Feed at 6 PM",
		duration=10,
		priority=2,
		status=Task.STATUS_PENDING,
	)
	pet.add_task(task)

	# Act
	owner.add_pet(pet)
	all_tasks = owner.get_all_tasks()

	# Assert
	assert pet.owner is owner
	assert task in all_tasks


def test_recurring_task_due_daily() -> None:
	pet = Pet(name="Milo")
	task = Task(
		name="Medication",
		description="Daily pill",
		duration=5,
		priority=3,
		status=Task.STATUS_PENDING,
		recurrence="daily",
		last_completed_date=date.today() - timedelta(days=1),
	)
	pet.add_task(task)
	scheduler = Scheduler(availability=60, pets=[pet])
	plan = scheduler.generate_daily_plan(on_date=date.today())
	assert len(plan) == 1


def test_recurring_task_weekly_not_due_too_soon() -> None:
	# Arrange
	task = Task(
		name="Weigh-in",
		description="Weekly weight check",
		duration=5,
		priority=1,
		status=Task.STATUS_COMPLETED,
		recurrence="weekly",
		last_completed_date=date.today() - timedelta(days=3),
	)

	# Act
	is_due = task.is_due(date.today())

	# Assert
	assert is_due is False


def test_sort_by_time_orders_unscheduled_last() -> None:
	# Arrange
	task_early = Task(
		name="Early",
		description="",
		duration=5,
		priority=1,
		status=Task.STATUS_PENDING,
		due_time=30,
	)
	task_late = Task(
		name="Late",
		description="",
		duration=5,
		priority=1,
		status=Task.STATUS_PENDING,
		due_time=90,
	)
	task_unscheduled = Task(
		name="Anytime",
		description="",
		duration=5,
		priority=1,
		status=Task.STATUS_PENDING,
		due_time=None,
	)

	# Act
	sorted_tasks = sort_by_time([task_unscheduled, task_late, task_early])

	# Assert
	assert [task.name for task in sorted_tasks] == ["Early", "Late", "Anytime"]


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


def test_same_time_conflicts_detected_in_plan() -> None:
	# Arrange
	pet = Pet(name="Nova")
	task_a = Task(
		name="Walk",
		description="Evening walk",
		duration=20,
		priority=1,
		status=Task.STATUS_PENDING,
		due_time=120,
	)
	task_b = Task(
		name="Play",
		description="Fetch",
		duration=15,
		priority=2,
		status=Task.STATUS_PENDING,
		due_time=120,
	)
	pet.add_task(task_a)
	pet.add_task(task_b)
	scheduler = Scheduler(availability=None, pets=[pet])

	# Act
	plan = scheduler.generate_daily_plan()
	conflicts = scheduler.same_time_conflicts

	# Assert
	assert len(plan) == 2
	assert len(conflicts) == 1