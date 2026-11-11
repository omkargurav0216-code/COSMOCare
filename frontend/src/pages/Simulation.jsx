
import { useState } from "react";

import {
  SlidersHorizontal,
  Activity,
  Moon,
  HeartPulse,
  Radiation,
  Play,
  RotateCcw,
  Info,
  Gauge,
} from "lucide-react";

import { simulationConfig } from "../data/simulationConfig";

function Simulation() {
  const { baselineScore, defaults, ranges } = simulationConfig;

  const [sleep, setSleep] = useState(defaults.sleep);
  const [heartRate, setHeartRate] = useState(defaults.heartRate);
  const [radiation, setRadiation] = useState(defaults.radiation);
  const [result, setResult] = useState(null);

  // Illustrative frontend-only formula.
  // Replace with the agreed ML/backend simulation integration later.
  const calculateDemoScore = () => {
    const sleepImpact = (7 - sleep) * 5;
    const heartRateImpact = (heartRate - 72) * 0.25;
    const radiationImpact = (radiation - 0.3) * 10;

    return Math.round(
      Math.max(
        0,
        Math.min(
          100,
          baselineScore +
            sleepImpact +
            heartRateImpact +
            radiationImpact
        )
      )
    );
  };

  const handleSimulation = () => {
    setResult(calculateDemoScore());
  };

  const handleReset = () => {
    setSleep(defaults.sleep);
    setHeartRate(defaults.heartRate);
    setRadiation(defaults.radiation);
    setResult(null);
  };

  const getRiskLabel = (score) => {
    if (score < 30) return "Low";
    if (score < 60) return "Moderate";
    return "High";
  };

  const getRiskColor = (score) => {
    if (score < 30) return "text-emerald-400";
    if (score < 60) return "text-amber-400";
    return "text-red-400";
  };

  const getRiskBarColor = (score) => {
    if (score < 30) return "bg-emerald-400";
    if (score < 60) return "bg-amber-400";
    return "bg-red-400";
  };

  const scoreDifference =
    result === null ? null : result - baselineScore;

  return (
    <div className="space-y-7">

      {/* Page heading */}
      <section>
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-cyan-400" />

          <p className="text-xs font-semibold tracking-[0.18em] text-cyan-400">
            SCENARIO ANALYSIS
          </p>
        </div>

        <h1 className="mt-2 text-2xl font-bold tracking-tight text-white sm:text-3xl">
          What-If Simulation
        </h1>

        <p className="mt-2 text-sm leading-6 text-slate-400">
          Explore hypothetical changes in astronaut health parameters
          and compare their illustrative risk scores.
        </p>
      </section>

      {/* Prototype notice */}
      <section className="flex items-start gap-3 rounded-xl border border-amber-400/15 bg-amber-400/5 p-4">
        <Info
          className="mt-0.5 shrink-0 text-amber-400"
          size={19}
        />

        <div>
          <p className="text-sm font-semibold text-amber-300">
            Demonstration Mode
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-400">
            This simulation uses an illustrative local formula.
            It is not connected to the actual ASTRA ML model or
            backend and does not generate clinical predictions.
          </p>
        </div>
      </section>

      {/* Baseline score */}
      <section className="astra-panel p-5">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
          <div>
            <div className="flex items-center gap-2">
              <Gauge size={17} className="text-cyan-400" />

              <p className="text-xs font-semibold tracking-wider text-slate-400">
                BASELINE RISK SCORE
              </p>
            </div>

            <div className="mt-3 flex items-end gap-2">
              <span className="text-4xl font-bold text-white">
                {baselineScore}
              </span>

              <span className="mb-1 text-sm text-slate-500">
                / 100
              </span>
            </div>

            <p className="mt-2 text-xs text-slate-500">
              Illustrative reference score for this demonstration.
            </p>
          </div>

          <span className="w-fit rounded-full border border-amber-400/20 bg-amber-400/10 px-4 py-2 text-xs font-medium text-amber-400">
            Moderate Baseline
          </span>
        </div>
      </section>

      {/* Main simulation layout */}
      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">

        {/* Parameter controls */}
        <section className="astra-panel p-5 sm:p-6">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-cyan-400/10 p-2.5">
              <SlidersHorizontal
                className="text-cyan-400"
                size={21}
              />
            </div>

            <div>
              <h2 className="font-semibold text-white">
                Adjust Health Parameters
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Configure values for a hypothetical scenario.
              </p>
            </div>
          </div>

          {/* Sleep duration */}
          <ParameterSlider
            label="Sleep Duration"
            icon={Moon}
            iconColor="text-purple-400"
            value={sleep}
            displayValue={`${sleep} hours`}
            min={ranges.sleep.min}
            max={ranges.sleep.max}
            step={ranges.sleep.step}
            onChange={(value) => {
              setSleep(value);
              setResult(null);
            }}
            minLabel={`${ranges.sleep.min} hours`}
            maxLabel={`${ranges.sleep.max} hours`}
          />

          {/* Heart rate */}
          <ParameterSlider
            label="Heart Rate"
            icon={HeartPulse}
            iconColor="text-red-400"
            value={heartRate}
            displayValue={`${heartRate} BPM`}
            min={ranges.heartRate.min}
            max={ranges.heartRate.max}
            step={ranges.heartRate.step}
            onChange={(value) => {
              setHeartRate(value);
              setResult(null);
            }}
            minLabel={`${ranges.heartRate.min} BPM`}
            maxLabel={`${ranges.heartRate.max} BPM`}
          />

          {/* Radiation exposure */}
          <ParameterSlider
            label="Radiation Exposure"
            icon={Radiation}
            iconColor="text-amber-400"
            value={radiation}
            displayValue={`${radiation.toFixed(1)} mSv`}
            min={ranges.radiation.min}
            max={ranges.radiation.max}
            step={ranges.radiation.step}
            onChange={(value) => {
              setRadiation(value);
              setResult(null);
            }}
            minLabel={`${ranges.radiation.min} mSv`}
            maxLabel={`${ranges.radiation.max} mSv`}
          />

          {/* Action buttons */}
          <div className="mt-9 flex flex-wrap gap-3">
            <button
              onClick={handleSimulation}
              className="inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-2 focus:ring-offset-[#0b1425]"
            >
              <Play size={16} />
              Run Simulation
            </button>

            <button
              onClick={handleReset}
              className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-5 py-3 text-sm font-medium text-slate-300 transition hover:border-slate-600 hover:bg-slate-800"
            >
              <RotateCcw size={16} />
              Reset Parameters
            </button>
          </div>
        </section>

        {/* Simulation results */}
        <section className="astra-panel p-5 sm:p-6">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-blue-500/10 p-2.5">
              <Activity
                className="text-cyan-400"
                size={21}
              />
            </div>

            <div>
              <h2 className="font-semibold text-white">
                Simulation Results
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Baseline and hypothetical scenario comparison
              </p>
            </div>
          </div>

          {result === null ? (
            <div className="flex min-h-80 flex-col items-center justify-center text-center">
              <div className="rounded-full border border-slate-700 bg-slate-800/60 p-5">
                <SlidersHorizontal
                  size={30}
                  className="text-slate-500"
                />
              </div>

              <h3 className="mt-5 font-semibold text-white">
                Awaiting Simulation
              </h3>

              <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
                Adjust the health parameters and run the simulation
                to view an illustrative result.
              </p>
            </div>
          ) : (
            <div className="mt-8 space-y-7">

              {/* Result score */}
              <div>
                <p className="text-sm text-slate-400">
                  Simulated Risk Score
                </p>

                <div className="mt-3 flex items-end gap-2">
                  <span
                    className={`text-5xl font-bold tracking-tight ${getRiskColor(result)}`}
                  >
                    {result}
                  </span>

                  <span className="mb-1 text-sm text-slate-500">
                    / 100
                  </span>
                </div>

                <span
                  className={`mt-3 inline-flex rounded-full border border-current/20 bg-slate-800/50 px-3 py-1.5 text-xs font-semibold ${getRiskColor(result)}`}
                >
                  {getRiskLabel(result)} Risk
                </span>
              </div>

              {/* Score comparison */}
              <div className="space-y-5">
                <ScoreBar
                  label="Baseline"
                  score={baselineScore}
                  color="bg-slate-500"
                  valueColor="text-slate-300"
                />

                <ScoreBar
                  label="Simulated"
                  score={result}
                  color={getRiskBarColor(result)}
                  valueColor={getRiskColor(result)}
                />
              </div>

              {/* Difference */}
              <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
                <p className="text-xs font-medium tracking-wider text-slate-500">
                  CHANGE FROM BASELINE
                </p>

                <p
                  className={`mt-2 text-2xl font-bold ${
                    scoreDifference > 0
                      ? "text-red-400"
                      : scoreDifference < 0
                        ? "text-emerald-400"
                        : "text-slate-300"
                  }`}
                >
                  {scoreDifference > 0 ? "+" : ""}
                  {scoreDifference} points
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  Illustrative difference from the reference score.
                </p>
              </div>

              {/* Result disclaimer */}
              <div className="flex items-start gap-2 border-t border-slate-800 pt-4">
                <Info
                  size={15}
                  className="mt-0.5 shrink-0 text-amber-400"
                />

                <p className="text-xs leading-5 text-slate-500">
                  This result is generated locally using a demonstration
                  formula. It is not produced by the ASTRA ML model
                  and should not be used for medical decisions.
                </p>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

// Reusable parameter slider.
function ParameterSlider({
  label,
  icon: Icon,
  iconColor,
  value,
  displayValue,
  min,
  max,
  step,
  onChange,
  minLabel,
  maxLabel,
}) {
  return (
    <div className="mt-8">
      <div className="flex items-center justify-between gap-3">
        <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
          <Icon size={17} className={iconColor} />
          {label}
        </label>

        <span className="rounded-lg border border-slate-700 bg-slate-800/60 px-3 py-1.5 text-sm font-semibold text-white">
          {displayValue}
        </span>
      </div>

      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        aria-label={label}
        className="mt-5 w-full cursor-pointer accent-cyan-400"
      />

      <div className="flex justify-between text-xs text-slate-500">
        <span>{minLabel}</span>
        <span>{maxLabel}</span>
      </div>
    </div>
  );
}

// Reusable score comparison bar.
function ScoreBar({ label, score, color, valueColor }) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between text-sm">
        <span className="text-slate-400">{label}</span>

        <span className={`font-semibold ${valueColor}`}>
          {score}/100
        </span>
      </div>

      <div
        className="h-3 overflow-hidden rounded-full bg-slate-800"
        role="progressbar"
        aria-label={`${label} risk score`}
        aria-valuenow={score}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

export default Simulation;
