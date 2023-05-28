from flask import Flask, request, Markup, Blueprint
import networkx as nx
import json

drawing_routes = Blueprint("draw_graph", __name__)

@drawing_routes.route("/draw_undirected_network")
def _draw_undirected_network():
    """Takes a list of edges and returns a graphviz svg picture of the graph.
    Each node is labeled with its label.
    """
    edges = request.args.get("edges", "[]")
    edges = json.loads(edges)
    network = nx.Graph(edges)
    network_svg = nx.nx_agraph.to_agraph(network).draw(format="svg", prog="neato").decode('ascii')
    return Markup(network_svg)


@drawing_routes.route("/draw_oriented_network")
def _draw_oriented_network():
    """Takes a list of edges and returns a graphviz svg picture of the graph.
    Each node is labeled with its label.
    """
    edges = request.args.get("edges", "[]")
    edges = json.loads(edges)
    network = nx.DiGraph(edges)
    graphviz_network = nx.nx_agraph.to_agraph(network)
    network_svg = graphviz_network.draw(format="svg", prog="dot").decode('ascii')
    return Markup(network_svg)
