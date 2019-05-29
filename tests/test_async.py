import asyncio
from time import time

async def main():
    print('hello')
    await asyncio.sleep(2)
    print('world')

asyncio.run(main())
print('here')


# test thread
def factorize(number):
    for i in range(1, number + 1):
        if number % 1 == 0:
            yield i


numbers = [2139079, 1214759, 1516637, 1852285]
start = time()
for n in numbers:
    list(factorize(n))
end = time()
print('Took {} seconds'.format(end - start))

from threading import Thread

class Factorize(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self) -> None:
        self.factors = list(factorize(self.number))


start = time()
threads = []
for n in numbers:
    thread = Factorize(n)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
end = time()
print('Took {} seconds'.format(end - start))


# test subprocess
import subprocess
proc = subprocess.Popen(['echo', 'Hello from the child!'], stdout=subprocess.PIPE)
out, err = proc.communicate()
print(out.encode('utf-8'))


# test multiprocess
print('test multiprocess')
def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


numbers = [(1963309, 2265973), (2030677, 3814172), (1551645, 2229620), (2039045, 2020802)]
start = time()
results = list(map(gcd, numbers))
end = time()
print('Took {} seconds'.format(end - start))

from concurrent.futures import ProcessPoolExecutor
start = time()
pool = ProcessPoolExecutor(max_workers=2)
results = list(pool.map(gcd, numbers))
end = time()
print('Took {} seconds'.format(end - start))

