
from dataclasses import dataclass, field


class Owner:
	def __init__(self, name):
		self.name = name
		self.owned_pets = []  # List of Pet objects

	def add_pet(self, pet):
		pass


@dataclass
class Pet:
	name: str
	current_tasks: list = field(default_factory=list)


class Scheduler:
	def __init__(self, availability):
		self.availability = availability  # Could be a schedule or timeframe

	def generate_daily_plan(self):
		pass


@dataclass
class Task:
	name: str
	description: str
	duration: int
	priority: int
	status: str

	def mark_in_progress(self):
		pass

	def mark_completed(self):
		pass

	def update_task_duration(self, duration):
		pass

	def update_task_priority(self, priority):
		pass
