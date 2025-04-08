#  Лабораторна робота 3:

## 3.1

В першому завданні ми маємо протестувати різні команди пов'язані з різними обмеженнями відкритих файлів. 

![Запуск без root-прав](images/lb3.1.png)

Після того, як написав усі ці команди потрібно авторизуватися з root-правами: 
```bash
bash docker run -it --ulimit nofile=4096:8192 ubuntu bash
```

![З root-правами](images/lb3.1.1.png)

Можна побачити, що ліміт у всіх -aH (hard limit) файлів став більшим за -aS (soft limit)

---

## 3.2

Потрібно встановити perf у Docker-контейнері. Це робиться через ```privileged```  в контейнері:
```bash
bash docker run -it --privileged ubuntu bash
```

Після цього можна встановлювати ```perf```:
```bash
bash apt update && apt install -y linux-tools-common linux-tools-generic linux-tools-$(uname -r)
```

Маємо невеличку програму на 'С' з незкінечним лупом:
[lb3.2.c](lb3.2.c)

В іншому вікні терміналу вводимо
```bash
bash ps aux
```

Відслідковуємо PID запущеної програму і вводимо
```bash
bash perf stat -p <PID>
```

![](images/lb3.2.png)

---

##  3.3

Маємо програму для [кидків](lb3.3.py) кубика на пайтоні та текстовий документ, куди записуються [результати](DResults.txt):
```python
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
```


Перед тим, як її запустити встановлюю обмеження 10 блоків по 512 байт:
```bash
bash ulimit -f 10
```

Запускаю:
```bash
bash python3 dice_simulator.p
```

Вивело таку помилку в консолі:

![Помилка](images/lb3.3.png)

Програма перевищела ліміт на цьому моменті:

![Програма зупинилася на 863-му кидкі](images/lb3.3.1.png)

Усередині контейнера:
```bash
apt update && apt install -y python3 gcc make perf gdb
```

---

##  3.4

Маємо програму яка імітує [лотерею](lb3.4.py):
```python
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
```

Перед запуском встановлюю ліміт на 2 секунди:
```bash
bash ulimit -t 2
```

Після запуску програма почне виводити в консоль результати кидків і ядро силоміць знищує програму після вичерпання ліміту процесу:

![Killed](images/lb3.4.png)

Ядро вбиває процес, після чого ми бачимо у консолі слово "Вбито"(Killed) яке спричиняє саме ядро.

---

##  3.5

Створюємо програму для [копіювання](lb3.5.py) вмісту текста. Вона приймає 2 аргументи як [вхідний](input.txt) та [вихідний](output.txt) тексти.
```python
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
```

Запускаємо перший раз:

![Звичайний](images/lb3.5.png)

Програма повідомила про успішне копіювання тексту та вивела, скільки зайняло пам'яті

Спробуємо запустити з різними дозволами:
```bash
bash chmod -w output.txt
```

![Помилка](images/lb3.5.1.png)

Тепер перевищемо заданий ліміт в 1 мб:

![Limit](images/lb3.5.2.png)

---

##  3.6

Зробив рекурсивний [скрипт](lb3.6.py)
```python
def recursive(depth = 0):
	print(f"Recursive depth: {depth}")
	recursive(depth + 1)

try:
	recursive()

except RecursionError as e:
	print(f"Stack limit over: {e}")
```

Ця буде виводити в консоль стек, а під кінець видасть помилку ```Stack Limit Over```:

![Stack](images/lb3.6.png)

---

## №10

Для останнього завдання я написав [bash-скріпт](tests.sh) який одночасно показує усі можливі ulimit обмеження:
```bash
bash #!/bin/bash

echo "Start"

echo -e "Ulimit soft:"
ulimit -aS

echo -e "Ulimit hard:"
ulimit -aH

echo -n "Max open files:"
ulimit -n

echo -n "Max user procces:"
ulimit -u

echo -n "Max stack size:"
ulimit -s

echo -n "Max CPU time:"
ulimit -t

echo -n "Max virtual memory:"
ulimit -v

echo -e "Modifying:"

try_set(){
	local name="$1"
	local opt="$2"
	local val="$3"
	echo -n "Setting $name to $val:"
	if ulimit -$opt $val 2>/dev/null; then
		echo "Success":
	else
		echo "Failed"
	fi
}


try_set "max open files" n 2048
try_set "max stack size" s 1024
try_set "max CPU time" t 10

ulimit -aS

echo "End"
```

Ось, що він вивів мені:
```bash
bash nano tests.sh
maks@maks-VirtualBox:~/lb3$ ./tests.sh
Start
Ulimit soft:
real-time non-blocking time  (microseconds, -R) unlimited
core file size              (blocks, -c) 0
data seg size               (kbytes, -d) unlimited
scheduling priority                 (-e) 0
file size                   (blocks, -f) unlimited
pending signals                     (-i) 7552
max locked memory           (kbytes, -l) 251928
max memory size             (kbytes, -m) unlimited
open files                          (-n) 1024
pipe size                (512 bytes, -p) 8
POSIX message queues         (bytes, -q) 819200
real-time priority                  (-r) 0
stack size                  (kbytes, -s) 8192
cpu time                   (seconds, -t) unlimited
max user processes                  (-u) 7552
virtual memory              (kbytes, -v) unlimited
file locks                          (-x) unlimited
Ulimit hard:
real-time non-blocking time  (microseconds, -R) unlimited
core file size              (blocks, -c) unlimited
data seg size               (kbytes, -d) unlimited
scheduling priority                 (-e) 0
file size                   (blocks, -f) unlimited
pending signals                     (-i) 7552
max locked memory           (kbytes, -l) 251928
max memory size             (kbytes, -m) unlimited
open files                          (-n) 1048576
pipe size                (512 bytes, -p) 8
POSIX message queues         (bytes, -q) 819200
real-time priority                  (-r) 0
stack size                  (kbytes, -s) unlimited
cpu time                   (seconds, -t) unlimited
max user processes                  (-u) 7552
virtual memory              (kbytes, -v) unlimited
file locks                          (-x) unlimited
Max open files:1024
Max user procces:7552
Max stack size:8192
Max CPU time:unlimited
Max virtual memory:unlimited
Modifying:
Setting max open files to 2048:Success:
Setting max stack size to 1024:Success:
Setting max CPU time to 10:Success:
real-time non-blocking time  (microseconds, -R) unlimited
core file size              (blocks, -c) 0
data seg size               (kbytes, -d) unlimited
scheduling priority                 (-e) 0
file size                   (blocks, -f) unlimited
pending signals                     (-i) 7552
max locked memory           (kbytes, -l) 251928
max memory size             (kbytes, -m) unlimited
open files                          (-n) 2048
pipe size                (512 bytes, -p) 8
POSIX message queues         (bytes, -q) 819200
real-time priority                  (-r) 0
stack size                  (kbytes, -s) 1024
cpu time                   (seconds, -t) 10
max user processes                  (-u) 7552
virtual memory              (kbytes, -v) unlimited
file locks                          (-x) unlimited
End
```

Можна побачити, що деякі з обмежень процесів змінилися.