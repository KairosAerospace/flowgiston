from unittest import TestCase
from flowgiston.base import *
class TestFlowchart(TestCase):

    def test_base_class(self):
        f = FlowgistonChart()
        n1 = f.Generic.node("N1")
        n1.edge(f.Generic.node("N2"))
