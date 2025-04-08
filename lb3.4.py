import random
import time
import signal
import sys

def timelimit(signum, frame):
	print("CPU time limit over")
	sys.exit(1)

signal.signal(signal.SIGXCPU, timelimit)

def lottery():
	seven = random.sample(range(1,50),7)
	six = random.sample(range(1,37),6)
	return seven, six

def main():
	print("Lottery started")
	while True:
		seven, six = lottery()
		print(f"7 of 49: {seven} | 6 of 36: {six}")

if __name__ == "__main__":
	main()


