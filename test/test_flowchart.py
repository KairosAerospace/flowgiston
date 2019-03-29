from unittest import TestCase
from flowgiston.base import *
from tempfile import TemporaryDirectory
import os


class TestFlowchart(TestCase):
    def test_base_class(self):
        f = FlowgistonChart()
        n1 = f.Generic.node("N1")
        n1.edge(f.Generic.node("N2"))
        with TemporaryDirectory() as td:
            f.save('test.gv', td)
            with open(os.path.join(td, 'test.gv'), 'r') as tf:
                v = tf.readlines()
                self.assertIn('digraph', v[0])
                self.assertIn('[label=N1 style=filled]', v[1])
                self.assertIn('[label=N2 style=filled]', v[2])
                self.assertIn('->', v[3])
