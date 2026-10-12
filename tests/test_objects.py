from objects.GraphObjects import *


def test_next_smallest_multiple():
    assert next_smallest_multiple(11, 13) == 0
    assert next_smallest_multiple(23, 2) == 22
    assert next_smallest_multiple(23, 1) == 23
    assert next_smallest_multiple(2323, 2323) == 2323
    assert next_smallest_multiple(-13, 2) == -14
    assert next_smallest_multiple(-13, 13) == -13


def test_GridLines():
    a = GridLines()
    assert [a.xDist, a.yDist, a.width] == [50, 50, 3]

    a = GridLines(100)
    assert [a.xDist, a.yDist, a.width] == [100, 100, 3]

    a = GridLines((200, 300))
    assert [a.xDist, a.yDist, a.width] == [200, 300, 3]

    a = GridLines(100, 5)
    assert [a.xDist, a.yDist, a.width] == [100, 100, 5]

    a = GridLines((100, 300), 5)
    assert [a.xDist, a.yDist, a.width] == [100, 300, 5]

    a = GridLines(100, 200, 5)
    assert [a.xDist, a.yDist, a.width] == [100, 200, 5]


def test_Pos():
    a = Pos()
    assert Pos() != Pos()
    assert str(a) == "(None, None)"
    assert repr(a) == "Pos(None, None)"

    a = Pos(10, 13)
    b = Pos(2, 2)

    assert b != a
    assert str(a) == "(10, 13)"
    assert repr(a) == "Pos(10, 13)"

    assert a.x == a[0] == 10
    assert a.y == a[1] == 13

    assert a.pos == Pos(10, 13) == (a.x, a.y) == (10, 13)

    a[0] = b.x
    assert a.pos == Pos(2, 13) == (a.x, a.y) == (2, 13)





