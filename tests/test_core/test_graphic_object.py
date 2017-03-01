import unittest

from brown.core import brown
from brown.utils.units import GraphicUnit
from brown.utils.point import Point
from brown.core.pen import Pen
from brown.core.brush import Brush
from brown.core.paper import Paper
from brown.utils.units import Mm
from brown.core.flowable_frame import FlowableFrame


from mock_graphic_object import MockGraphicObject


class TestGraphicObject(unittest.TestCase):

    def setUp(self):
        brown.setup(
            Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.frame = FlowableFrame((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_init(self):
        mock_pen = Pen('#ffffff')
        mock_brush = Brush('#eeeeee')
        mock_parent = MockGraphicObject((10, 11), parent=None)
        grob = MockGraphicObject(
            (5, 6), GraphicUnit(7), mock_pen, mock_brush, mock_parent)
        assert(grob.pos.x == grob.x)
        assert(grob.x == GraphicUnit(5))
        assert(grob.pos.y == grob.y)
        assert(grob.y == GraphicUnit(6))
        assert(grob.breakable_width == GraphicUnit(7))
        assert(grob.parent == mock_parent)

    def test_pos_setter_changes_x(self):
        grob = MockGraphicObject((5, 6))
        grob.pos = Point(7, 8)
        assert(grob.pos.x == GraphicUnit(7))
        assert(grob.pos.y == GraphicUnit(8))

    def test_map_from_origin(self):
        item = MockGraphicObject((5, 6, 2))
        relative_pos = MockGraphicObject.map_from_origin(item)
        assert(relative_pos.x.value == 5)
        assert(relative_pos.y.value == 6)
        assert(relative_pos.page == 2)

    def test_map_from_origin_through_parent(self):
        parent = MockGraphicObject((100, 101))
        item = MockGraphicObject((5, 6), parent=parent)
        relative_pos = MockGraphicObject.map_from_origin(item)
        assert(relative_pos.x.value == 105)
        assert(relative_pos.y.value == 107)

    def test_map_between_items(self):
        source = MockGraphicObject((5, 6, 1))
        destination = MockGraphicObject((100, 100, 4))
        relative_pos = MockGraphicObject.map_between_items(source, destination)
        assert(relative_pos.x.value == 95)
        assert(relative_pos.y.value == 94)
        assert(relative_pos.page == 3)

    def test_map_between_items_through_parent(self):
        parent = MockGraphicObject((100, 102, 7))
        source = MockGraphicObject((5, 6, 1), parent=parent)
        destination = MockGraphicObject((1, 1, 4))
        relative_pos = MockGraphicObject.map_between_items(source, destination)
        assert(relative_pos.x.value == -104)
        assert(relative_pos.y.value == -107)
        assert(relative_pos.page == -4)

    def test_register_child(self):
        parent = MockGraphicObject((0, 0))
        child = MockGraphicObject((0, 0))
        parent._register_child(child)
        assert(child in parent.children)

    def test_unregister_child(self):
        parent = MockGraphicObject((0, 0))
        child = MockGraphicObject((0, 0))
        parent.children = {child}
        parent._unregister_child(child)
        assert(child not in parent.children)

    def test_setting_parent_registers_self_with_parent(self):
        parent = MockGraphicObject((0, 0))
        child = MockGraphicObject((0, 0), parent=parent)
        assert(child in parent.children)
