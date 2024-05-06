# Doogledoor

## Description

Doogledoor is the web side of an Internet of Things project to track the family dog's ins and outs through her door.

The firmware part of this project runs on a [Thing Plus - ESP32-S2](https://www.sparkfun.com/products/17743) and makes use of an [OpenPIR motion sensor](https://www.sparkfun.com/products/13968). The code and relevant links for that are available in the [Dooglebot repository](https://github.com/jsulz/dooglebot).

This repository hosts the Flask application that is responsible for storing data sent by the Thing Plus and displaying it (see: https://doogledoor.jsulz.com/).

There's a fair amount of boilerplate code here, so if you're interested, check out the following files where most of the logic is contained:

- `doogledoor/doogledoor.py`
  - Contains all the routes for the web application
  - Responsible for responding to POST requests from the Thing Plus and storing the data in a Cloud SQL Postgres database
  - Pulls the data from the same database and shapes it for the front end
- `doogledoor/static/scripts/doogledoor.tsx`
  - Manages the display of the data from the backend (and makes the GET requests to the Flask API to get the data)
  - Includes the functionality for showing the chart and changing the date ranges

If you have any questions, feel free to [let me know](https://www.jsulz.com/contact/)!
