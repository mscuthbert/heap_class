'''
The same as the default implementation but without private imports.

list-like implementation of heap/PriorityQueue.
'''
from collections.abc import MutableSequence, Iterable, Iterator
from typing import TypeVar, Optional, Union
from heapq import heappop, heappush, heappushpop, heapreplace, heapify

HeapContents = TypeVar('HeapContents')


__version__ = '0.9.0b1'


class Heap(MutableSequence[HeapContents]):
    # noinspection PyShadowingBuiltins
    def __init__(self,
                 items: Union[HeapContents, Iterable[HeapContents]] = None,
                 *others,
                 max=False,  # pylint: disable=redefined-builtin
                 tup: Optional[bool] = None,
                 _set_no_check=False):
        self.max = max

        items: list[HeapContents]
        if others:
            items = [items] + list(others)
        elif not items:
            items = []

        if tup is None:
            if items is None:
                tup = False
            else:
                tup = isinstance(items[0], tuple)
        self.tup = tup
        if _set_no_check:
            self._heap = items
            return

        if self.max:
            items = [self._maxify(i) for i in items]

        if items:
            heapify(items)
        self._heap: list[HeapContents] = items

    def __getitem__(self, pos: int) -> HeapContents:
        '''
        Quite inefficient.
        '''
        if pos == 0:
            return self._maxify(self._heap[0])
        if pos < 0:
            pos = len(self) + pos

        for i, item in enumerate(self):
            if i == pos:
                return item
        raise IndexError('Heap index out of range')

    def __setitem__(self, pos: int, new_item: HeapContents) -> None:
        '''
        Quite inefficient.  Simply removes the item at that position
        and then appends a new one.  No guarantee at all that this will
        be true:  `h[3] = 9;  h[3] == 9`.
        '''
        if pos < 0:
            pos = len(self) + pos
        if pos > len(self):
            raise IndexError('Heap index out of range')

        new_items: list[HeapContents] = []
        for i, item in enumerate(self):
            if i != pos:
                new_items.append(self._maxify(item))  # we reverse maxification
            else:
                new_items.append(self._maxify(new_item))
        heapify(new_items)
        self._heap = new_items

    def __delitem__(self, pos) -> None:
        '''
        Quite inefficient
        '''
        if pos < 0:
            pos = len(self) + pos
        if pos > len(self):
            raise IndexError('Heap index out of range')

        new_items: list[HeapContents] = []
        for i, item in enumerate(self):
            if i != pos:
                new_items.append(self._maxify(item))  # we reverse maxification
        heapify(new_items)
        self._heap = new_items


    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __contains__(self, item: HeapContents) -> bool:
        return item in self._heap

    def __iter__(self) -> Iterator[HeapContents]:
        temp_heap = self._heap[:]
        while temp_heap:
            yield self._maxify(heappop(temp_heap))

    def __repr__(self) -> str:
        return f'Heap({list(self)}, max={self.max}, tup={self.tup})'

    def __reversed__(self) -> 'Heap[HeapContents]':
        return Heap(self.raw(), max=not self.max, tup=self.tup)

    def __sorted__(self, key=None) -> Iterator[HeapContents]:
        return iter(self)

    def _maxify(self, item: HeapContents) -> HeapContents:
        if not self.max:
            return item
        if not self.tup:
            return -item
        new_i = []
        for j in item:
            try:
                j = -j
            except TypeError:
                # might be a string or other non-invertible item.
                pass
            new_i.append(j)
        return tuple(new_i)

    def append(self, new_item: HeapContents) -> None:
        '''
        synonym for push -- to make it feel more list-like
        '''
        self.push(new_item)

    def clear(self) -> None:
        self._heap = []

    def copy(self) -> 'Heap[HeapContents]':
        return Heap(self._heap[:], max=self.max, tup=self.tup, _set_no_check=True)

    def count(self, item: HeapContents) -> int:
        return self._heap.count(item)

    def extend(self, others: Iterable[HeapContents]) -> None:
        for o in others:
            self.push(o)

    def index(self, item: HeapContents, start: int = 0, end: int = -1) -> int:
        '''
        Another inefficient operation
        '''
        for i, existing in self:
            if existing == item and i >= start and (end == -1 or i < end):
                return i

        raise ValueError(f'{item!r} is not in Heap')

    def insert(self, index: int, item: HeapContents) -> None:
        '''
        Index does not matter, except for checking input.
        '''
        if not isinstance(index, int):
            raise TypeError(
                f'{type(index).__name__}  object cannot be interpreted as an integer'
            )
        self.push(item)

    def peek(self) -> Optional[HeapContents]:
        return self._maxify(self._heap[0]) if self._heap else None

    def pop(self, index: int = 0) -> HeapContents:
        if not self._heap:
            raise IndexError('pop from empty Heap')

        if index < 0:
            index = len(self._heap) + index

        if index == 0:
            return self._maxify(heappop(self._heap))

        if index < 0 or index >= len(self._heap):
            raise IndexError('pop index out of range')

        # inefficient time.
        new_items = []
        o: HeapContents = self._heap[0]
        for i, item in enumerate(self):
            rev_item = self._maxify(item)
            if i == index:
                o = item
            else:
                new_items.append(rev_item)
        heapify(new_items)
        self._heap = new_items
        return o

    def push(self, new_item: HeapContents) -> None:
        heappush(self._heap, self._maxify(new_item))

    def pushpop(self, new_item: HeapContents) -> HeapContents:
        return self._maxify(heappushpop(self._heap, self._maxify(new_item)))

    def raw(self) -> list[HeapContents]:
        '''
        The `raw` method returns the contents of the heap in
        arbitrary order.  Useful for efficiently calling `set(h.raw())`.
        '''
        return [self._maxify(i) for i in self._heap]

    def remove(self, item: HeapContents) -> None:
        '''
        Note that if there are two items which are equal but also one is > the
        other (a very poor example of ordering) then the item removed
        might not be the same as if you iterated through the Heap and
        removed the smallest/largest item that equaled item.
        '''
        try:
            self._heap.remove(self._maxify(item))
        except ValueError:
            raise ValueError('Heap.remove(x): x not in Heap')
        heapify(self._heap)

    def replace(self, item: HeapContents) -> HeapContents:
        return heapreplace(self._heap, self._maxify(item))

    def reverse(self) -> None:
        self.max = not self.max
        self._heap = [self._maxify(i) for i in self._heap]
        heapify(self._heap)

    def sort(self, key=None) -> None:
        '''
        does nothing.
        '''
        pass
