def print_triangle(k):
    rows = []
    for n in range(1, k + 1):
        row = [str(n**i) for i in range(1, n + 1)]
        rows.append("  ".join(row))
    
    width = len(rows[-1])
    for row in rows:
        print(row.center(width))

# Mfano wa matumizi
print_triangle(5)
