from pawpal_system import Pet, Task


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