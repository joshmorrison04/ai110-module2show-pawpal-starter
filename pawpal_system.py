
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


class Owner:
	def __init__(self, name: str) -> None:
		"""Initialize an owner with a name and empty pet list."""
		self.name: str = name
		self.owned_pets: List[Pet] = []

	def add_pet(self, pet: "Pet") -> None:
		"""Add a pet to this owner's list if not already present."""
		if pet not in self.owned_pets:
			self.owned_pets.append(pet)
			pet.owner = self

	def get_all_tasks(self) -> List["Task"]:
		"""Return a combined list of tasks for all owned pets."""
		all_tasks: List[Task] = []
		for pet in self.owned_pets:
			all_tasks.extend(pet.list_tasks())
		return all_tasks


@dataclass
class Pet:
	name: str
	owner: Optional[Owner] = None
	current_tasks: Dict[str, "Task"] = field(default_factory=dict)

	def add_task(self, task: "Task") -> None:
		"""Add or replace a task by name for this pet."""
		self.current_tasks[task.name] = task

	def get_task(self, task_name: str) -> Optional["Task"]:
		"""Get a task by name if it exists."""
		return self.current_tasks.get(task_name)

	def remove_task(self, task_name: str) -> None:
		"""Remove a task by name if present."""
		self.current_tasks.pop(task_name, None)

	def list_tasks(self) -> List["Task"]:
		"""List all current tasks for this pet."""
		return list(self.current_tasks.values())


class Scheduler:
	def __init__(self, availability: Optional[int], pets: Optional[List[Pet]] = None) -> None:
		"""Initialize the scheduler with availability and pets."""
		self.availability: Optional[int] = availability
		self.pets: List[Pet] = pets or []

	def generate_daily_plan(self) -> List[Tuple[Pet, "Task"]]:
		"""Generate an ordered plan of pending tasks within availability."""
		available_minutes = self.availability if isinstance(self.availability, int) else None
		pending_tasks: List[Tuple[Pet, Task]] = []
		for pet in self.pets:
			for task in pet.list_tasks():
				if task.status != Task.STATUS_COMPLETED:
					pending_tasks.append((pet, task))

		pending_tasks.sort(key=lambda item: (-item[1].priority, item[1].duration))

		if available_minutes is None:
			return pending_tasks

		plan: List[Tuple[Pet, Task]] = []
		used_minutes = 0
		for pet, task in pending_tasks:
			if used_minutes + task.duration > available_minutes:
				continue
			plan.append((pet, task))
			used_minutes += task.duration

		return plan


@dataclass
class Task:
	name: str
	description: str
	duration: int
	priority: int
	status: str

	STATUS_PENDING = "pending"
	STATUS_IN_PROGRESS = "in_progress"
	STATUS_COMPLETED = "completed"

	def mark_in_progress(self) -> None:
		"""Mark this task as in progress."""
		self.status = self.STATUS_IN_PROGRESS

	def mark_completed(self) -> None:
		"""Mark this task as completed."""
		self.status = self.STATUS_COMPLETED

	def update_task_duration(self, duration: int) -> None:
		"""Update the task duration after validating it."""
		if duration <= 0:
			raise ValueError("duration must be a positive integer")
		self.duration = duration

	def update_task_priority(self, priority: int) -> None:
		"""Update the task priority after validating it."""
		if priority < 0:
			raise ValueError("priority must be a non-negative integer")
		self.priority = priority
