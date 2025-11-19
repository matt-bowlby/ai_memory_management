from .algorithm import Algorithm
from thread import Thread

class SJF(Algorithm):
	def __init__(self, threads: list[Thread]) -> None:
		super().__init__(threads)
		self.active_thread: Thread | None = None

	def tick(self, time_step: int) -> Thread | None:
		'''
		Non-preemptive Shortest Job First Scheduling Algorithm
		Pick the thread with the shortest remaining time that has arrived
		Run it to completion
		'''
		# If there is no active thread or it finished, pick next thread
		if self.active_thread is None or self.active_thread.is_finished():
			if self.active_thread and self.active_thread.is_finished():
				self.active_thread = None 

			# Gather all arrived and not finished threads
			available = [th for th in self.threads if th.arrival <= time_step and not th.is_finished()]
			if not available:
				return None
			
			# pick the one with the shortest remaining time
			self.active_thread = min(available, key=lambda th: (th.burst, th.arrival))

		# Run active thread for one tick
		self.active_thread.tick(time_step)
		return self.active_thread
