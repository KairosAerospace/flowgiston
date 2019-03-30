from uuid import uuid4
from graphviz import Digraph


def flowgiston_base():
    """
    Returns an instance of the FlowgistonBase class.  Subclassing this class allows users to apply their own
     styling and those classes will be made available in instances of FlowgistonChart associated with this class.
    Returns: A class of type FlowgistonBase

    """

    class FlowgistonBase:
        # copied from here: https://www.graphviz.org/doc/info/attrs.html
        __GV_NODE_ATTRIBS = [
            'area', 'color', 'comment', 'colorscheme', 'distortion', 'fillcolor', 'fixedsize', 'fontcolor', 'fontname',
            'gradientangle', 'group', 'height', 'href', 'id', 'image', 'imagepos', 'imagescale', 'labelloc', 'layer',
            'margin', 'nojustify', 'ordering', 'penwidth', 'peripheries', 'pin', 'pos', 'rects', 'regular', 'root',
            'samplepoints', 'shape', 'shapefile', 'showboxes', 'sides', 'skew', 'sortv', 'style', 'target', 'tooltip',
            'width', 'vertices', 'xlabel', 'xlp', 'z'
        ]
        # All node types should inherit from this type
        style = 'filled'

        def __init__(self, fchart: 'FlowgistonChart'):
            """
            No need to call this, it gets called automagically when you create a flowchart.
            Args:
                fchart: A FlowgistonChart
            """
            self.fchart = fchart

            # populate style features from the class
            self._base_style = {}
            for a in self.__GV_NODE_ATTRIBS:
                if hasattr(self, a):
                    self._base_style[a] = getattr(self, a)

        def _construct_style(self, **kwargs):
            """
            Constructs a style dict from the passed kwargs and the base style
            Args:
                **kwargs: keyword args to pass for node styling

            Returns: dict

            """
            style = self._base_style.copy()
            style.update(kwargs)
            return style

        def _name(self):
            """
            Returns a random name for this node.
            Returns: str

            """
            return 'n_' + uuid4().hex

        def _nodegen(self, label: str, **kwargs) -> 'FlowgistonNode':
            """
            Wraps the graphviz node creation.
            Args:
                label: Label for this node.  If it's None, checks to see if there's a label in the keyword args or on the class attributes, in that order.
                kwargs**: keyword args to pass for node styling
            Returns: a new FlowgistonNode corresponding to this object

            """
            name = self._name()
            if label is None:
                label = kwargs.get('label', None)
            if label is None:
                label = getattr(self, 'label', None)

            self.fchart.graph.node(name, label=label, **self._construct_style(**kwargs))
            return FlowgistonNode(name, label, self)

        def conditional(self, label: str, **kwargs) -> 'FlowgistonNode':
            """
            Generate a conditional node (diamond)
            Args:
                label: Label for this node
                **kwargs: keyword args to pass for node styling

            Returns: A conditional FlowgistonNode

            """
            return self._nodegen(label, shape='diamond', **kwargs)

        # shorthand for conditional
        def if_(self, label: str, **kwargs) -> 'FlowgistonNode':
            """
            Shorthand for conditional
            Args:
                label: Label for this node
                **kwargs: keyword args to pass for node styling

            Returns: A conditional FlowgistonNode

            """
            return self.conditional(label, **kwargs)

        def process(self, label: str, **kwargs):
            """
            Create a process node (rectangle)
            Args:
                label: Label for this node
                **kwargs: keyword args to pass for node styling

            Returns: A process FlowgistonNode

            """
            return self._nodegen(label, shape='box', **kwargs)

        def yes(self, node: 'FlowgistonNode', **kwargs) -> 'FlowgistonNode':
            """
            Generates an outbound edge to another node labeled 'Yes'
            Args:
                node: The destination node
                **kwargs: Keyword args for styling this edge

            Returns: The destination FlowgistonNode

            """
            self.fchart.yes(self, node, **kwargs)

        def no(self, node, **kwargs) -> 'FlowgistonNode':
            """
            Generates an outbound edge to another node labeled 'No'
            Args:
                node: The destination node
                **kwargs: Keyword args for styling this edge

            Returns: The destination FlowgistonNode

            """
            self.fchart.no(self, node, **kwargs)

        def node(self, label=None, **kwargs) -> 'FlowgistonNode':
            """
            Generates a generic node with the default styling for the class
            Args:
                label: An optional label for this node
                **kwargs: Keyword args for styling this node

            Returns: A FlowgistonNode

            """
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
        self.Generic = self.flowgiston_base_klass(self)
        for klass in self.flowgiston_base_klass.__subclasses__():
            setattr(self, klass.__name__, klass(self))

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
