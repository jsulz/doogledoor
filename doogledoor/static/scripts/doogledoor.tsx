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

interface Doogles {
  time: string;
  dd: number;
}

export default function DoogleDoor() {
  const [time, setTime] = useState("today");
  const [chartData, setChartData] = useState([]);
  const [doogleCount, setDoogleCount] = useState(0);

  useEffect(() => {
    const paramString = "time=" + time;
    const params = new URLSearchParams(paramString);
    fetch("/api/v1/doogles?" + params)
      .then((response) => response.json())
      .then((data) => {
        const initial = 0;
        const newDoogleCount = data.reduce(
          (accumulator: number, current: Doogles) => accumulator + current.dd,
          initial
        );
        setDoogleCount(newDoogleCount);
        setChartData(data);
      });
  }, [time]);

  return (
    <>
      <DoogleCount count={doogleCount} />
      <TimeSelectors changeTime={setTime} currentTime={time} />
      <DoogleChart data={chartData} />
    </>
  );
}

function DoogleCount({ count }: { count: number }) {
  return (
    <div className="mb-5">
      <h1 className="doogle-heading">{count}</h1>
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
