from flask import Flask, request, render_template, url_for, Blueprint
from .rooting import *
import networkx as nx
import json
from urllib.parse import unquote

orientation_routes = Blueprint("orient_network", __name__)

class_checker_dict = {
    "TC": (ClassTreeChild, 3),
    "SF": (ClassStackFree, 3),
    "O": (ClassOrchard, 3),
    "TB": (ClassTreeBased, 2),
    "default": (ClassAllNetworks, 1),
}

@orientation_routes.route("/orientation")
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
        return render_template("orientation.html", edges="", network_class=network_class, data_url="", show_results=False)

    edges = edges.splitlines()
    edges = [e.split() for e in edges]
    edges = [(e[0], e[1]) for e in edges]

    data_url = url_for("orient_network._get_orientations", edges=json.dumps(edges), network_class=network_class)

    return render_template("orientation.html", data_url=data_url, edges=json.dumps(edges), show_results=True)

@orientation_routes.route("/get_orientations")
def _get_orientations():
    edges = request.args.get("edges", "[]")
    edges = unquote(edges)
    edges = json.loads(edges)
    if not edges:
        return json.dumps([])

    network_class = request.args.get("network_class", "")
    class_checker, chain_length = class_checker_dict.get(network_class, class_checker_dict["default"])

    network = nx.Graph(edges)

    orientations = LevelStuff(network, chain_length, class_checker) or dict()
    oriented_networks = [OrientationAlgorithmBinary(network,rootEdge,reticulations) for rootEdge, reticulations in orientations.items()]
    oriented_networks_edge_lists = [json.dumps([e for e in oriented_network.edges]) for oriented_network in oriented_networks]

    results = []
    for (root, reticulations), edge_list in zip(orientations.items(), oriented_networks_edge_lists):
        results.append({
            "root": root,
            "reticulations": reticulations,
            "edges": edge_list,
        })
    return json.dumps(results)
