from .algorithm import Algorithm
from thread import Thread

class Priority(Algorithm):
	def __init__(self, threads: list[Thread]) -> None:
		super().__init__(threads)
		self.active_thread: Thread | None = None

	def tick(self, time_step: int) -> Thread | None:
		'''
		Non-preemptive Priority Scheduling Algorith
		Pick the highest priority (lowest number) thread that has arrived
		Run it to completion
		'''

		# if no active thread or active has finished, pick next
		if self.active_thread is None or self.active_thread.is_finished():
			# if finished, do not re-add
			if self.active_thread and self.active_thread.is_finished():
				self.active_thread = None
			
			# Gather all threads that have arrived and not finished
			available=[t for t in self.threads if t.arrival <= time_step and not t.is_finished()]

			if not available:
				return None
			
			# Pick by priority first --> arrival time second
			self.active_thread = min(available, key=lambda t: (t.priority, t.arrival))

		# Run the active thread for one tick
		self.active_thread.tick(time_step)
		return self.active_thread
		