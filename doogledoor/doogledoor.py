from flask import Blueprint, render_template

doog = Blueprint("doogledoor", __name__, template_folder="templates")


@doog.route("/", methods=["GET"])
def home():
    return render_template("pages/home.html.jinja")
