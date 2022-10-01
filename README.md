# heap_class

list-like implementation of heap/PriorityQueue

# Usage

```python3
>>> from heap_class import Heap
>>> h = Heap([3, 1, 9, 20], max=True)
>>> h.pop()
20
>>> h.peek()
9
>>> h.push(17)  # or h.append(17)
>>> h.peek()
17
>>> h[0]
17
>>> h[1]  # inefficient, but works
9
>>> y = reversed(h)
>>> y.peek()
1
>>> y  # repr is inefficient, but correct
Heap([1, 3, 9, 17], max=False, tup=False)
>>> 9 in y
True
>>> y.raw()  # heap structure
[1, 3, 17, 9]
>>> set(y.raw())  # raw helpful for fast casting
{1, 3, 17, 9}

Tuples and *args creation supported.

>>> h = Heap((6,4), (6,9), (10,2), max=True)
>>> h.pop()
(10, 2)
>>> h.pop()
(6, 9)
```

## Credit

Copyright (c) 2022 Michael Scott Asato Cuthbert

## License

MIT
