from flask import Flask, request, render_template, Markup
from rooting import *
import networkx as nx
import json

app = Flask(__name__)

class_checker_dict = {
    "TC": (ClassTreeChild, 3),
    "SF": (ClassStackFree, 3),
    "O": (ClassOrchard, 3),
    "TB": (ClassTreeBased, 2),
    "default": (ClassAllNetworks, 1),
}



@app.route("/orientation")
def _orientation_page():
    """Return the orientation page.
    This page contains a form field for the user to enter a list of edges of an undirected graph.
    The user can also select a class of graphs to restrict type of oriented graph that is requested.
    This list and the graph class is sent to this page again as a GET request, and the orientation of the graph is returned in a text field and as a graphviz svg picture.
    """
    edges = request.args.get("edges", "")
    network_class = request.args.get("class", "")
    class_checker, chain_length = class_checker_dict.get(network_class, class_checker_dict["default"])
    if not edges:
        return render_template("orientation.html", edges="", orientations=None, network_class=network_class, show_results=False)

    edges = edges.splitlines()
    edges = [e.split() for e in edges]
    edges = [(e[0], e[1]) for e in edges]

    network = nx.Graph(edges)

    orientations = LevelStuff(network, chain_length, class_checker) or dict()
    oriented_networks = [OrientationAlgorithmBinary(network,rootEdge,reticulations) for rootEdge, reticulations in orientations.items()]
    oriented_networks_edge_lists = [json.dumps([e for e in oriented_network.edges]) for oriented_network in oriented_networks]

    return render_template("orientation.html", edges=edges, orientations=oriented_networks_edge_lists, network_class=network_class, show_results=True)

@app.route("/draw_oriented_network")
def _draw_oriented_network():
    """Takes a list of edges and returns a graphviz svg picture of the graph.
    Each node is labeled with its label.
    """
    edges = request.args.get("edges", "[]")
    edges = json.loads(edges)
    network = nx.DiGraph(edges)
    network_svg = nx.nx_agraph.to_agraph(network).draw(format="svg", prog="dot")
    return Markup(network_svg)
