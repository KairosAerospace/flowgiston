from unittest import TestCase
from flowgiston.base import *
from tempfile import TemporaryDirectory
import os
import pydot


class TestFlowchart(TestCase):
    def test_base_class(self):
        f = FlowgistonChart()
        n1 = f.Generic.node("N1")
        n2 = n1.edge(f.Generic.node("N2"))

        with TemporaryDirectory() as td:
            f.save('test.gv', td)
            with open(os.path.join(td, 'test.gv'), 'r') as tf:
                g = pydot.graph_from_dot_data(tf.read())[0]
                self.assertEqual(g.get_node(n1.name)[0].get_attributes()['label'], n1.label)
                self.assertEqual(g.get_node(n2.name)[0].get_attributes()['label'], n2.label)
                self.assertEqual(len(g.get_edges()), 1)
            n3 = n2.edge(f.Generic.if_("N3"), fillcolor='blue')
            with TemporaryDirectory() as td:
                f.save('test.gv', td)
                with open(os.path.join(td, 'test.gv'), 'r') as tf:
                    g = pydot.graph_from_dot_data(tf.read())[0]
                    n3_attribs = g.get_node(n3.name)[0].get_attributes()
                    self.assertEqual(n3_attribs['label'], n3.label)
                    self.assertEqual(n3_attribs['shape'], 'diamond')

                    #         v = tf.readlines()
                    #         n3_txt = [x for x in v if 'N3' in x]
                    #         self.assertEqual(len(n3_txt), 1)
                    #         self.assertIn('shape=diamond', n3_txt[0])
