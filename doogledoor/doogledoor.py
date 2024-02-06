from flask import Blueprint, render_template

# from doogledoor.db import database
# from doogledoor.model import DoogleDoor
import sqlalchemy

doog = Blueprint("doogledoor", __name__, template_folder="templates")


@doog.route("/", methods=["GET"])
def home():

    return render_template("pages/home.html.jinja")


daily_data = [
    {"0:00": 0},
    {"1:00": 0},
    {"2:00": 0},
    {"3:00": 0},
    {"4:00": 0},
    {"5:00": 0},
    {"6:00": 2},
    {"7:00": 2},
    {"8:00": 0},
    {"9:00": 0},
    {"10:00": 4},
    {"11:00": 3},
    {"12:00": 2},
    {"13:00": 4},
    {"14:00": 0},
    {"15:00": 0},
    {"16:00": 5},
    {"17:00": 6},
    {"18:00": 5},
    {"19:00": 2},
    {"20:00": 2},
    {"21:00": 0},
    {"22:00": 0},
    {"23:00": 0},
    {"24:00": 0},
]

weekly_data = [
    {"1/31": 20},
    {"2/1": 30},
    {"2/2": 35},
    {"2/3": 36},
    {"2/4": 40},
    {"2/5": 22},
    {"2/6": 22},
]
