import random
import os

def roll():
	return random.randint(1,6)

def diceroll(filename, max_rolls= 10000):
	try:
		with open(filename, 'w') as f:
			for i in range(max_rolls):
				result = roll()
				f.write(f"roll {i + 1}: {result}\n")
	except OSError as e:
		print(f"Error: {e}")
		if "File too large" in str(e):
			print("FIle size overlimited")


if __name__ == "__main__":
	output_file = "DResults.txt"
	diceroll(output_file)
