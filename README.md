# Flowgiston: Dead Easy Flowcharts in Python 
Flowgiston is a simple wrapper around GraphViz for making frustration-free 
flowcharts in Jupyter Notebook.
Here's an [example](https://github.com/KairosAerospace/flowgiston/blob/master/example/Example.ipynb):
![alt text](https://github.com/KairosAerospace/flowgiston/raw/master/example/example.png "Example")

## Getting started
### Install

```
$ pip install flowgiston
```

### Nodes and custom styles
Chart building is easiest in Jupyter Notebook.  Charts will automatically render 
inline if you simply make the chart the last line of your notebook cell, as below:
```python
from flowgiston import FlowgistonChart
chart = FlowgistonChart()
chart.node("Hello, world")
chart

```

To create custom styled nodes, subclass the FlowgistonBase class, and your subclasses will automatically be added to the chart instance:
```python
from flowgiston import FlowgistonChart, flowgiston_base
Base = flowgiston_base()
class MyCustomNode(Base):
    style = 'filled,dashed'
    fillcolor = 'lightblue'
    
class Stop(Base):
    fillcolor = 'red'
    fontcolor = 'white'
    shape = 'octagon'
    
chart = FlowgistonChart(Base)
start = chart.MyCustomNode.start("Get it on")
start.edge(chart.Stop.node("STAHHHHP"))
chart
```

### Edges
Edges can be created between nodes in several ways.
```python
chart.edge(node1, node2, 'do it') # create a labeled edge from node1 to node2
node3 = node1.edge(chart.node('a third node'), 'do it more') # same, but more functional
node1.yes(node3) # create an edge labeled 'yes'


```


