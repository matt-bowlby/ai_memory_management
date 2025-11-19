from .algorithm import Algorithm
from thread import Thread

class PreemptiveSJF(Algorithm):
	def __init__(self, threads: list[Thread]) -> None:
		super().__init__(threads)
		self.active_thread: Thread | None = None

	def tick(self, time_step: int) -> Thread | None:
		'''
		Preemptive Shortest Job First
		Always select a thread with the shortest remaining time
		Preempts the currently running thread if a shorter one arrives.'''
		
        # Gather all arrived and not finished threads
		available = [th for th in self.threads if th.arrival <= time_step and not th.is_finished()]
		if not available: 
			return None # not thread available
		
        # Pick the thread with the shortest remianing time
		shortest = min(available, key=lambda th: (th.remaining, th.arrival))
		
        # Preemption check: 
		if (
			self.active_thread is None 
			or self.active_thread.is_finished()
			or self.active_thread != shortest
        ): 
			self.active_thread = shortest

		# Run active thread for one tick
		self.active_thread.tick(time_step)
		return self.active_thread

