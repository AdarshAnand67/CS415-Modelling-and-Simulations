    # Generator function


def my_generator(n):
    yield 1+n
    yield 2+n
    yield 3+n
    return


g1 = my_generator(0)
g2 = my_generator(1)

for value in g1:
    print(value)

# print(next(g2))
# print(next(g2))
# print(next(g2))
# print(next(g2))
for val in g2:
    print(val)