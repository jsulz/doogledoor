from flask import Blueprint, render_template, request, jsonify, make_response
import os

# from doogledoor.db import database
# from doogledoor.model import DoogleDoor
import sqlalchemy

doog = Blueprint("doogledoor", __name__, template_folder="templates")


@doog.route("/", methods=["GET"])
def home():

    return render_template("pages/home.html.jinja")


@doog.route("/api/v1/doogles", methods=["GET", "POST"])
def doogles():
    if request.method == "POST":
        try:
            bearer_token = request.headers["Authorization"]
        except KeyError:
            return make_response(jsonify({"Error": "Authorization not provided"}), 401)

        if bearer_token != os.environ["BEARER_TOKEN"]:
            return make_response(jsonify({"Error": "Incorrect bearer token"}), 401)

        print(request.get_data())
        print(request.get_json())

        return make_response("Okay", 200)
    if request.method == "GET":
        try:
            time = request.args["time"]
        except KeyError:
            return make_response(jsonify({"Error": "Time attribute not provided"}), 500)

        TODAY = "today"
        WEEKLY = "week"
        MONTHLY = "month"
        YEARLY = "year"

        if time == TODAY:
            api_response = jsonify(daily_data)

        if time == WEEKLY:
            api_response = jsonify(weekly_data)

        if time == MONTHLY:
            api_response = jsonify(monthly_data)

        if time == YEARLY:
            api_response = jsonify(yearly_data)

        return make_response(api_response, 200)

    return make_response(jsonify({"Error": "Method not supported"}), 405)


daily_data = [
    {"time": "1:00", "dd": 0},
    {"time": "2:00", "dd": 0},
    {"time": "3:00", "dd": 0},
    {"time": "4:00", "dd": 0},
    {"time": "5:00", "dd": 0},
    {"time": "6:00", "dd": 2},
    {"time": "7:00", "dd": 2},
    {"time": "8:00", "dd": 0},
    {"time": "9:00", "dd": 0},
    {"time": "10:00", "dd": 4},
    {"time": "11:00", "dd": 3},
    {"time": "12:00", "dd": 2},
    {"time": "13:00", "dd": 4},
    {"time": "14:00", "dd": 0},
    {"time": "15:00", "dd": 0},
    {"time": "16:00", "dd": 5},
    {"time": "17:00", "dd": 6},
    {"time": "18:00", "dd": 5},
    {"time": "19:00", "dd": 2},
    {"time": "20:00", "dd": 2},
    {"time": "21:00", "dd": 0},
    {"time": "22:00", "dd": 0},
    {"time": "23:00", "dd": 0},
    {"time": "24:00", "dd": 0},
]

weekly_data = [
    {"time": "1/31", "dd": 20},
    {"time": "2/1", "dd": 30},
    {"time": "2/2", "dd": 35},
    {"time": "2/3", "dd": 36},
    {"time": "2/4", "dd": 40},
    {"time": "2/5", "dd": 22},
    {"time": "2/6", "dd": 22},
]

monthly_data = [
    {"time": "1/9", "dd": 29},
    {"time": "1/10", "dd": 38},
    {"time": "1/11", "dd": 37},
    {"time": "1/12", "dd": 39},
    {"time": "1/13", "dd": 30},
    {"time": "1/14", "dd": 42},
    {"time": "1/15", "dd": 36},
    {"time": "1/16", "dd": 34},
    {"time": "1/17", "dd": 35},
    {"time": "1/18", "dd": 40},
    {"time": "1/19", "dd": 30},
    {"time": "1/20", "dd": 26},
    {"time": "1/21", "dd": 24},
    {"time": "1/2", "dd": 45},
    {"time": "1/23", "dd": 50},
    {"time": "1/24", "dd": 29},
    {"time": "1/25", "dd": 28},
    {"time": "1/26", "dd": 24},
    {"time": "1/27", "dd": 36},
    {"time": "1/2", "dd": 33},
    {"time": "1/29", "dd": 32},
    {"time": "1/30", "dd": 30},
    {"time": "1/31", "dd": 20},
    {"time": "2/1", "dd": 30},
    {"time": "2/2", "dd": 35},
    {"time": "2/3", "dd": 36},
    {"time": "2/4", "dd": 40},
    {"time": "2/5", "dd": 22},
    {"time": "2/6", "dd": 22},
]

yearly_data = [
    {"time": "March", "dd": 1000},
    {"time": "April", "dd": 954},
    {"time": "May", "dd": 853},
    {"time": "June", "dd": 952},
    {"time": "July", "dd": 954},
    {"time": "August", "dd": 1156},
    {"time": "September", "dd": 1100},
    {"time": "October", "dd": 920},
    {"time": "November", "dd": 680},
    {"time": "December", "dd": 970},
    {"time": "January", "dd": 950},
    {"time": "February", "dd": 1200},
]
