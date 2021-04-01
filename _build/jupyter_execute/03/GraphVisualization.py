# Graph Visualization with ipycytoscape
This notebook demonstrates the visualization of subgraphs from the [Neo4j](https://neo4j.com/) Graph Database. It uses the [py2neo](https://py2neo.org/) library to access a Neo4j database instance.

The examples in this notebook access the [COVID-19-Net](https://github.com/covid-19-net/covid-19-community) Knowledge Graph.

Author: Peter W. Rose (pwrose@ucsd.edu)

!pip install ipycytoscape

!pip install py2neo==2021.0.1

import random
import ipycytoscape
from py2neo import Graph

#### Node and edge styles

node_centered = {'selector': 'node',
                 'style': {'font-size': '10',
                           'label': 'data(name)',
                           'height': '60',
                           'width': '80',
                           'text-max-width': '80',
                           'text-wrap': 'wrap',
                           'text-valign': 'center',
                           'background-color': 'blue',
                           'background-opacity': 0.6}
             }

edge_directed = {'selector': 'edge',
                 'style':  {'line-color': '#9dbaea',
                            'target-arrow-shape': 'triangle',
                            'target-arrow-color': '#9dbaea',
                            'curve-style': 'bezier'}
                }

edge_directed_named = {'selector': 'edge',
                       'style':  {'font-size': '8',
                                  'label': 'data(name)',
                                  'line-color': '#9dbaea',
                                  'text-rotation': 'autorotate',
                                  'target-arrow-shape': 'triangle',
                                  'target-arrow-color': '#9dbaea',
                                  'curve-style': 'bezier'}
                }

edge_undirected = {'selector': 'edge',
                   'style':  {'line-color': '#9dbaea'}
                  }

#### Node colors
Change seed to select a different color palette.

def random_color_palette(n_colors, seed=6):
    """ 
    Creates a random color palette of n_colors 
    See https://stackoverflow.com/questions/28999287/generate-random-colors-rgb
    
    """
    random.seed(seed)
    return ['#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(n_colors)]

### Connect to a Neo4j Database
Here we use the [COVID-19-Net](https://github.com/covid-19-net/covid-19-community) Knowledge Graph to demonstrate how to run a Neo4j Cypher query and pass the resulting subgraph into Cytoscape.

graph = Graph("bolt://132.249.238.185:7687", user="reader", password="demo")

### Example 1: Find all cities with the name "San Francisco"
This query demonstrates the geographic hierachy in COVID-19-Net.

query1 = """
MATCH p=(:City{name:'Skopje'})-[:IN*]->(:World) RETURN p
"""
subgraph1 = graph.run(query1).to_subgraph()

#### Add Neo4j subgraph to Cytoscape Widget

widget1 = ipycytoscape.CytoscapeWidget()
widget1.graph.add_graph_from_neo4j(subgraph1)

#### Set node and edge styles

style1 = [node_centered, edge_directed]

#### Set node specific colors based on node labels

labels1 = list(subgraph1.labels())
print('Node labels:', labels1)

colors1 = random_color_palette(len(labels1))

for label, color in zip(labels1, colors1):
    style1.append({'selector': 'node[label = "' + label + '"]', 'style': {'background-color': color}})

widget1.set_style(style1)

widget1.set_layout(name='dagre', padding=0)

When a Neo4j subgraph is added to a Cytoscape graph, a tooltip attribute is generated that contains all Neo4j node properties.

widget1.set_tooltip_source('tooltip')

Click on a node to show the tooltip

widget1

### Example 2: Find all proteins that interact with the SARS-CoV-2 Spike protein
Here we run an undirected query (no "->" arrow) since the direction of interaction is arbitrary.

query2 = """
MATCH p=(:Protein{name: 'Spike glycoprotein', taxonomyId: 'taxonomy:2697049'})-[:INTERACTS_WITH]-(:Protein) RETURN p
"""
subgraph2 = graph.run(query2).to_subgraph()

widget2 = ipycytoscape.CytoscapeWidget()
widget2.graph.add_graph_from_neo4j(subgraph2)

style2 = [node_centered, edge_undirected]

labels2 = list(subgraph2.labels())
print('Node labels:', labels2)

colors2 = random_color_palette(len(labels2))

for label, color in zip(labels2, colors2):
    style2.append({'selector': 'node[label = "' + label + '"]', 'style': {'background-color': color}})

widget2.set_style(style2)

widget2.set_layout(name='concentric', padding=0)

widget2.set_tooltip_source('tooltip')

Click on a node to show the tooltip

widget2

### Example 3: Explore the Data Sources used to create the COVID-19-Net Knowledge Graph

query3 = """
MATCH p=(:MetaNode)-[:ETL_FROM]->(:DataSource) RETURN p  // ETL_FROM: Extracted, transformed, and loaded FROM
"""
subgraph3 = graph.run(query3).to_subgraph()

widget3 = ipycytoscape.CytoscapeWidget()
widget3.graph.add_graph_from_neo4j(subgraph3)

style3 = [node_centered, edge_directed]

labels3 = list(subgraph3.labels())
print('Node labels:', labels3)

colors3 = random_color_palette(len(labels3))

for label, color in zip(labels3, colors3):
    style3.append({'selector': 'node[label = "' + label + '"]', 'style': {'background-color': color}})

widget3.set_style(style3)

widget3.set_layout(name='klay', padding=0)

widget3.set_tooltip_source('tooltip')

Click on a node to show the tooltip

widget3

### Example 4: Create a Metagraph that shows the Nodes and their Relationships in the COVID-19-Net Knowledge Graph

query4 = """
MATCH p=(a:MetaNode)-[:META_RELATIONSHIP]->(b:MetaNode) 
WHERE a.name <> 'Location' AND b.name <> 'Location' // exclude Location nodes since they make the graph too crowded
RETURN p
"""
subgraph4 = graph.run(query4).to_subgraph()

widget4 = ipycytoscape.CytoscapeWidget()
widget4.graph.add_graph_from_neo4j(subgraph4)

style4 = [node_centered, edge_directed_named]

labels4 = list(subgraph4.labels())
print('Node labels:', labels4)

colors4 = random_color_palette(len(labels4))

for label, color in zip(labels4, colors4):
    style4.append({'selector': 'node[label = "' + label + '"]', 'style': {'background-color': color}})

widget4.set_style(style4)

Cola layout [options](https://github.com/cytoscape/cytoscape.js-cola#api)

widget4.set_layout(name='cola', padding=0, nodeSpacing=65, nodeDimensionsIncludeLabels=True, unconstrIter=5000)

widget4.set_tooltip_source('tooltip')

Click on a node to show the node tooltip

widget4

