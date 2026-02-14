
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, Iterable, List, Optional, Tuple


def sort_by_time(tasks: Iterable["Task"]) -> List["Task"]:
	"""Return tasks sorted by due time, placing unscheduled tasks last."""
	return sorted(
		tasks,
		key=lambda task: (
			task.due_time is None,
			task.due_time if task.due_time is not None else 0,
		),
	)

def filter_tasks_by_status(
	*,
	tasks: Iterable[Tuple["Pet", "Task"]],
	status: Optional[str] = None,
	pet_name: Optional[str] = None,
) -> List[Tuple["Pet", "Task"]]:
	"""Filter tasks from an iterable based on status and/or pet name."""
	filtered: List[Tuple[Pet, Task]] = []
	for pet, task in tasks:
		if status is not None and task.status != status:
			continue
		if pet_name is not None and pet.name != pet_name:
			continue
		filtered.append((pet, task))
	return filtered


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
	def __init__(
		self,
		availability: Optional[int] = None,
		pets: Optional[List[Pet]] = None,
		*,
		timeframe_availability: Optional[int] = None,
	) -> None:
		"""Initialize the scheduler with availability and pets."""
		if availability is None and timeframe_availability is not None:
			availability = timeframe_availability
		self.availability: Optional[int] = availability
		self.pets: List[Pet] = pets or []
		self.same_time_conflicts: List[Tuple[Pet, Task, Pet, Task]] = []

	def generate_daily_plan(
		self,
		*,
		pet_name: Optional[str] = None,
		status: Optional[str] = None,
		on_date: Optional[date] = None,
	) -> List[Tuple[Pet, "Task"]]:
		"""Generate an ordered plan of due tasks within availability."""
		available_minutes = self.availability if isinstance(self.availability, int) else None
		plan_candidates = self._collect_tasks(pet_name=pet_name, status=status, on_date=on_date)

		plan_candidates.sort(
			key=lambda item: (
				item[1].due_time is None,
				item[1].due_time if item[1].due_time is not None else 0,
				-item[1].priority,
				item[1].duration,
			)
		)

		if available_minutes is None:
			self.same_time_conflicts = self.detect_same_time_conflicts(plan_candidates)
			return plan_candidates

		plan: List[Tuple[Pet, Task]] = []
		used_minutes = 0
		for pet, task in plan_candidates:
			if used_minutes + task.duration > available_minutes:
				continue
			plan.append((pet, task))
			used_minutes += task.duration

		self.same_time_conflicts = self.detect_same_time_conflicts(plan)
		return plan

	def detect_conflicts(self, plan: Iterable[Tuple[Pet, "Task"]]) -> List[Tuple[Pet, "Task", Pet, "Task"]]:
		"""Detect time conflicts in a plan with explicit start times."""
		timed_tasks = [item for item in plan if item[1].due_time is not None]
		timed_tasks.sort(key=lambda item: item[1].due_time)
		conflicts: List[Tuple[Pet, Task, Pet, Task]] = []
		current_end: Optional[int] = None
		current_item: Optional[Tuple[Pet, Task]] = None
		for pet, task in timed_tasks:
			start_time = task.due_time
			if start_time is None:
				continue
			if current_end is not None and start_time < current_end and current_item is not None:
				conflicts.append((current_item[0], current_item[1], pet, task))
			end_time = start_time + task.duration
			if current_end is None or end_time > current_end:
				current_end = end_time
				current_item = (pet, task)
		return conflicts

	def detect_same_time_conflicts(
		self,
		plan: Iterable[Tuple[Pet, "Task"]],
	) -> List[Tuple[Pet, "Task", Pet, "Task"]]:
		"""Detect tasks that share the same due time."""
		conflicts: List[Tuple[Pet, Task, Pet, Task]] = []
		seen: Dict[int, Tuple[Pet, Task]] = {}
		for pet, task in plan:
			if task.due_time is None:
				continue
			if task.due_time in seen:
				other_pet, other_task = seen[task.due_time]
				conflicts.append((other_pet, other_task, pet, task))
			else:
				seen[task.due_time] = (pet, task)
		return conflicts

	def _collect_tasks(
		self,
		*,
		pet_name: Optional[str],
		status: Optional[str],
		on_date: Optional[date],
	) -> List[Tuple[Pet, "Task"]]:
		"""Collect tasks across pets with optional filters."""
		target_date = on_date or date.today()
		collected: List[Tuple[Pet, Task]] = []
		for pet in self.pets:
			if pet_name and pet.name != pet_name:
				continue
			for task in pet.list_tasks():
				if status is None and task.status == Task.STATUS_COMPLETED:
					continue
				if status is not None and task.status != status:
					continue
				if not task.is_due(target_date):
					continue
				collected.append((pet, task))
		return collected


@dataclass
class Task:
	name: str
	description: str
	duration: int
	priority: int
	status: str
	due_time: Optional[int] = None
	recurrence: Optional[str] = None
	last_completed_date: Optional[date] = None
	next_due_date: Optional[date] = None

	STATUS_PENDING = "pending"
	STATUS_IN_PROGRESS = "in_progress"
	STATUS_COMPLETED = "completed"

	def mark_in_progress(self) -> None:
		"""Mark this task as in progress."""
		self.status = self.STATUS_IN_PROGRESS

	def mark_completed(self, completed_on: Optional[date] = None) -> None:
		"""Mark this task as completed."""
		self.status = self.STATUS_COMPLETED
		self.last_completed_date = completed_on or date.today()
		if self.recurrence in {"daily", "weekly"}:
			days = 1 if self.recurrence == "daily" else 7
			self.next_due_date = self.last_completed_date + timedelta(days=days)
			self.status = self.STATUS_PENDING

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

	def is_due(self, on_date: date) -> bool:
		"""Return True if this task should be scheduled on the given date."""
		if self.status == self.STATUS_COMPLETED and self.recurrence is None:
			return False
		if self.recurrence is None:
			return self.status != self.STATUS_COMPLETED
		if self.recurrence == "daily":
			if self.last_completed_date is None:
				return True
			return on_date >= self.last_completed_date + timedelta(days=1)
		if self.recurrence == "weekly":
			if self.last_completed_date is None:
				return True
			return on_date >= self.last_completed_date + timedelta(days=7)
		return True
