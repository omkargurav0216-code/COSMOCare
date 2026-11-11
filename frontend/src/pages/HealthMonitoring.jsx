
import { useState } from "react";
import { mockTelemetry } from "../data/mockTelemetry";
import { mockAstronauts } from "../data/mockAstronauts";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  HeartPulse,
  Activity,
  Moon,
  Thermometer,
  Radiation,
  Clock3,
  Satellite,
  TrendingUp,
  ShieldCheck,
} from "lucide-react";

const metricOptions = [
  {
    key: "heartRate",
    label: "Heart Rate",
    unit: "BPM",
    color: "#fb7185",
    icon: HeartPulse,
  },
  {
    key: "spo2",
    label: "Blood Oxygen",
    unit: "%",
    color: "#22d3ee",
    icon: Activity,
  },
  {
    key: "sleep",
    label: "Sleep Duration",
    unit: "hrs",
    color: "#a78bfa",
    icon: Moon,
  },
  {
    key: "temperature",
    label: "Temperature",
    unit: "°C",
    color: "#fbbf24",
    icon: Thermometer,
  },
  {
    key: "radiation",
    label: "Radiation Exposure",
    unit: "mSv",
    color: "#fb923c",
    icon: Radiation,
  },
];

function HealthMonitoring() {
  const [timeRange, setTimeRange] = useState("24h");
  const [selectedMetric, setSelectedMetric] = useState("heartRate");

  const astronaut = mockAstronauts.find(
    (item) => item.id === "AST-001"
  );

  const currentMetric = metricOptions.find(
    (metric) => metric.key === selectedMetric
  );

  const chartData = mockTelemetry[timeRange] || [];

  if (!astronaut || !currentMetric) {
    return (
      <div className="astra-panel p-8 text-center">
        <h2 className="text-lg font-semibold text-white">
          Health data unavailable
        </h2>
        <p className="mt-2 text-sm text-slate-400">
          The selected astronaut or metric could not be loaded.
        </p>
      </div>
    );
  }

  const summaryMetrics = metricOptions.map((metric) => ({
    ...metric,
    value: astronaut[metric.key] ?? "N/A",
  }));

  // Illustrative prototype value. Not an ML-generated score.
  const fatigueScore = 25;

  return (
    <div className="space-y-7">

      {/* Page heading */}
      <section>
        <div className="flex items-center gap-2 text-xs font-semibold tracking-[0.18em] text-cyan-400">
          <Activity size={15} />
          BIOMETRIC TELEMETRY
        </div>

        <h1 className="mt-2 text-3xl font-bold tracking-tight text-white">
          Health Monitoring
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
          Monitor astronaut biometric indicators, review telemetry
          trends and explore health-related mission data.
        </p>
      </section>

      {/* Selected astronaut */}
      <section className="astra-panel flex flex-col justify-between gap-4 p-5 sm:flex-row sm:items-center">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-400/10 text-cyan-400">
            <Satellite size={23} />
          </div>

          <div>
            <p className="text-xs font-medium tracking-wider text-slate-500">
              SELECTED ASTRONAUT
            </p>

            <h2 className="mt-1 font-semibold text-white">
              {astronaut.name}
            </h2>

            <p className="mt-1 text-xs text-slate-400">
              {astronaut.id} · {astronaut.role}
            </p>
          </div>
        </div>

        <span className="flex w-fit items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-2 text-xs font-medium text-emerald-400">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          Demo Monitoring
        </span>
      </section>

      {/* Health indicator cards */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white">
              Health Indicators
            </h2>
            <p className="mt-1 text-xs text-slate-500">
              Illustrative astronaut profile readings
            </p>
          </div>

          <span className="text-xs text-slate-500">
            05 Metrics
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {summaryMetrics.map((metric) => {
            const Icon = metric.icon;

            return (
              <div
                key={metric.key}
                className="astra-panel astra-panel-hover p-5"
              >
                <div className="flex items-center justify-between">
                  <p className="text-sm text-slate-400">
                    {metric.label}
                  </p>

                  <div className="rounded-lg bg-white/5 p-2">
                    <Icon size={19} style={{ color: metric.color }} />
                  </div>
                </div>

                <div className="mt-5 flex items-baseline gap-2">
                  <span className="text-3xl font-bold tracking-tight text-white">
                    {metric.value}
                  </span>

                  <span className="text-xs text-slate-500">
                    {metric.unit}
                  </span>
                </div>

                <div
                  className="mt-4 h-1 w-full rounded-full"
                  style={{ backgroundColor: `${metric.color}20` }}
                >
                  <div
                    className="h-1 w-2/3 rounded-full"
                    style={{ backgroundColor: metric.color }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Telemetry trends */}
      <section className="astra-panel p-5 sm:p-6">
        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
          <div>
            <div className="flex items-center gap-2">
              <TrendingUp size={19} className="text-cyan-400" />

              <h2 className="text-lg font-semibold text-white">
                Telemetry Trends
              </h2>
            </div>

            <p className="mt-2 text-sm text-slate-500">
              Historical biometric data visualization
            </p>
          </div>

          <div className="flex w-fit rounded-lg border border-slate-700/70 bg-[#080f1e] p-1">
            {["24h", "7d"].map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                aria-pressed={timeRange === range}
                className={`rounded-md px-4 py-2 text-xs font-medium transition ${
                  timeRange === range
                    ? "bg-blue-500/20 text-cyan-300"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {range === "24h" ? "24 Hours" : "7 Days"}
              </button>
            ))}
          </div>
        </div>

        {/* Metric selector */}
        <div className="mt-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <label
            htmlFor="health-metric"
            className="text-sm text-slate-400"
          >
            Select health indicator
          </label>

          <select
            id="health-metric"
            value={selectedMetric}
            onChange={(event) => setSelectedMetric(event.target.value)}
            className="rounded-lg border border-slate-700 bg-[#111f35] px-4 py-2.5 text-sm text-white outline-none transition focus:border-cyan-400"
          >
            {metricOptions.map((metric) => (
              <option key={metric.key} value={metric.key}>
                {metric.label}
              </option>
            ))}
          </select>
        </div>

        {/* Selected metric */}
        <div className="mt-6 flex items-center gap-3">
          <div
            className="h-9 w-1 rounded-full"
            style={{ backgroundColor: currentMetric.color }}
          />

          <div>
            <p className="text-sm font-semibold text-white">
              {currentMetric.label}
            </p>

            <p className="text-xs text-slate-500">
              Measurement unit: {currentMetric.unit}
            </p>
          </div>
        </div>

        {/* Chart */}
        <div className="mt-6 h-72 w-full">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={chartData}
                margin={{ top: 10, right: 10, left: -15, bottom: 0 }}
              >
                <CartesianGrid
                  stroke="#263449"
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="time"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#94a3b8", fontSize: 11 }}
                  dy={10}
                />

                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#94a3b8", fontSize: 11 }}
                  domain={["auto", "auto"]}
                />

                <Tooltip
                  contentStyle={{
                    backgroundColor: "#111f35",
                    border: "1px solid #334155",
                    borderRadius: "10px",
                    color: "#fff",
                  }}
                  formatter={(value) => [
                    `${value} ${currentMetric.unit}`,
                    currentMetric.label,
                  ]}
                />

                <Line
                  type="monotone"
                  dataKey={selectedMetric}
                  name={currentMetric.label}
                  stroke={currentMetric.color}
                  strokeWidth={2.5}
                  dot={false}
                  activeDot={{
                    r: 5,
                    fill: currentMetric.color,
                    stroke: "#0d1729",
                    strokeWidth: 2,
                  }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex h-full items-center justify-center text-sm text-slate-500">
              No illustrative telemetry available for this time range.
            </div>
          )}
        </div>

        <div className="mt-4 flex items-center gap-2 border-t border-slate-800 pt-4 text-xs text-slate-500">
          <Clock3 size={14} />
          {timeRange === "24h"
            ? "Illustrative readings across 24 hours"
            : "Illustrative readings across 7 days"}
        </div>
      </section>

      {/* Fatigue monitoring */}
      <section className="astra-panel p-5 sm:p-6">
        <div className="flex items-center gap-2">
          <Moon size={19} className="text-purple-400" />

          <h2 className="text-lg font-semibold text-white">
            Fatigue Monitoring
          </h2>
        </div>

        <p className="mt-2 text-sm text-slate-500">
          Illustrative fatigue indicator for the selected astronaut
        </p>

        <div className="mt-6 grid gap-6 sm:grid-cols-2 sm:items-center">
          <div>
            <p className="text-xs text-slate-500">
              Prototype indicator
            </p>

            <p className="mt-2 text-3xl font-bold text-emerald-400">
              Low
            </p>

            <p className="mt-1 text-sm text-slate-400">
              {fatigueScore}/100
            </p>
          </div>

          <div>
            <div className="mb-3 flex justify-between text-xs text-slate-500">
              <span>0 - Low</span>
              <span>100 - High</span>
            </div>

            <div className="h-3 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-emerald-400 transition-all"
                style={{ width: `${fatigueScore}%` }}
              />
            </div>

            <p className="mt-3 text-right text-xs text-slate-500">
              Illustrative score: {fatigueScore}/100
            </p>
          </div>
        </div>
      </section>

      {/* Data notice */}
      <div className="flex items-start gap-3 rounded-xl border border-blue-400/10 bg-blue-400/5 p-4">
        <ShieldCheck
          size={18}
          className="mt-0.5 shrink-0 text-blue-400"
        />

        <p className="text-xs leading-5 text-slate-400">
          <span className="font-semibold text-slate-300">
            Prototype data notice:
          </span>{" "}
          All telemetry values, charts and fatigue indicators are
          simulated illustrative data. They are not actual astronaut
          measurements, validated medical assessments or clinical
          predictions. Live telemetry integration is pending the
          agreed backend API contract.
        </p>
      </div>
    </div>
  );
}

export default HealthMonitoring;
