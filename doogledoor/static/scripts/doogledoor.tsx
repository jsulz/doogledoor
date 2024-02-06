import React, { ChangeEvent, useEffect, useState } from "react";
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
import { Payload } from "recharts/types/component/DefaultLegendContent";
import * as bootstrap from "bootstrap";

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

interface Doogles {
  time: string;
  dd: number;
}

export default function DoogleDoor() {
  const [time, setTime] = useState("today");
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const paramString = "time=" + time;
    const params = new URLSearchParams(paramString);
    fetch("/api/v1/doogles?" + params)
      .then((response) => response.json())
      .then((data) => setChartData(data));
  }, [time]);

  return (
    <>
      <DoogleCount />
      <TimeSelectors changeTime={setTime} currentTime={time} />
      <DoogleChart data={chartData} />
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

function TimeSelectors({
  changeTime,
  currentTime,
}: {
  changeTime: React.Dispatch<React.SetStateAction<string>>;
  currentTime: string;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    changeTime(e.target.name);
  };

  const times = ["today", "week", "month", "year"];
  return (
    <>
      <div className="btn-group mb-5 btn-group-lg">
        {times.map((time) => {
          return (
            <>
              <input
                type="radio"
                className="btn-check"
                name={time}
                id={time}
                autoComplete="off"
                onChange={(e) => handleChange(e)}
                checked={currentTime === time}
              />
              <label className="btn btn-outline-primary" htmlFor={time}>
                {time}
              </label>
            </>
          );
        })}
      </div>
    </>
  );
}

function DoogleChart({ data }: { data: Doogles[] }) {
  const handleClick = (): void => {
    const myModal = new bootstrap.Modal("#doogleExplainer");
    myModal.show();
  };
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        width={500}
        height={300}
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <XAxis dataKey="time" />
        <YAxis dataKey="dd" />
        <Tooltip />
        <Legend onClick={handleClick} />
        <Bar
          dataKey="dd"
          name="Doogle Ins and Outs*"
          fill="#61adc2"
          activeBar={<Rectangle fill="#C29F61" />}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}
