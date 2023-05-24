from flask import Flask, request, render_template
from rooting import *

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
        return render_template("orientation.html", edges="", orientation="", network_class=network_class)

    edges = edges.splitlines()
    edges = [e.split() for e in edges]
    edges = [(e[0], e[1]) for e in edges]

    network = nx.Graph(edges)

    orientations = LevelStuff(network, chain_length, class_checker)
    oriented_networks = [OrientationAlgorithmBinary(network,rootEdge,reticulations) for rootEdge, reticulations in orientations.items()]
    oriented_networks_edge_lists = [nx.to_edgelist(oriented_network) for oriented_network in oriented_networks]

    return render_template("orientation.html", edges=edges, orientation=oriented_networks_edge_lists, network_class=network_class)
