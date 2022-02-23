def topten():
    # Print square of numbers from 1 to 10
    n = 1
    while n <= 10:
        sq = n * n
        yield sq
        n += 1


values = topten()
print(values)
# print(next(values))
# print(next(values))
# print(next(values))
for i in values:
    print(i)


"""
The yield statement suspends function’s execution and sends a value back to the caller, but retains enough state to enable function to resume where it is left off. When resumed, the function continues execution immediately after the last yield run. This allows its code to produce a series of values over time, rather than computing them at once and sending them back like a list.
"""
