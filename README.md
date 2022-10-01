# heap_class

list-like implementation of heap/PriorityQueue in Python

# Usage

```python3
>>> from heap_class import Heap
>>> h = Heap([3, 1, 9, 20], max=True)
>>> h.pop()
20
>>> h.peek()  # same as h[0]
9
>>> h.push(17)  # or h.append(17)
>>> h[0]  # same as h.peek()
17
>>> h[1]  # inefficient, but works
9
>>> y = reversed(h)
>>> y.peek()
1
>>> y  # repr is inefficient, but correct
Heap([1, 3, 9, 17], max=False)
>>> 9 in y
True
>>> y.raw()  # heap structure
[1, 3, 17, 9]
>>> set(y.raw())  # raw helpful for fast casting
{1, 3, 17, 9}

Complex entries and *args creation supported.

>>> h = Heap((6,4), (6,9), (10,2), max=True)
>>> h.pop()
(10, 2)
>>> h.pop()
(6, 9)

This is rather hard in heapq because of the different
forms of negation.  Easy here.

>>> h = Heap(('aa', 4), ('aa', 5), ('zz', 2), ('zz', 1), max=True)
>>> h.pop()
('zz', 2)

Custom keys are supported:

>>> vals = [('Adam', 'Smith'), ('Zeta', 'Jones')]
>>> h = Heap(vals, key=lambda name: name[1])
>>> h.peek()  # Jones comes before Smith
('Zeta', 'Jones')
>>> h.push(('Aaron', 'Allen'))
>>> h.peek()
('Aaron', 'Allen')


Replace the top item with a new one.  Order changes.

>>> h.replace(('Annie', 'Sun'))
('Aaron', 'Allen')

>>> for ordered_name in h:
...     print(ordered_name)
('Zeta', 'Jones')
('Adam', 'Smith')
('Annie', 'Sun')

The heap is not changed:

>>> h.peek()
('Zeta', 'Jones')

Note that if you plan to iterate through the whole
Heap, sorting with the same key is more efficient:

>>> for ordered_name in sorted(h.raw(), key=lambda name: name[1]):
...     print(ordered_name)
('Zeta', 'Jones')
('Adam', 'Smith')
('Annie', 'Sun')

```

## Credit

Copyright (c) 2022 Michael Scott Asato Cuthbert

## License

MIT
