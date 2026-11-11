
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  UserRound,
  Activity,
  HeartPulse,
  ArrowUpRight,
  Search,
  Users,
  Filter,
  Satellite,
  Wind,
  BatteryMedium,
} from "lucide-react";

import { mockAstronauts } from "../data/mockAstronauts";

const astronauts = mockAstronauts.map((astronaut) => ({
  ...astronaut,
  mission: "ASTRA-01",
  initials: astronaut.name
    .split(" ")
    .map((part) => part[0])
    .join(""),
  color: {
    "AST-001": "bg-cyan-500/10 text-cyan-400 border-cyan-400/20",
    "AST-002": "bg-purple-500/10 text-purple-400 border-purple-400/20",
    "AST-003": "bg-emerald-500/10 text-emerald-400 border-emerald-400/20",
    "AST-004": "bg-amber-500/10 text-amber-400 border-amber-400/20",
  }[astronaut.id] || "bg-slate-500/10 text-slate-400 border-slate-500/20",
}));

const statusStyles = {
  Normal: "border-emerald-400/20 bg-emerald-400/10 text-emerald-400",
  Monitoring: "border-amber-400/20 bg-amber-400/10 text-amber-400",
  Critical: "border-red-400/20 bg-red-400/10 text-red-400",
};

function Astronauts() {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");

  const totalCrew = astronauts.length;

  const normalCount = astronauts.filter(
    (astronaut) => astronaut.status === "Normal"
  ).length;

  const monitoringCount = astronauts.filter(
    (astronaut) => astronaut.status === "Monitoring"
  ).length;

  const criticalCount = astronauts.filter(
    (astronaut) => astronaut.status === "Critical"
  ).length;

  const filteredAstronauts = useMemo(() => {
    const query = searchTerm.trim().toLowerCase();

    return astronauts.filter((astronaut) => {
      const matchesSearch =
        astronaut.name.toLowerCase().includes(query) ||
        astronaut.id.toLowerCase().includes(query) ||
        astronaut.role.toLowerCase().includes(query);

      const matchesStatus =
        statusFilter === "All" || astronaut.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [searchTerm, statusFilter]);

  return (
    <div className="space-y-7">

      {/* Page heading */}
      <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <div className="mb-2 flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
            <p className="text-xs font-semibold tracking-[0.2em] text-cyan-400">
              MISSION CONTROL / CREW
            </p>
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-white">
            Astronaut Directory
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            Crew profiles and individual health monitoring indicators.
          </p>
        </div>

        <div className="flex items-center gap-3 rounded-xl border border-cyan-400/15 bg-cyan-400/5 px-4 py-3">
          <Satellite size={21} className="text-cyan-400" />
          <div>
            <p className="text-[10px] tracking-widest text-slate-500">
              MISSION
            </p>
            <p className="mt-1 text-sm font-bold text-white">ASTRA-01</p>
          </div>
        </div>
      </section>

      {/* Crew summary */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-slate-300">
            Crew Statistics
          </h2>
          <span className="text-[10px] tracking-wider text-slate-500">
            ILLUSTRATIVE DATA
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <SummaryCard
            label="Total Crew"
            value={totalCrew}
            icon={Users}
            color="text-cyan-400"
            bg="bg-cyan-400/10"
          />

          <SummaryCard
            label="Normal"
            value={normalCount}
            icon={Activity}
            color="text-emerald-400"
            bg="bg-emerald-400/10"
          />

          <SummaryCard
            label="Monitoring"
            value={monitoringCount}
            icon={HeartPulse}
            color="text-amber-400"
            bg="bg-amber-400/10"
          />

          <SummaryCard
            label="Critical"
            value={criticalCount}
            icon={Filter}
            color="text-red-400"
            bg="bg-red-400/10"
          />
        </div>
      </section>

      {/* Search and filters */}
      <section className="astra-panel p-4">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex min-w-0 flex-1 items-center gap-3 rounded-lg border border-slate-700/80 bg-slate-950/40 px-4 py-3">
            <Search size={18} className="shrink-0 text-slate-500" />

            <input
              type="text"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search by astronaut name, ID or role..."
              className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
            />

            {searchTerm && (
              <button
                onClick={() => setSearchTerm("")}
                className="text-xs text-slate-400 hover:text-white"
              >
                Clear
              </button>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <span className="mr-1 text-xs text-slate-500">Status:</span>

            {["All", "Normal", "Monitoring", "Critical"].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`rounded-lg border px-3 py-2 text-xs font-medium transition ${
                  statusFilter === status
                    ? "border-cyan-400/30 bg-cyan-400/10 text-cyan-300"
                    : "border-slate-700 bg-slate-900/50 text-slate-400 hover:border-slate-500 hover:text-white"
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-3 text-xs text-slate-500">
          Showing {filteredAstronauts.length} of {totalCrew} crew members
        </div>
      </section>

      {/* Astronaut cards */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-slate-300">
            Crew Profiles
          </h2>
          <span className="text-xs text-slate-500">
            {filteredAstronauts.length} profiles
          </span>
        </div>

        {filteredAstronauts.length > 0 ? (
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
            {filteredAstronauts.map((astronaut) => (
              <AstronautCard
                key={astronaut.id}
                astronaut={astronaut}
              />
            ))}
          </div>
        ) : (
          <div className="astra-panel px-5 py-14 text-center">
            <Search size={30} className="mx-auto text-slate-600" />
            <h3 className="mt-4 font-semibold text-white">
              No astronauts found
            </h3>
            <p className="mt-2 text-sm text-slate-500">
              Try changing your search or status filter.
            </p>
            <button
              onClick={() => {
                setSearchTerm("");
                setStatusFilter("All");
              }}
              className="mt-5 rounded-lg border border-cyan-400/20 bg-cyan-400/5 px-4 py-2 text-xs font-medium text-cyan-400 hover:bg-cyan-400/10"
            >
              Reset filters
            </button>
          </div>
        )}
      </section>

      {/* Disclaimer */}
      <div className="rounded-xl border border-blue-400/10 bg-blue-400/[0.04] p-4">
        <p className="text-xs leading-relaxed text-slate-400">
          <span className="font-semibold text-slate-300">
            Prototype environment:
          </span>{" "}
          Astronaut profiles and health indicators are illustrative mock data.
          They do not represent actual astronaut telemetry or clinical
          assessments.
        </p>
      </div>
    </div>
  );
}

function SummaryCard({ label, value, icon: Icon, color, bg }) {
  return (
    <div className="astra-panel astra-panel-hover p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">{label}</p>
        <div className={`rounded-xl p-2.5 ${bg}`}>
          <Icon size={19} className={color} />
        </div>
      </div>

      <p className={`mt-5 text-3xl font-bold ${color}`}>
        {String(value).padStart(2, "0")}
      </p>

      <p className="mt-2 text-xs text-slate-500">
        Crew members
      </p>
    </div>
  );
}

function AstronautCard({ astronaut }) {
  const statusClass =
    statusStyles[astronaut.status] || statusStyles.Normal;

  return (
    <div className="astra-panel astra-panel-hover group p-5 md:p-6">
      {/* Identity */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-center gap-4">
          <div
            className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-xl border text-lg font-bold ${astronaut.color}`}
          >
            {astronaut.initials}
          </div>

          <div className="min-w-0">
            <h3 className="truncate text-base font-semibold text-white">
              {astronaut.name}
            </h3>

            <p className="mt-1 text-sm text-slate-400">
              {astronaut.role}
            </p>

            <p className="mt-1 text-xs tracking-wide text-slate-500">
              {astronaut.id}
            </p>
          </div>
        </div>

        <span
          className={`shrink-0 rounded-full border px-3 py-1.5 text-[10px] font-semibold ${statusClass}`}
        >
          {astronaut.status}
        </span>
      </div>

      {/* Metrics */}
      <div className="my-5 grid grid-cols-3 gap-3 border-y border-slate-800/80 py-5">
        <Metric
          label="Heart Rate"
          value={`${astronaut.heartRate} bpm`}
          icon={HeartPulse}
          color="text-rose-400"
        />

        <Metric
          label="SpO₂"
          value={`${astronaut.spo2}%`}
          icon={Wind}
          color="text-cyan-400"
        />

        <Metric
          label="Fatigue"
          value={astronaut.fatigue}
          icon={BatteryMedium}
          color="text-amber-400"
        />
      </div>

      {/* Footer */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-[10px] tracking-wider text-slate-500">
            ASSIGNED MISSION
          </p>
          <p className="mt-1 text-xs font-medium text-slate-300">
            {astronaut.mission}
          </p>
        </div>

        <Link
          to={`/astronauts/${astronaut.id}`}
          className="flex items-center gap-2 rounded-lg border border-cyan-400/20 bg-cyan-400/5 px-4 py-2.5 text-xs font-semibold text-cyan-400 transition hover:border-cyan-400/40 hover:bg-cyan-400/10"
        >
          View Profile
          <ArrowUpRight size={15} />
        </Link>
      </div>
    </div>
  );
}

function Metric({ label, value, icon: Icon, color }) {
  return (
    <div className="min-w-0">
      <div className="flex items-center gap-1.5">
        <Icon size={14} className={color} />
        <p className="truncate text-[10px] text-slate-500 sm:text-xs">
          {label}
        </p>
      </div>

      <p className="mt-2 truncate text-sm font-semibold text-slate-200">
        {value}
      </p>
    </div>
  );
}

export default Astronauts;
