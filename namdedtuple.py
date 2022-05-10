from collections import namedtuple


PointTuple = namedtuple('point', ['x', 'y'])

point = PointTuple(1, 2)
print(f"The coordinates are {point.x}, {point.y}")


StudentTuple = namedtuple('student', ['name', 'age', 'college', 'gpa'])

student1 = StudentTuple('John', 20, 'UCB', 3.5)
student2 = StudentTuple('Mary', 21, 'UCB', 3.0)

for student in [student1, student2]:
    print(f"{student.name} is {student.age} years old, and is in {student.college}. Their GPA is {student.gpa}.")

Theater = namedtuple('Theater', 'counter, movies, available, '
                     'sold_out, when_sold_out, '
                     'num_renegers')

theater = Theater(2, ['The Lion King', 'The Little Mermaid'], 0, 0, 0, 0)

print(f"The theater has {theater.counter} seats.")
print(f"The theater has {theater.movies} movies.")