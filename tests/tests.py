from unittest import TestCase

from heap_class import Heap

class TestHeap(TestCase):
    def test_basic(self):
        h = Heap([40, 30, 20])
        self.assertEqual(h[0], 20)
        out = h.pop()
        self.assertEqual(out, 20)
        self.assertEqual(h[0], 30)
        self.assertFalse(h.max)

        h.reverse()
        self.assertTrue(h.max)
        self.assertEqual(h[0], 40)
        self.assertEqual(h.pop(), 40)
        self.assertEqual(h.pop(), 30)
        self.assertFalse(h)

        h.push(10)
        h.push(20)
        self.assertEqual(list(h), [20, 10])

    def test_docs(self):
        h = Heap([3, 1, 9, 20], max=True)
        self.assertEqual(h.pop(), 20)
        self.assertEqual(h.peek(), 9)
        self.assertIsNone(h.push(17))
        self.assertEqual(h[0], 17)
        # inefficient, but works
        self.assertEqual(h[1], 9)

        y = reversed(h)
        self.assertIsInstance(y, Heap)
        self.assertEqual(y.peek(), 1)
        self.assertEqual(repr(y), 'Heap([1, 3, 9, 17], max=False)')
        self.assertIn(9, y)
        # cannot test y.raw() for equality since it can
        # be heapified in different ways.
        self.assertEqual(set(y.raw()), {1, 3, 9, 17})

    def test_docs_tuple(self):
        h = Heap([(6, 4), (6, 9), (10, 2)], max=True)
        self.assertEqual(h.pop(), (10, 2))
        self.assertEqual(h.pop(), (6, 9))

        h2 = Heap([('aa', 4), ('aa', 5), ('zz', 2), ('zz', 1)], max=True)
        self.assertEqual(h2.pop(), ('zz', 2))

        vals = [('Adam', 'Smith'), ('Zeta', 'Jones')]
        h3 = Heap(vals, key=lambda name: name[1])
        self.assertEqual(h3.peek(), ('Zeta', 'Jones'))
        h3.push(('Aaron', 'Allen'))
        self.assertEqual(h3.peek(), ('Aaron', 'Allen'))
        self.assertEqual(h3.replace(('Annie', 'Sun')), ('Aaron', 'Allen'))
        self.assertEqual(h3.peek(), ('Zeta', 'Jones'))
        self.assertEqual(
            list(h3),
            [('Zeta', 'Jones'), ('Adam', 'Smith'), ('Annie', 'Sun')]
        )
        self.assertEqual(
            list(sorted(h3.raw(), key=lambda name: name[1])),
            [('Zeta', 'Jones'), ('Adam', 'Smith'), ('Annie', 'Sun')]
        )




