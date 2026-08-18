
import itertools

def print_triangle_forever():
    n = 1
    while True:
        row = [str(n**i) for i in range(1, n + 1)]
        line = "  ".join(row)
        print(line)
        n += 1

try:
    print_triangle_forever()
except KeyboardInterrupt:
    print("\nImesimamishwa na mtumiaji.")
