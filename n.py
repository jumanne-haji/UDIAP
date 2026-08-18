import itertools

prefix = "0753"

def generate_numbers():
    for digits in itertools.product('0123456789', repeat=6):
        suffix = "".join(digits)
        yield prefix + suffix

# Kuchapisha zote (jumla ni milioni 1 - 1,000,000)
for number in generate_numbers():
    print(number)
