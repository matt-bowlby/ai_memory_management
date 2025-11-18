from algorithms.first_come_first_serve import FCFS
from algorithms.priority import Priority
from algorithms.round_robin import RR
from dispatcher import Dispatcher
from thread_file_loader import load_threads_from_file

TICK_RATE = 5 # Ticks per second

def main():
	import time

	tick_interval = 1.0 / TICK_RATE
	next_tick = time.time() + tick_interval

	file_name = "threads_test_cases.txt"
	#file_name = "RR_threads_test_case" # Did not worked out (in the instructions it is a differnet type pof threads)
	#algorithm = FCFS([])
	algorithm = Priority([])
	#algorithm = RR([], quantum=2)
	dispatcher = Dispatcher(load_threads_from_file(file_name), algorithm)

	while True:
		dispatcher.tick()

		# Wait until the next tick
		sleep_duration = next_tick - time.time()
		if sleep_duration > 0:
			time.sleep(sleep_duration)
		next_tick += tick_interval

if __name__ == "__main__":
	main()