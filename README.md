# Advent of Code 24

Solutions for the advent of code 2024 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2024

## Python

### Custom Key in Sorted

To use a `key` function that takes two arguments use `functools.cmp_to_key`
(see day 5).

```
import functools

def compare(a, b):
    return a - b

ordered = sorted(elements, key=functools.cmp_to_key(compare))
```

## Algorithms

### Loop Detection

Keep track of the states in a visited set, if a state is already visited
there is a loop. The state must contain all necessary information, e.g.
position might not be enough we also need direction.

### Line Representations

There are many ways to represent a line. One example is by a point `(x, y)` and a vector `(u, v)`. Another example is
the general form `ax + by + c = 0`. Both if these avoids to potential division by zero that could be an issue with the
slope-intercept representation `y = m*x + b`. See https://www.sunshine2k.de/articles/algorithm/line2d/linerep2d.html
and day 8.
