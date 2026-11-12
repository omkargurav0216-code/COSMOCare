
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
    key: "heart_rate_bpm",
    label: "Heart Rate",
    unit: "BPM",
    color: "#fb7185",
    icon: HeartPulse,
  },
  {
    key: "spo2_percent",
    label: "Blood Oxygen",
    unit: "%",
    color: "#22d3ee",
    icon: Activity,
  },
  {
    key: "sleep_chart_hours",
    label: "Sleep Duration",
    unit: "hrs",
    color: "#a78bfa",
    icon: Moon,
  },
  {
    key: "body_temperature_celsius",
    label: "Temperature",
    unit: "°C",
    color: "#fbbf24",
    icon: Thermometer,
  },
  {
    key: "radiation_dose_rate_usv_per_hour",
    label: "Radiation Dose Rate",
    unit: "μSv/hour",
    color: "#fb923c",
    icon: Radiation,
  },
];

const formatTimestamp = (timestamp, range) => {
  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "Unknown";
  }

  if (range === "24h") {
    return date.toLocaleTimeString("en-GB", {
      hour: "2-digit",
      minute: "2-digit",
      timeZone: "UTC",
    });
  }

  return date.toLocaleDateString("en-GB", {
    weekday: "short",
    timeZone: "UTC",
  });
};

function HealthMonitoring() {
  const [timeRange, setTimeRange] = useState("24h");
  const [selectedMetric, setSelectedMetric] =
    useState("heart_rate_bpm");

  const astronaut = mockAstronauts.find(
    (item) => item.astronaut_id === "AST-001"
  );

  const currentMetric = metricOptions.find(
    (metric) => metric.key === selectedMetric
  );

  const chartData = (mockTelemetry[timeRange] || []).map(
    (reading) => ({
      ...reading,
      display_time: formatTimestamp(reading.timestamp, timeRange),
    })
  );

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

  const summaryMetrics = [
    {
      ...metricOptions[0],
      value: astronaut.heart_rate_bpm,
    },
    {
      ...metricOptions[1],
      value: astronaut.spo2_percent,
    },
    {
      ...metricOptions[2],
      value: astronaut.sleep_hours_last_24h,
    },
    {
      ...metricOptions[3],
      value: astronaut.body_temperature_celsius,
    },
    {
      ...metricOptions[4],
      value: astronaut.radiation_dose_rate_usv_per_hour,
    },
  ];

  const selectedMetricHasData = chartData.some(
    (reading) =>
      typeof reading[selectedMetric] === "number" &&
      Number.isFinite(reading[selectedMetric])
  );

  const fatigueValue = astronaut.fatigue_level_0_10;

  const fatigueAvailable =
    typeof fatigueValue === "number" &&
    Number.isFinite(fatigueValue);

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
              {astronaut.astronaut_id} · {astronaut.role}
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
            const available =
              typeof metric.value === "number" &&
              Number.isFinite(metric.value);

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
                    <Icon
                      size={19}
                      style={{ color: metric.color }}
                    />
                  </div>
                </div>

                <div className="mt-5 flex flex-wrap items-baseline gap-2">
                  <span className={`font-bold tracking-tight ${
                    available
                      ? "text-3xl text-white"
                      : "text-base text-slate-500"
                  }`}>
                    {available ? metric.value : "Insufficient Data"}
                  </span>

                  {available && (
                    <span className="text-xs text-slate-500">
                      {metric.unit}
                    </span>
                  )}
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
              Illustrative biometric chart samples
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
          {selectedMetricHasData ? (
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
                  dataKey="display_time"
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
                  connectNulls={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex h-full flex-col items-center justify-center gap-2 text-center text-sm text-slate-500">
              <ShieldCheck size={24} />
              <p>Insufficient Data</p>
              <p className="text-xs">
                No validated illustrative samples are available for this metric.
              </p>
            </div>
          )}
        </div>

        <div className="mt-4 flex items-center gap-2 border-t border-slate-800 pt-4 text-xs text-slate-500">
          <Clock3 size={14} />
          {timeRange === "24h"
            ? "Illustrative samples across 24 hours"
            : "Illustrative samples across 7 days"}
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
          Fatigue indicator from the astronaut telemetry profile
        </p>

        {fatigueAvailable ? (
          <div className="mt-6">
            <p className="text-3xl font-bold text-white">
              {fatigueValue}/10
            </p>
            <p className="mt-2 text-xs text-slate-500">
              Numeric fatigue measurement (0–10 scale)
            </p>
            <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-purple-400"
                style={{
                  width: `${Math.min(10, Math.max(0, fatigueValue)) * 10}%`,
                }}
              />
            </div>
          </div>
        ) : (
          <div className="mt-6 rounded-lg border border-slate-700/60 bg-slate-900/40 p-4">
            <p className="font-semibold text-slate-300">
              Insufficient Data
            </p>
            <p className="mt-1 text-sm text-slate-500">
              A validated numeric fatigue measurement is not currently available.
            </p>
          </div>
        )}
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
          All telemetry values and charts are simulated illustrative
          data. Sleep chart samples are not validated rolling 24-hour
          sleep measurements. Radiation dose rate and numeric fatigue
          values are currently unavailable. These values are not actual
          astronaut measurements, validated medical assessments or
          clinical predictions. Live telemetry integration is pending
          the agreed backend API contract.
        </p>
      </div>
    </div>
  );
}

export default HealthMonitoring;
