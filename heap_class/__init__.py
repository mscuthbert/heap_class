'''
list-like implementation of heap/PriorityQueue.
'''
from collections.abc import MutableSequence, Iterable, Iterator, Callable
from typing import TypeVar, Union, Optional, Any, cast
# noinspection PyUnresolvedReferences,PyProtectedMember
from heapq import (
    heappop, heappush, heappushpop, heapreplace, heapify,
    _heappop_max as heappop_max,
    _heapreplace_max as heapreplace_max,
    _heapify_max as heapify_max,
    _siftdown_max, _siftup_max
)

C_LANGUAGE_HEAP = (type(heappop_max).__name__ == 'builtin_function_or_method')


__version__ = '0.9.0b1'


HeapContents = TypeVar('HeapContents')


def heappush_max(heap, item):
    heap.append(item)
    _siftdown_max(heap, 0, len(heap)-1)


def heappushpop_max(heap, item):
    if C_LANGUAGE_HEAP:
        # if in C, fastest will probably be push then pop
        heappush_max(heap, item)
        return heappop_max(item)
    else:
        # do the manipulation efficiently but in Python
        if heap and heap[0] > item:
            item, heap[0] = heap[0], item
            _siftup_max(heap, 0)
        return item


class Heap(MutableSequence[HeapContents]):
    # noinspection PyShadowingBuiltins
    def __init__(self,
                 items: Union[HeapContents, Iterable[HeapContents]] = None,
                 *others,
                 max: bool = False,  # pylint: disable=redefined-builtin
                 key: Optional[Callable[[HeapContents], Any]] = None,
                 _replace_heap=False):
        self.max = max
        self.key = key

        items: list[Union[HeapContents], tuple[Any, HeapContents]]
        self._heap: list[Union[HeapContents], tuple[Any, HeapContents]]
        if _replace_heap:
            self._heap = items
            return

        if others:
            items = [items] + list(others)
        elif not items:
            items = []
        else:
            items = items[:]

        if self.key is not None:
            items = [self._add_key(i) for i in items]

        if items and self.max:
            heapify_max(items)
        elif items:
            heapify(items)
        self._heap = items

    def __getitem__(self, pos: int) -> HeapContents:
        '''
        Quite inefficient.
        '''
        if pos == 0:
            return self._del_key(self._heap[0])
        if pos < 0:
            pos = len(self) + pos

        for i, item in enumerate(self._iter_with_key()):
            if i == pos:
                return self._del_key(item)
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

        new_item = self._add_key(new_item)

        new_items: list[HeapContents] = []
        for i, item in enumerate(self._iter_with_key()):
            if i != pos:
                new_items.append(item)
            else:
                new_items.append(new_item)
        if self.max:
            heapify_max(new_items)
        else:
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

        new_items = []
        for i, item in enumerate(self._iter_with_key()):
            if i != pos:
                new_items.append(item)  # we reverse maxification
        if self.max:
            heapify_max(new_items)
        else:
            heapify(new_items)
        self._heap = new_items


    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __contains__(self, item: HeapContents) -> bool:
        return self._add_key(item) in self._heap

    def __iter__(self) -> Iterator[HeapContents]:
        for item in self._iter_with_key():
            yield self._del_key(item)

    def __repr__(self) -> str:
        return f'Heap({list(self)}, max={self.max})'

    def __reversed__(self) -> 'Heap[HeapContents]':
        return Heap(self.raw(), max=not self.max)

    def _add_key(self, item: HeapContents) -> Union[HeapContents, tuple[Any, HeapContents]]:
        if self.key is None:
            return item
        kv = self.key(item)
        return (kv, item)

    def _del_key(self, item: Union[HeapContents, tuple[Any, HeapContents]]) -> HeapContents:
        if self.key is None:
            return item
        else:
            return item[1]

    def _iter_with_key(self) -> Iterator[Union[tuple[Any, HeapContents], HeapContents]]:
        temp_heap = self._heap[:]
        while temp_heap:
            if self.max:
                yield heappop_max(temp_heap)
            else:
                yield heappop(temp_heap)

    def append(self, new_item: HeapContents) -> None:
        '''
        synonym for push -- to make it feel more list-like
        '''
        self.push(new_item)

    def clear(self) -> None:
        self._heap = []

    def copy(self) -> 'Heap[HeapContents]':
        return Heap(self._heap[:], max=self.max, key=self.key, _replace_heap=True)

    def count(self, item: HeapContents) -> int:
        return self._heap.count(self._add_key(item))

    def extend(self, others: Iterable[HeapContents]) -> None:
        for o in others:
            self.push(self._add_key(o))

    def index(self, item: HeapContents, start: int = 0, end: int = -1) -> int:
        '''
        Another inefficient operation
        '''
        keyed_item = self._add_key(item)
        for i, existing in self._iter_with_key():
            if existing == keyed_item and i >= start and (end == -1 or i < end):
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

    def peek(self) -> HeapContents:
        try:
            return self._del_key(self._heap[0])
        except IndexError:
            raise IndexError('peek on empty Heap') from None

    def pop(self, index: int = 0) -> HeapContents:
        if not self._heap:
            raise IndexError('pop from empty Heap')

        if index < 0:
            index = len(self._heap) + index

        if index == 0:
            if self.max:
                return self._del_key(heappop_max(self._heap))
            else:
                return self._del_key(heappop(self._heap))

        if index < 0 or index >= len(self._heap):
            raise IndexError('pop index out of range')

        # inefficient time.
        new_items = []
        o: HeapContents = self._heap[0]
        i = 0
        for i, item in enumerate(self._iter_with_key()):
            if i == index:
                o = self._del_key(item)
            else:
                new_items.append(item)

        if self.max:
            heapify_max(new_items)
        else:
            heapify(new_items)
        self._heap = new_items
        return o

    def push(self, new_item: HeapContents) -> None:
        if self.max:
            heappush_max(self._heap, self._add_key(new_item))
        else:
            heappush(self._heap, self._add_key(new_item))

    def pushpop(self, new_item: HeapContents) -> HeapContents:
        new_item = self._add_key(new_item)
        if self.max:
            o = heappushpop_max(self._heap, new_item)
        else:
            o = heappushpop(self._heap, new_item)
        return self._del_key(o)

    def raw(self) -> list[HeapContents]:
        '''
        The `raw` method returns the contents of the heap in
        arbitrary order.  Useful for efficiently calling `set(h.raw())`.
        '''
        return [self._del_key(i) for i in self._heap]

    def remove(self, item: HeapContents) -> None:
        '''
        Note that if there are two items which are equal but also one is > the
        other (a very poor example of ordering) then the item removed
        might not be the same as if you iterated through the Heap and
        removed the smallest/largest item that equaled item.
        '''
        try:
            self._heap.remove(self._add_key(item))
        except ValueError:
            raise ValueError('Heap.remove(x): x not in Heap')

        if self.max:
            heapify_max(self._heap)
        else:
            heapify(self._heap)

    def replace(self, item: HeapContents) -> HeapContents:
        '''
        Replace the first item with the new item.  Same as heapreplace
        '''
        item = self._add_key(item)
        if self.max:
            o = heapreplace_max(self._heap, item)
        else:
            o = heapreplace(self._heap, item)
        return self._del_key(o)

    def reverse(self) -> None:
        '''
        O(n) operation
        '''
        self.max = not self.max
        if self.max:
            heapify_max(self._heap)
        else:
            heapify(self._heap)

    def sort(self, key=None) -> None:
        '''
        does nothing.  Heaps are a form of sorted.
        '''
        pass
