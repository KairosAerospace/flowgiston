from unittest import TestCase
from flowgiston.base import *
from tempfile import TemporaryDirectory
import os


class TestFlowchart(TestCase):
    def test_base_class(self):
        f = FlowgistonChart()
        n1 = f.Generic.node("N1")
        n2 = n1.edge(f.Generic.node("N2"))
        with TemporaryDirectory() as td:
            f.save('test.gv', td)
            with open(os.path.join(td, 'test.gv'), 'r') as tf:
                v = tf.readlines()
                self.assertIn('digraph', v[0])
                self.assertIn('[label=N1 style=filled]', v[1])
                self.assertIn('[label=N2 style=filled]', v[2])
                self.assertIn('->', v[3])

        n3 = n2.edge(f.Generic.if_("N3"), fillcolor='blue')
        with TemporaryDirectory() as td:
            f.save('test.gv', td)
            with open(os.path.join(td, 'test.gv'), 'r') as tf:
                v = tf.readlines()
                n3_txt = [x for x in v if 'N3' in x]
                self.assertEqual(len(n3_txt), 1)
                self.assertIn('shape=diamond', n3_txt[0])
