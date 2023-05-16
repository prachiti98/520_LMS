from flask.templating import render_template
from flask import Blueprint

about_blueprint = Blueprint('about_blueprint', __name__)


@index_blueprint.route("/about")
def index():
    return render_template("about.html")