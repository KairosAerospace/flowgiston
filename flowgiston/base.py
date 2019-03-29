from uuid import uuid4
from graphviz import Digraph


def flowgiston_base():
    class FlowgistonBase:
        __STYLE_ATTRIBS = ['style', 'shape', 'fillcolor', 'fontcolor']
        style = 'filled'

        def __init__(self, fchart: 'FlowgistonChart'):
            self.fchart = fchart

            # populate style features from the class
            self._base_style = {}
            for a in FlowgistonBase.__STYLE_ATTRIBS:
                if hasattr(self, a):
                    self._base_style[a] = getattr(self, a)

        def _construct_style(self, **kwargs):
            style = self._base_style.copy()
            style.update(kwargs)
            return style

        def _name(self):
            return 'n_' + uuid4().hex

        def _nodegen(self, label, **kwargs):
            name = self._name()
            self.fchart.graph.node(name, label=label, **self._construct_style(**kwargs))
            return FlowgistonNode(name, label, self)

        def conditional(self, label, **kwargs):
            return self._nodegen(label, shape='diamond', **kwargs)

        # shorthand for conditional
        def if_(self, label, **kwargs):
            return self.conditional(label, **kwargs)

        def process(self, label, **kwargs):
            return self._nodegen(label, shape='box', **kwargs)

        def yes(self, node, **kwargs):
            self.fchart.yes(self, node, **kwargs)

        def no(self, node, **kwargs):
            self.fchart.no(self, node, **kwargs)

        def node(self, label, **kwargs):
            return self._nodegen(label, **kwargs)

    return FlowgistonBase


class FlowgistonChart:
    # renders the graph in Jupyter
    def _repr_svg_(self):
        return self.graph._repr_svg_()

    def __init__(self, flowgiston_base_klass=None):
        self.graph = Digraph()

        if flowgiston_base_klass is None:
            self.flowgiston_base_klass = flowgiston_base()
        else:
            self.flowgiston_base_klass = flowgiston_base_klass
        for klass in self.flowgiston_base_klass.__subclasses__():
            setattr(self, klass.__name__, klass(self))
        self.Generic = self.flowgiston_base_klass(self)

    def edge(self, n1, n2, label, **kwargs):
        self.graph.edge(n1.name, n2.name, label, **kwargs)

    def yes(self, n1, n2, **kwargs):
        self.edge(n1, n2, 'Yes', **kwargs)

    def no(self, n1, n2, **kwargs):
        self.edge(n1, n2, 'No', **kwargs)

    def render(self, filename=None, directory=None, view=False, cleanup=False, format=None, renderer=None,
               formatter=None):
        return self.graph.render(filename=filename, directory=directory, view=view, cleanup=cleanup, format=format,
                                 renderer=renderer, formatter=formatter)

    def save(self, filename=None, directory=None):
        return self.graph.save(filename=filename, directory=directory)


class FlowgistonNode:
    def __init__(self, name, label, flowbase: 'FlowgistonBase'):
        self.name = name
        self.label = label
        self.flowbase = flowbase

    def edge(self, node, label=None, **kwargs):
        self.flowbase.fchart.graph.edge(self.name, node.name, label=label, **kwargs)
        return node

    def yes(self, node, **kwargs):
        self.edge(node, label='Yes', **kwargs)
        return node

    def no(self, node, **kwargs):
        self.edge(node, label='No', **kwargs)
        return node
