# heap_class

list-like implementation of heap/PriorityQueue in Python

# Installation

```
% pip install heap-class
```

Note the hyphen in the package name

# Usage

From `heap_class` (underscore, not hyphen) import `Heap`.

Create an easy max-heap.

```
>>> from heap_class import Heap
>>> h = Heap([3, 1, 9, 20], max=True)
```

Standard list and heap methods are all available

```
>>> h.pop()
20
>>> h.peek()  # same as h[0]
9
>>> h.push(17)  # or h.append(17)
>>> h[0]  # same as h.peek()
17
>>> h[1]  # inefficient, but works
9
```

Calling `reversed()` turns it into a min-heap

```
>>> y = reversed(h)
>>> y.peek()
1
```

The `__repr__` of a heap is inefficient, but 
useful for debugging.  It shows the sorted version
of the heap.

```
>>> y
Heap([1, 3, 9, 17], max=False)
```

Contains checking takes place in list's normal `O(n)` time.

```
>>> 9 in y
True
```

To view the raw structure of the heap, call `.raw()`.
(this is the same view as a heapified list)

```
>>> y.raw()
[1, 3, 17, 9]
>>> set(y.raw())  # raw() is helpful for fast casting
{1, 3, 17, 9}
```

Complex entries such as tuples are supported:

```
>>> h2 = Heap([(6,4), (6,9), (10,2)], max=True)
>>> h2.pop()
(10, 2)
>>> h2.pop()
(6, 9)
```

Max heaps with tuples of different types are rather hard 
in heapq because of the different forms of negation each
position needs.  But they are easy here.  This is one of
the main implementation advantages of using heap-class.

```
>>> h2 = Heap([('aa', 4), ('aa', 5), ('zz', 2), ('zz', 1)], max=True)
>>> h2.pop()
('zz', 2)
```

Custom sort keys are supported.  Here we will sort the
heap of names by the second entry (last name)

```
>>> vals = [('Adam', 'Smith'), ('Zeta', 'Jones')]
>>> h3 = Heap(vals, key=lambda name: name[1])
>>> h3.peek()  # Jones comes before Smith
('Zeta', 'Jones')
>>> h3.push(('Aaron', 'Allen'))
>>> h3.peek()
('Aaron', 'Allen')
```

`replace(val)` returns the current first item and
replaces it with the new item (same as 
`heapreplace`/`heapreplace_max` in heapq).

Notice that if you replace the top item with a new item 
the order of the heap automatically changes, so the
new top might differ.

```
>>> h3.replace(('Annie', 'Sun'))
('Aaron', 'Allen')
>>> h3.peek()
('Zeta', 'Jones')
```

(`pushpop()` is also supported, which adds the new item first
before popping the top of the heap).

It is possible to iterate further through the heap
as a sorted container, though this is inefficient
(useful for testing, however)

```
>>> for ordered_name in h3:
...     print(ordered_name)
('Zeta', 'Jones')
('Adam', 'Smith')
('Annie', 'Sun')
```

Note that if you plan to iterate through the whole
Heap, sorting with the same key has the same algorithmic
efficiency but is much faster since it is highly optimized
in C:

```
>>> for ordered_name in sorted(h3.raw(), key=lambda name: name[1]):
...     print(ordered_name)
('Zeta', 'Jones')
('Adam', 'Smith')
('Annie', 'Sun')
```

# Change Log

* 0.9.1b2 -- (2025-08)
    - Add `key` support
    - Added typing
    - Add tests
    - Removed support for `*args` creation: together with `key` support it made
      typing a complete nightmare.
    - Remove undocumented support for `.tup=True/False` a kludge unnecessary after 
      `*args` creation was removed.
    - Remove undocumented `no_private_imports.py` version of Heap. We'll
      update this when heapq changes.
    - Point GitHub link to the right place.

* 0.9.0b1 -- (2022)
    - Initial release


# Credit

Copyright © 2022-25 Michael Scott Asato Cuthbert

# License

MIT

# Development/Distribution

* Install build tools

```
% pip install -U build twine pytest
```

* Run tests

```
% pytest tests/tests.py
```

If you get big failures, make sure you've run `pip install -e .` in the main directory 
(with pyproject.toml in it) to make `heap_class` visible to the tests.

Fix any problems, obviously.

* Update `__version__` in `heap_class/__init.py`.
* Empty existing builds:

```
% trash dist build *.egg-info
```

(if you don't have trash on your OS, use `rm -rf` instead)

* Check that artifacts render on PyPI

```
% twine check dist/*
```

* Upload to PyPI

```
% twine upload dist/*
```

You will need the proper `.pypirc` with passwords etc.  See elsewhere on-line for
docs on that.
