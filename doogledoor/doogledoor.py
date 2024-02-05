from flask import Blueprint, render_template
from doogledoor.db import database
from doogledoor.model import DoogleDoor
import sqlalchemy

doog = Blueprint("doogledoor", __name__, template_folder="templates")


@doog.route("/", methods=["GET"])
def home():
    with database.connect() as conn:
        stmt = sqlalchemy.select(DoogleDoor).order_by(DoogleDoor.published)
        for row in conn.execute(stmt).all():
            print(row)
    return render_template("pages/home.html.jinja")
