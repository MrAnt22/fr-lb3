def recursive(depth = 0):
	print(f"Recursive depth: {depth}")
	recursive(depth + 1)

try:
	recursive()

except RecursionError as e:
	print(f"Stack limit over: {e}")
