
import {
  Users,
  Activity,
  ShieldAlert,
  Bell,
  Clock3,
  Orbit,
  ArrowUpRight,
  Satellite,
  AlertTriangle,
} from "lucide-react";
import { Link } from "react-router-dom";

import { mockAstronauts } from "../data/mockAstronauts";
import { mockAlerts } from "../data/mockAlerts";

function Dashboard() {
  // Crew status calculations
  const totalCrew = mockAstronauts.length;

  const normalCount = mockAstronauts.filter(
    (astronaut) => astronaut.status === "Normal"
  ).length;

  const monitoringCount = mockAstronauts.filter(
    (astronaut) => astronaut.status === "Monitoring"
  ).length;

  const criticalCount = mockAstronauts.filter(
    (astronaut) => astronaut.status === "Critical"
  ).length;

  const activeAlerts = mockAlerts.filter(
    (alert) => alert.status === "Active"
  );

  const activeAlertsCount = activeAlerts.length;

  const crewHealth = [
    {
      name: "Normal",
      count: normalCount,
      color: "bg-emerald-400",
      text: "text-emerald-400",
    },
    {
      name: "Monitoring",
      count: monitoringCount,
      color: "bg-amber-400",
      text: "text-amber-400",
    },
    {
      name: "Critical",
      count: criticalCount,
      color: "bg-red-400",
      text: "text-red-400",
    },
  ];

  const stats = [
    {
      title: "Total Astronauts",
      value: String(totalCrew).padStart(2, "0"),
      subtitle: "Crew members in mission",
      icon: Users,
      color: "text-cyan-400",
      bg: "bg-cyan-400/10",
    },
    {
      title: "Crew Monitoring",
      value: String(monitoringCount + criticalCount).padStart(2, "0"),
      subtitle: "Require additional attention",
      icon: Activity,
      color: "text-amber-400",
      bg: "bg-amber-400/10",
    },
    {
      title: "Risk Assessment",
      value: "Low",
      subtitle: "Illustrative prototype result",
      icon: ShieldAlert,
      color: "text-emerald-400",
      bg: "bg-emerald-400/10",
    },
    {
      title: "Active Alerts",
      value: String(activeAlertsCount).padStart(2, "0"),
      subtitle: "Currently active mock alerts",
      icon: Bell,
      color: "text-red-400",
      bg: "bg-red-400/10",
    },
  ];

  const severityStyles = {
    High: "border-red-400/20 bg-red-400/10 text-red-400",
    Medium: "border-amber-400/20 bg-amber-400/10 text-amber-400",
    Low: "border-cyan-400/20 bg-cyan-400/10 text-cyan-400",
  };

  return (
    <div className="space-y-7">

      {/* Page heading */}
      <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <div className="mb-2 flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
            <p className="text-xs font-semibold tracking-[0.2em] text-cyan-400">
              MISSION CONTROL / OVERVIEW
            </p>
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-white">
            Mission Dashboard
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            Astronaut health monitoring and mission risk overview.
          </p>
        </div>

        <div className="flex items-center gap-3 rounded-xl border border-cyan-400/15 bg-cyan-400/5 px-4 py-3">
          <div className="rounded-lg bg-cyan-400/10 p-2.5">
            <Orbit size={22} className="text-cyan-400" />
          </div>

          <div>
            <p className="text-[10px] font-medium tracking-widest text-slate-500">
              MISSION IDENTIFIER
            </p>
            <p className="mt-1 text-sm font-bold text-white">ASTRA-01</p>
          </div>
        </div>
      </section>

      {/* Mission overview */}
      <section className="relative overflow-hidden rounded-2xl border border-blue-400/15 bg-gradient-to-br from-[#102440] via-[#0d1b30] to-[#0b1425] p-6 md:p-7">
        <div className="pointer-events-none absolute -right-12 -top-24 h-64 w-64 rounded-full border border-cyan-400/10" />
        <div className="pointer-events-none absolute -right-4 -top-16 h-48 w-48 rounded-full border border-cyan-400/10" />

        <div className="relative flex flex-col justify-between gap-6 md:flex-row md:items-center">
          <div>
            <div className="flex items-center gap-2">
              <Satellite size={17} className="text-cyan-400" />
              <p className="text-xs font-semibold tracking-widest text-cyan-400">
                CURRENT MISSION
              </p>
            </div>

            <h2 className="mt-3 text-xl font-bold text-white md:text-2xl">
              Deep Space Exploration
            </h2>

            <p className="mt-2 max-w-lg text-sm leading-relaxed text-slate-400">
              An astronaut health monitoring and risk assessment prototype
              designed to support long-duration space missions.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <div className="min-w-32 rounded-xl border border-white/5 bg-white/[0.04] p-4">
              <p className="text-[10px] tracking-wider text-slate-500">
                CREW SIZE
              </p>
              <p className="mt-2 text-2xl font-bold text-white">
                {String(totalCrew).padStart(2, "0")}
              </p>
            </div>

            <div className="min-w-32 rounded-xl border border-white/5 bg-white/[0.04] p-4">
              <p className="text-[10px] tracking-wider text-slate-500">
                ENVIRONMENT
              </p>
              <p className="mt-2 text-lg font-bold text-cyan-400">
                DEMO MODE
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* KPI cards */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold tracking-wide text-slate-300">
            Mission Statistics
          </h2>
          <span className="text-[10px] tracking-wider text-slate-500">
            MOCK DATA
          </span>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {stats.map((stat) => {
            const Icon = stat.icon;

            return (
              <div
                key={stat.title}
                className="astra-panel astra-panel-hover group p-5"
              >
                <div className="flex items-center justify-between">
                  <p className="text-sm text-slate-400">{stat.title}</p>

                  <div className={`rounded-xl p-2.5 ${stat.bg}`}>
                    <Icon size={19} className={stat.color} />
                  </div>
                </div>

                <div className="mt-5 flex items-end justify-between">
                  <h3 className={`text-3xl font-bold tracking-tight ${stat.color}`}>
                    {stat.value}
                  </h3>

                  <ArrowUpRight
                    size={17}
                    className="mb-1 text-slate-600 transition group-hover:text-cyan-400"
                  />
                </div>

                <p className="mt-2 text-xs text-slate-500">
                  {stat.subtitle}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Crew health and alerts */}
      <section className="grid grid-cols-1 gap-5 xl:grid-cols-2">

        {/* Crew health overview */}
        <div className="astra-panel p-5 md:p-6">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-base font-semibold text-white">
                Crew Health Overview
              </h2>
              <p className="mt-1 text-xs text-slate-500">
                Distribution of current crew status
              </p>
            </div>

            <div className="rounded-lg bg-cyan-400/10 p-2.5">
              <Activity size={19} className="text-cyan-400" />
            </div>
          </div>

          {/* Crew distribution */}
          <div className="mt-7">
            <div className="flex items-end justify-between">
              <div>
                <p className="text-3xl font-bold text-white">
                  {totalCrew}
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  Total crew members
                </p>
              </div>

              <Link
                to="/astronauts"
                className="flex items-center gap-1 text-xs font-medium text-cyan-400 transition hover:text-cyan-300"
              >
                View crew <ArrowUpRight size={14} />
              </Link>
            </div>

            <div className="mt-5 flex h-3 overflow-hidden rounded-full bg-slate-800">
              {crewHealth.map((item) => (
                <div
                  key={item.name}
                  className={`${item.color} transition-all duration-500`}
                  style={{
                    width: `${totalCrew ? (item.count / totalCrew) * 100 : 0}%`,
                  }}
                />
              ))}
            </div>

            <div className="mt-6 space-y-5">
              {crewHealth.map((item) => (
                <div key={item.name}>
                  <div className="mb-2 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={`h-2 w-2 rounded-full ${item.color}`} />
                      <span className="text-sm text-slate-300">
                        {item.name}
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className={`text-sm font-semibold ${item.text}`}>
                        {item.count}
                      </span>
                      <span className="w-10 text-right text-xs text-slate-500">
                        {totalCrew
                          ? Math.round((item.count / totalCrew) * 100)
                          : 0}%
                      </span>
                    </div>
                  </div>

                  <div className="h-1.5 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className={`h-full rounded-full ${item.color} transition-all duration-500`}
                      style={{
                        width: `${totalCrew ? (item.count / totalCrew) * 100 : 0}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent alerts */}
        <div className="astra-panel p-5 md:p-6">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-base font-semibold text-white">
                Recent Alerts
              </h2>
              <p className="mt-1 text-xs text-slate-500">
                Latest astronaut monitoring alerts
              </p>
            </div>

            <div className="rounded-lg bg-amber-400/10 p-2.5">
              <AlertTriangle size={19} className="text-amber-400" />
            </div>
          </div>

          <div className="mt-5 space-y-3">
            {mockAlerts.slice(0, 4).map((alert, index) => (
              <div
                key={alert.id ?? `${alert.description}-${index}`}
                className="flex items-start justify-between gap-3 rounded-xl border border-slate-800/80 bg-slate-900/40 p-3.5 transition hover:border-slate-700"
              >
                <div className="flex min-w-0 gap-3">
                  <div className="mt-0.5 rounded-lg bg-slate-800 p-2">
                    <Bell size={15} className="text-slate-400" />
                  </div>

                  <div className="min-w-0">
                    <p className="text-sm font-medium text-slate-200">
                      {alert.description}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {alert.category} · {alert.time}
                    </p>
                  </div>
                </div>

                <span
                  className={`shrink-0 rounded-md border px-2 py-1 text-[10px] font-semibold ${
                    severityStyles[alert.severity] ||
                    "border-slate-700 bg-slate-800 text-slate-400"
                  }`}
                >
                  {alert.severity}
                </span>
              </div>
            ))}

            {mockAlerts.length === 0 && (
              <div className="rounded-xl border border-dashed border-slate-700 p-8 text-center">
                <Bell className="mx-auto text-slate-600" size={25} />
                <p className="mt-3 text-sm text-slate-400">
                  No alerts available.
                </p>
              </div>
            )}
          </div>

          <Link
            to="/alerts"
            className="mt-5 flex items-center justify-center gap-2 rounded-lg border border-slate-700 py-2.5 text-xs font-medium text-slate-300 transition hover:border-cyan-400/30 hover:text-cyan-400"
          >
            View all alerts <ArrowUpRight size={14} />
          </Link>
        </div>
      </section>

      {/* Prototype disclaimer */}
      <div className="flex items-start gap-3 rounded-xl border border-blue-400/10 bg-blue-400/[0.04] p-4">
        <Clock3 size={16} className="mt-0.5 shrink-0 text-blue-400" />

        <p className="text-xs leading-relaxed text-slate-400">
          <span className="font-semibold text-slate-300">
            Prototype environment:
          </span>{" "}
          All displayed health indicators, alerts and risk values are
          illustrative mock data. No live astronaut telemetry or clinical
          predictions are being generated.
        </p>
      </div>
    </div>
  );
}

export default Dashboard;
