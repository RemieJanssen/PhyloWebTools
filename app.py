from flask import Flask

from tools.rooting.rooting_page import orientation_routes
from tools.draw_graphs import drawing_routes

app = Flask(__name__)
app.register_blueprint(orientation_routes)
app.register_blueprint(drawing_routes)



