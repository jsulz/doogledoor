import * as React from "react";
import {
  ResponsiveContainer,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Legend,
  Bar,
  Rectangle,
} from "recharts";

let dailyData = [
  {
    hour: "6:00",
    dd: 5,
  },
  {
    hour: "7:00",
    dd: 7,
  },
  {
    hour: "8:00",
    dd: 2,
  },
  {
    hour: "9:00",
    dd: 3,
  },
  {
    hour: "10:00",
    dd: 4,
  },
  {
    hour: "11:00",
    dd: 5,
  },
  {
    hour: "12:00",
    dd: 0,
  },
  {
    hour: "13:00",
    dd: 10,
  },
  {
    hour: "14:00",
    dd: 2,
  },
  {
    hour: "15:00",
    dd: 2,
  },
  {
    hour: "16:00",
    dd: 0,
  },
  {
    hour: "17:00",
    dd: 2,
  },
  {
    hour: "18:00",
    dd: 6,
  },
  {
    hour: "19:00",
    dd: 5,
  },
  {
    hour: "20:00",
    dd: 20,
  },
];

export default function DoogleDoor() {
  const one = 1;
  return (
    <>
      <DoogleCount />
      <TimeSelectors />
      <DoogleChart />
    </>
  );
}

function DoogleCount() {
  return (
    <div className="mb-5">
      <h1 className="doogle-heading">42</h1>
      <p className="">Today's Total</p>
    </div>
  );
}

function TimeSelectors() {
  return (
    <>
      <div className="btn-group mb-5 btn-group-lg">
        <input
          type="radio"
          className="btn-check"
          name="btnradio"
          id="btnradio1"
          autoComplete="off"
          checked
        />
        <label className="btn btn-outline-primary" htmlFor="btnradio1">
          Today
        </label>
        <input
          type="radio"
          className="btn-check"
          name="btnradio"
          id="btnradio1"
          autoComplete="off"
        />
        <label className="btn btn-outline-primary" htmlFor="btnradio1">
          Past Week
        </label>
        <input
          type="radio"
          className="btn-check"
          name="btnradio"
          id="btnradio2"
          autoComplete="off"
        />
        <label className="btn btn-outline-primary" htmlFor="btnradio2">
          Past Month
        </label>

        <input
          type="radio"
          className="btn-check"
          name="btnradio"
          id="btnradio3"
          autoComplete="off"
        />
        <label className="btn btn-outline-primary" htmlFor="btnradio3">
          Past Year
        </label>
      </div>
    </>
  );
}

function DoogleChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        width={500}
        height={300}
        data={dailyData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <XAxis dataKey="hour" />
        <YAxis dataKey="dd" />
        <Tooltip />
        <Legend />
        <Bar
          dataKey="dd"
          name="Doogle Ins and Outs"
          fill="#61adc2"
          activeBar={<Rectangle fill="#C29F61" />}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}
