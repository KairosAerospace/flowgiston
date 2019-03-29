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
            n3 = n2.edge(f.Generic.if_("N3", fillcolor='blue'))
            with TemporaryDirectory() as td:
                f.save('test.gv', td)
                with open(os.path.join(td, 'test.gv'), 'r') as tf:
                    g = pydot.graph_from_dot_data(tf.read())[0]
                    n3_attribs = g.get_node(n3.name)[0].get_attributes()
                    self.assertEqual(n3_attribs['label'], n3.label)
                    self.assertEqual(n3_attribs['shape'], 'diamond')
                    self.assertEqual(n3_attribs['fillcolor'], 'blue')

    def test_inheritance(self):
        Base = flowgiston_base()

        class BlueNode(Base):
            fillcolor = 'blue'

        class Stop(Base):
            fillcolor = 'red'
            fontcolor = 'white'
            shape = 'octagon'
            label = 'STOP'

        f = FlowgistonChart(Base)

        b = f.BlueNode.if_('This is a blue node')
        s = b.yes(f.Stop.node())
        r = f.Generic.process('Generic node', style='dashed')

        f.edge(b, r, "foo")

        # test overriding of default label
        s1 = f.Stop.node("STAHHHHP")

        with TemporaryDirectory() as td:
            f.save('test.gv', td)
            with open(os.path.join(td, 'test.gv'), 'r') as tf:
                g = pydot.graph_from_dot_data(tf.read())[0]
                stop_attrs = g.get_node(s.name)[0].get_attributes()

                # check that it gets the default label from the class variable
                self.assertEqual(stop_attrs['label'], Stop.label)

                # check that it inherits the other variables
                self.assertEqual(stop_attrs['fontcolor'], Stop.fontcolor)
                self.assertEqual(stop_attrs['shape'], Stop.shape)
                self.assertEqual(stop_attrs['fillcolor'], Stop.fillcolor)

                blue_attrs = g.get_node(b.name)[0].get_attributes()
                self.assertEqual(blue_attrs['fillcolor'], BlueNode.fillcolor)

                self.assertEqual(g.get_node(s1.name)[0].get_attributes()['label'], "STAHHHHP")

                edges = g.get_edges()
                self.assertTrue(len(edges), 2)
                d = {e.get_destination(): e for e in edges}
                self.assertEqual(d[s.name].get_attributes()['label'], 'Yes')
                self.assertEqual(d[r.name].get_attributes()['label'], 'foo')
