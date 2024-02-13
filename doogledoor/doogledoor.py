import os
import base64
import datetime
import calendar
import time
from dateutil import tz
from flask import Blueprint, render_template, request, jsonify, make_response
from sqlalchemy import select, text
import pandas as pd
from doogledoor.db import database
from doogledoor.model import DoogleDoor

doog = Blueprint("doogledoor", __name__, template_folder="templates")


@doog.route("/", methods=["GET"])
def home():

    return render_template("pages/home.html.jinja")


@doog.route("/about", methods=["GET"])
def about():
    return render_template("pages/about.html.jinja")


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
            stmt_text = f"INSERT INTO usage (published, published_tz) VALUES ({data}, to_timestamp({data}))"
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
        today_date = datetime.datetime(
            year=curr_datetime.year,
            month=curr_datetime.month,
            day=curr_datetime.day,
            tzinfo=pst,
        )
        tomorrow_date = today_date + datetime.timedelta(days=1)

        if window == TODAY:
            data = query_db(today_date, tomorrow_date, pst)
            response = build_df(data, "h")
            # response = get_response("today.csv", "h")
            final = []
            for key, value in response.items():
                hour = f"{key.hour}:00"
                final.append({"time": hour, "dd": value})

            api_response = jsonify(final)

        if window == WEEKLY:
            last_week = today_date - datetime.timedelta(days=6)
            data = query_db(last_week, tomorrow_date, pst)
            response = build_df(data, "D")

            # response = get_response("week.csv", "D")
            final = []
            for key, value in response.items():
                day = f"{key.month}/{key.day}"
                final.append({"time": day, "dd": value})

            api_response = jsonify(final)

        if window == MONTHLY:
            four_weeks_ago = today_date - datetime.timedelta(days=27)
            data = query_db(four_weeks_ago, tomorrow_date, pst)
            response = build_df(data, "D")
            final = []
            for key, value in response.items():
                day = f"{key.month}/{key.day}"
                final.append({"time": day, "dd": value})

            api_response = jsonify(final)

        if window == YEARLY:
            one_year_ago = today_date - datetime.timedelta(days=364)
            data = query_db(one_year_ago, tomorrow_date, pst)
            response = build_df(data, "ME")
            final = []
            for key, value in response.items():
                day = f"{calendar.month_name[key.month]}"
                final.append({"time": day, "dd": value})

            api_response = jsonify(final)

        return make_response(api_response, 200)

    return make_response(jsonify({"Error": "Method not supported"}), 405)


def build_df(data, frequency):
    df = pd.DataFrame(data, columns=["epoch", "timestamptz"])
    df["timestamptz"] = pd.to_datetime(df["timestamptz"])
    df = pd.DataFrame(df.set_index("timestamptz").resample(frequency).count())

    # Remove the boundary counts we created in query db
    df.iloc[0, df.columns.get_loc("epoch")] = (
        df.iloc[0, df.columns.get_loc("epoch")] - 1
    )
    df.iloc[-1, df.columns.get_loc("epoch")] = (
        df.iloc[-1, df.columns.get_loc("epoch")] - 1
    )

    return df["epoch"].to_dict()


def query_db(lower_bounds, upper_bounds, timezone):
    stmt = (
        select(DoogleDoor)
        .where(DoogleDoor.published_tz > lower_bounds)
        .where(DoogleDoor.published_tz < upper_bounds)
    )
    data = []

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
