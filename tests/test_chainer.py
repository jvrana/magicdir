from magicdir import *
import pytest

def test_chain_list():

    x = ["the", "cow", "jumped"]
    x = MagicList(x)

    x.strip()
    print(x.replace("e", "a"))


def test_chain_equivalence():
    parent = MagicChain()
    assert parent.root == parent

    child = MagicChain(parent=parent)
    assert child.root == parent

    grandchild = MagicChain(parent=child)
    assert grandchild.root == parent

    assert not grandchild.is_root()
    assert not child.is_root()
    assert parent.is_root()

@pytest.fixture(params=[True, False])
def b(request):
    pushup = request.param
    a = MagicChain(push_up=pushup)
    a._create_child('b1', )
    a._create_child('c1', )
    a.b1._create_child('b2', )
    a.b1.b2._create_child('b3', )
    a.c1._create_child('c2', )

    assert hasattr(a.c1, 'c2', )
    assert hasattr(a, 'b1')
    assert hasattr(a.b1, 'b2')
    assert hasattr(a.b1.b2, 'b3')

    if not pushup:
        assert not hasattr(a, 'b2')
        assert not hasattr(a, 'b3')
        assert not hasattr(a, 'c2')
    else:
        assert hasattr(a, 'b2')
        assert hasattr(a, 'b3')
        assert hasattr(a, 'c2')

def test_chainer_add_child(b):
    pass


def test_chaining():
    a = MagicChain(push_up=True)
    a._create_child('b1', )
    a._create_child('c1', )
    a.b1._create_child('b2', )
    b3 = a.b1.b2._create_child('b3', )
    a.c1._create_child('c2', )

    assert set(a.descendents().alias) == set(['b1', 'c1', 'b2', 'b3', 'c2'])
    a.descendents()[1]
    set(a.descendents())
    assert set(b3.ancestors().alias) == set(['b2', 'b1', None])

    children = a.descendents()

    children += [1]
    assert type(children) is MagicList

def test_ancestors():
    a = MagicChain(push_up=True)
    a._create_child('b1', )
    a.b1._create_child('c1', )
    d1 = a.c1._create_child('d1', )

    assert len(a.descendents(include_self=False)) == 3
    assert len(a.descendents(include_self=True)) == 4

    assert len(d1.ancestors(include_self=False)) == 3
    assert len(d1.ancestors(include_self=True)) == 4

def test_remove():
    a = MagicChain(push_up=True)
    a._create_child('b1', )
    a.b1._create_child('c1', )
    a.c1._create_child('d1', )
    a.d1._create_child('e1')

    assert hasattr(a, 'b1')
    assert hasattr(a, 'c1')
    assert hasattr(a, 'd1')
    assert hasattr(a, 'e1')

    c1 = a.c1.delete()
    assert hasattr(a, 'b1')
    assert not hasattr(a, 'c1')
    assert not hasattr(a, 'd1')
    assert not hasattr(a, 'e1')

    assert hasattr(c1, 'd1')
    assert hasattr(c1, 'e1')
    assert c1.root is c1
    assert c1.d1.root is c1
    assert c1.e1.root is c1

def test_remove_children():
    a = MagicChain(push_up=True)
    a._create_child('b1', )
    a._create_child('b2', )
    a.b1._create_child('c1', )
    a.c1._create_child('d1', )
    a.d1._create_child('e1')

    assert hasattr(a, 'b1')
    assert hasattr(a, 'c1')
    assert hasattr(a, 'd1')
    assert hasattr(a, 'e1')

    a.children.delete()

    assert not hasattr(a, 'b2')
    assert not hasattr(a, 'b1')
    assert not hasattr(a, 'c1')
    assert not hasattr(a, 'd1')
    assert not hasattr(a, 'e1')


def test_set_raises_attr_error():

    a = MagicChain()
    a._create_child('b1')
    with pytest.raises(AttributeError):
        a.b1 = 4


# def test_attributes():
#     a = Chainer(push_up=True)
#     a._create_child('b1', )
#     a._create_child('b2')
#     a.b1._create_child('c1', )
#     d1 = a.c1._create_child('d1', )
#
#     assert set(d1.ancestor_attrs('alias')) == set(['b1', 'c1', None])
#     assert set(a.descendent_attrs('alias')) == set(['b1', 'b2', 'c1', 'd1'])
#     assert set(a.b1.descendent_attrs('alias')) == set(['c1', 'd1'])


