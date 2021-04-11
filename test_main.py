import pytest

from main import Tree


@pytest.mark.parametrize("size", [10, 100, 1000, 2000, 4000])
@pytest.mark.parametrize("step", [1, 2, 5, 10, 20])
def test_add_and_search(size, step):
    tree = Tree()
    for element in range(0, size, step):
        tree.add(element)
    for element in range(0, size, step):
        assert tree.search(element)
    for element in range(10000, 10010):
        assert not tree.search(element)


@pytest.mark.parametrize("size", [10, 100, 1000, 2000, 4000])
@pytest.mark.parametrize("step", [1, 2, 5, 10, 20])
def test_add_and_order(size, step):
    tree = Tree()
    for element in range(0, size, step):
        tree.add(element)
    assert tree.inorder() == list(range(0, size, step))
