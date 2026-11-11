
import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft,
  HeartPulse,
  Activity,
  Thermometer,
  Moon,
  Radiation,
  UserRound,
  ShieldCheck,
  Satellite,
  Wind,
  Clock3,
  Gauge,
  Fingerprint,
} from "lucide-react";

import { mockAstronauts } from "../data/mockAstronauts";

const statusStyles = {
  Normal: "border-emerald-400/20 bg-emerald-400/10 text-emerald-400",
  Monitoring: "border-amber-400/20 bg-amber-400/10 text-amber-400",
  Critical: "border-red-400/20 bg-red-400/10 text-red-400",
};

function AstronautDetails() {
  const { id } = useParams();

  const astronaut = mockAstronauts.find((item) => item.id === id);

  if (!astronaut) {
    return (
      <div className="astra-panel flex flex-col items-center px-5 py-16 text-center">
        <UserRound size={36} className="text-slate-600" />

        <h1 className="mt-4 text-xl font-bold text-white">
          Astronaut Not Found
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          No crew profile matches the requested astronaut ID.
        </p>

        <Link
          to="/astronauts"
          className="mt-6 flex items-center gap-2 rounded-lg border border-cyan-400/20 bg-cyan-400/5 px-4 py-2.5 text-sm font-medium text-cyan-400 transition hover:bg-cyan-400/10"
        >
          <ArrowLeft size={16} />
          Return to Astronaut Directory
        </Link>
      </div>
    );
  }

  const initials = astronaut.name
    .split(" ")
    .map((part) => part[0])
    .join("");

  const statusClass =
    statusStyles[astronaut.status] || statusStyles.Normal;

  const metrics = [
    {
      label: "Heart Rate",
      value: astronaut.heartRate,
      unit: "bpm",
      icon: HeartPulse,
      color: "text-rose-400",
      bg: "bg-rose-400/10",
      description: "Cardiovascular indicator",
    },
    {
      label: "Blood Oxygen",
      value: astronaut.spo2,
      unit: "%",
      icon: Wind,
      color: "text-cyan-400",
      bg: "bg-cyan-400/10",
      description: "Oxygen saturation indicator",
    },
    {
      label: "Body Temperature",
      value: astronaut.temperature,
      unit: "°C",
      icon: Thermometer,
      color: "text-amber-400",
      bg: "bg-amber-400/10",
      description: "Body temperature indicator",
    },
    {
      label: "Sleep Duration",
      value: astronaut.sleep,
      unit: "hrs",
      icon: Moon,
      color: "text-purple-400",
      bg: "bg-purple-400/10",
      description: "Sleep monitoring indicator",
    },
    {
      label: "Radiation Exposure",
      value: astronaut.radiation,
      unit: "mSv",
      icon: Radiation,
      color: "text-orange-400",
      bg: "bg-orange-400/10",
      description: "Radiation monitoring indicator",
    },
    {
      label: "Fatigue Level",
      value: astronaut.fatigue,
      unit: "",
      icon: ShieldCheck,
      color: "text-emerald-400",
      bg: "bg-emerald-400/10",
      description: "Fatigue monitoring indicator",
    },
  ];

  return (
    <div className="space-y-7">

      {/* Breadcrumb */}
      <Link
        to="/astronauts"
        className="inline-flex items-center gap-2 text-sm text-slate-400 transition hover:text-cyan-400"
      >
        <ArrowLeft size={16} />
        Back to Astronaut Directory
      </Link>

      {/* Page heading */}
      <section>
        <div className="mb-2 flex items-center gap-2">
          <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
          <p className="text-xs font-semibold tracking-[0.2em] text-cyan-400">
            MISSION CONTROL / CREW PROFILE
          </p>
        </div>

        <h1 className="text-3xl font-bold tracking-tight text-white">
          Astronaut Details
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          Individual astronaut profile and health monitoring indicators.
        </p>
      </section>

      {/* Astronaut identity card */}
      <section className="relative overflow-hidden rounded-2xl border border-cyan-400/15 bg-gradient-to-br from-[#102440] via-[#0d1b30] to-[#0b1425] p-6 md:p-7">
        <div className="pointer-events-none absolute -right-16 -top-20 h-64 w-64 rounded-full border border-cyan-400/10" />
        <div className="pointer-events-none absolute -right-8 -top-12 h-48 w-48 rounded-full border border-cyan-400/10" />

        <div className="relative">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-start">
            <div className="flex items-center gap-5">
              <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10 text-2xl font-bold text-cyan-400">
                {initials}
              </div>

              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <Fingerprint size={15} className="text-cyan-400" />
                  <p className="text-xs font-semibold tracking-widest text-cyan-400">
                    {astronaut.id}
                  </p>
                </div>

                <h2 className="mt-2 text-2xl font-bold text-white">
                  {astronaut.name}
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                  {astronaut.role}
                </p>
              </div>
            </div>

            <div className="flex flex-col items-start gap-2 md:items-end">
              <p className="text-[10px] tracking-widest text-slate-500">
                CURRENT HEALTH STATUS
              </p>

              <span
                className={`rounded-full border px-4 py-2 text-xs font-semibold ${statusClass}`}
              >
                {astronaut.status}
              </span>

              <p className="text-[10px] text-slate-500">
                Illustrative prototype status
              </p>
            </div>
          </div>

          {/* Profile information */}
          <div className="mt-7 grid grid-cols-2 gap-5 border-t border-white/10 pt-6 sm:grid-cols-4">
            <Info label="Age" value={`${astronaut.age} years`} />
            <Info label="Mission" value="ASTRA-01" />
            <Info label="Crew Role" value={astronaut.role} />
            <Info label="Crew Identifier" value={astronaut.id} />
          </div>
        </div>
      </section>

      {/* Health metrics */}
      <section>
        <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-end">
          <div>
            <h2 className="text-lg font-semibold text-white">
              Health Monitoring
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Health indicators for {astronaut.name}
            </p>
          </div>

          <span className="rounded-md border border-blue-400/10 bg-blue-400/5 px-3 py-1.5 text-[10px] font-medium tracking-wider text-blue-300">
            MOCK TELEMETRY
          </span>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {metrics.map((metric) => {
            const Icon = metric.icon;

            return (
              <div
                key={metric.label}
                className="astra-panel astra-panel-hover group p-5"
              >
                <div className="flex items-center justify-between">
                  <div className={`rounded-xl p-2.5 ${metric.bg}`}>
                    <Icon size={20} className={metric.color} />
                  </div>

                  <Gauge
                    size={17}
                    className="text-slate-700 transition group-hover:text-slate-500"
                  />
                </div>

                <p className="mt-5 text-sm font-medium text-slate-300">
                  {metric.label}
                </p>

                <div className="mt-2 flex items-baseline gap-1.5">
                  <span className={`text-2xl font-bold ${metric.color}`}>
                    {metric.value ?? "N/A"}
                  </span>

                  <span className="text-xs text-slate-500">
                    {metric.unit}
                  </span>
                </div>

                <p className="mt-2 text-xs text-slate-500">
                  {metric.description}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Baseline information */}
      <section className="astra-panel p-5 md:p-6">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-cyan-400/10 p-2.5">
            <Activity size={21} className="text-cyan-400" />
          </div>

          <div>
            <h2 className="font-semibold text-white">
              Individual Health Baseline
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Reference profile and monitoring context
            </p>
          </div>
        </div>

        <p className="mt-5 text-sm leading-7 text-slate-400">
          An astronaut's health baseline represents their individual
          reference profile. Current health indicators should be
          evaluated against individual baseline values and mission
          context rather than relying only on population averages.
        </p>

        <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
            <p className="text-xs text-slate-500">
              Individual reference
            </p>
            <p className="mt-2 text-sm font-medium text-slate-300">
              Baseline comparison pending
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
            <p className="text-xs text-slate-500">
              Historical trends
            </p>
            <p className="mt-2 text-sm font-medium text-slate-300">
              Telemetry integration pending
            </p>
          </div>
        </div>

        <div className="mt-4 flex items-start gap-3 rounded-xl border border-blue-400/10 bg-blue-400/[0.04] p-4">
          <Clock3 size={17} className="mt-0.5 shrink-0 text-blue-400" />

          <p className="text-xs leading-relaxed text-slate-400">
            Baseline comparisons and historical trends will be
            incorporated when the agreed backend telemetry and
            astronaut data contracts are available.
          </p>
        </div>
      </section>

      {/* Disclaimer */}
      <div className="rounded-xl border border-blue-400/10 bg-blue-400/[0.04] p-4">
        <p className="text-xs leading-relaxed text-slate-400">
          <span className="font-semibold text-slate-300">
            Prototype environment:
          </span>{" "}
          All astronaut profiles and health values are simulated
          illustrative data. They are not actual astronaut medical
          records or clinical assessments.
        </p>
      </div>
    </div>
  );
}

function Info({ label, value }) {
  return (
    <div className="min-w-0">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-2 break-words text-sm font-medium text-slate-200">
        {value}
      </p>
    </div>
  );
}

export default AstronautDetails;
