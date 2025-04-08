import sys
import os

MAX_FILE_SIZE = 1024 * 1024 * 1

def main():
	if len(sys.argv) != 3:
		print("Program need two arguments")
		sys.exit(1)

	source = sys.argv[1]
	target = sys.argv[2]

	if not os.access(source, os.R_OK):
		print(f"Cannot open file {source}  for reading")
		sys.exit(1)

	with open(source, "rb") as src, open(target, "wb") as dst:
		total_written = 0
		while True:
			chunk = src.read(4096)
			if not chunk:
				break
			total_written += len(chunk)

			if total_written > MAX_FILE_SIZE:
				print("File size limit over")
				sys.exit(1)


			dst.write(chunk)
	print(f"Copied successfully ({total_written} bytes)")

if __name__ == "__main__":
	main()







