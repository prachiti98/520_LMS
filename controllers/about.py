from flask.templating import render_template
from flask import Blueprint

about_blueprint = Blueprint('about_blueprint', __name__)


@about_blueprint.route("/about")
def about():
    return render_template("about.html")