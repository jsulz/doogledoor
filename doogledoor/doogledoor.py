from flask import Blueprint, render_template, request, jsonify, make_response
import os
import base64

from doogledoor.db import database
import datetime
from dateutil import tz
from doogledoor.model import DoogleDoor
from sqlalchemy import insert, select, text
import pandas as pd
import calendar
import time

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

        message = request.get_json()
        data = base64.b64decode(message["messages"]["data"]).decode("utf-8")

        with database.connect() as conn:
            # stmt = insert(DoogleDoor).values(published=data)
            stmt_text = f"INSERT INTO usage (published, published_tz) VALUES ({message}, to_timestamp({message}))"
            stmt = text(stmt_text)
            conn.execute(stmt)
            conn.commit()

        return make_response(
            jsonify({"Success": "Message successfully published"}), 200
        )
    if request.method == "GET":
        try:
            window = request.args["time"]
        except KeyError:
            return make_response(jsonify({"Error": "Time attribute not provided"}), 500)

        TODAY = "today"
        WEEKLY = "week"
        MONTHLY = "month"
        YEARLY = "year"

        pst = tz.gettz("America/Los_Angeles")
        curr_datetime = datetime.datetime.fromtimestamp(time.time(), tz=pst)

        # stmt = (
        #    select(DoogleDoor)
        #    .where(DoogleDoor.published_tz > datetime.datetime(2024, 2, 11, tzinfo=pst))
        #    .where(DoogleDoor.published_tz < datetime.datetime(2024, 2, 12, tzinfo=pst))
        # )
        # data = []
        # with database.connect() as conn:
        #    for row in conn.execute(stmt).all():
        #        data.append([row[1], row[2]])

        if window == TODAY:
            today_date = datetime.datetime(
                year=curr_datetime.year,
                month=curr_datetime.month,
                day=curr_datetime.day,
                tzinfo=pst,
            )
            tomorrow_date = today_date + datetime.timedelta(days=1)

            data = query_db(today_date, tomorrow_date, pst)

            print(data)

            response = build_df(data, "h")
            # response = get_response("today.csv", "h")
            final = []
            for key, value in response.items():
                hour = f"{key.hour}:00"
                final.append({"time": hour, "dd": value})

            api_response = jsonify(final)

        if window == WEEKLY:
            response = get_response("week.csv", "D")
            final = []
            for key, value in response.items():
                day = f"{key.month}/{key.day}"
                final.append({"time": day, "dd": value})

            api_response = jsonify(final)

        if window == MONTHLY:
            # api_response = jsonify(monthly_data)
            response = get_response("month.csv", "D")
            final = []
            for key, value in response.items():
                day = f"{key.month}/{key.day}"
                final.append({"time": day, "dd": value})

            api_response = jsonify(final)

        if window == YEARLY:
            response = get_response("year.csv", "ME")
            final = []
            for key, value in response.items():
                day = f"{calendar.month_name[key.month]}"
                final.append({"time": day, "dd": value})

            api_response = jsonify(final)

        return make_response(api_response, 200)

    return make_response(jsonify({"Error": "Method not supported"}), 405)


def get_response(file, frequency):
    df = pd.read_csv(
        f"test_data/{file}",
        header=None,
        names=["epoch", "timestamptz"],
    )

    df["timestamptz"] = pd.to_datetime(df["timestamptz"])
    df = pd.DataFrame(df.set_index("timestamptz").resample(frequency).count())

    return df["epoch"].to_dict()


def build_df(data, frequency):
    df = pd.DataFrame(data, columns=["epoch", "timestamptz"])
    df["timestamptz"] = pd.to_datetime(df["timestamptz"])
    df = pd.DataFrame(df.set_index("timestamptz").resample(frequency).count())

    # Remove the boundary counts we created in query db
    df["epoch"].iloc[0] = df["epoch"].iloc[0] - 1
    df["epoch"].iloc[-1] = df["epoch"].iloc[-1] - 1

    return df["epoch"].to_dict()


def query_db(lower_bounds, upper_bounds, timezone):
    stmt = (
        select(DoogleDoor)
        .where(DoogleDoor.published_tz > lower_bounds)
        .where(DoogleDoor.published_tz < upper_bounds)
    )
    data = []
    print(lower_bounds.timestamp(), upper_bounds.timestamp() - 1)
    with database.connect() as conn:
        for row in conn.execute(stmt).all():
            data.append([row[1], row[2].astimezone(timezone)])

    # Add boundary counts
    data.insert(
        0,
        [
            lower_bounds.timestamp(),
            datetime.datetime.fromtimestamp(lower_bounds.timestamp(), tz=timezone),
        ],
    )
    data.append(
        [
            upper_bounds.timestamp() - 1,
            datetime.datetime.fromtimestamp(upper_bounds.timestamp() - 1, tz=timezone),
        ],
    )
    return data


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
