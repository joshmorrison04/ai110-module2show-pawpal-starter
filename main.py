"""Entry point for the PawPal demo schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
	owner = Owner("Jordan")

	pet_1 = Pet("Milo")
	pet_2 = Pet("Luna")

	owner.add_pet(pet_1)
	owner.add_pet(pet_2)

	pet_1.add_task(
		Task(
			name="Morning walk",
			description="30-minute walk at 7:30 AM",
			duration=30,
			priority=2,
			status=Task.STATUS_PENDING,
		)
	)
	pet_1.add_task(
		Task(
			name="Breakfast",
			description="Feed at 8:15 AM",
			duration=10,
			priority=3,
			status=Task.STATUS_PENDING,
		)
	)
	pet_2.add_task(
		Task(
			name="Playtime",
			description="20-minute play at 6:00 PM",
			duration=20,
			priority=1,
			status=Task.STATUS_PENDING,
		)
	)

	scheduler = Scheduler(availability=90, pets=owner.owned_pets)
	plan = scheduler.generate_daily_plan()

	print("Today's Schedule")
	print("=" * 17)
	for pet, task in plan:
		print(f"{pet.name}: {task.name} ({task.duration} min) - {task.description}")


if __name__ == "__main__":
	main()
