
import { useMemo, useState } from "react";
import { mockAlerts } from "../data/mockAlerts";

import {
  Bell,
  AlertTriangle,
  ShieldAlert,
  Info,
  Clock3,
  UserRound,
  CheckCircle2,
  Filter,
  Activity,
  Check,
  CircleCheck,
} from "lucide-react";

const severityStyles = {
  High: {
    badge: "border-red-400/20 bg-red-400/10 text-red-400",
    icon: "text-red-400",
  },
  Medium: {
    badge: "border-amber-400/20 bg-amber-400/10 text-amber-400",
    icon: "text-amber-400",
  },
  Low: {
    badge: "border-cyan-400/20 bg-cyan-400/10 text-cyan-400",
    icon: "text-cyan-400",
  },
};

const statusStyles = {
  Active: "text-amber-400 bg-amber-400/10",
  Acknowledged: "text-cyan-400 bg-cyan-400/10",
  Resolved: "text-emerald-400 bg-emerald-400/10",
};

function Alerts() {
  const [alerts, setAlerts] = useState(() =>
    mockAlerts.map((alert, index) => ({
      ...alert,
      id: alert.id ?? `alert-${index}`,
    }))
  );

  const [severityFilter, setSeverityFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");

  // Filter alerts based on selected filters.
  const filteredAlerts = useMemo(
    () =>
      alerts.filter((alert) => {
        const matchesSeverity =
          severityFilter === "All" ||
          alert.severity === severityFilter;

        const matchesStatus =
          statusFilter === "All" ||
          alert.status === statusFilter;

        return matchesSeverity && matchesStatus;
      }),
    [alerts, severityFilter, statusFilter]
  );

  // Prototype-only status update.
  const updateStatus = (id, newStatus) => {
    setAlerts((previousAlerts) =>
      previousAlerts.map((alert) =>
        alert.id === id
          ? { ...alert, status: newStatus }
          : alert
      )
    );
  };

  const activeCount = alerts.filter(
    (alert) => alert.status === "Active"
  ).length;

  const highCount = alerts.filter(
    (alert) => alert.severity === "High"
  ).length;

  const acknowledgedCount = alerts.filter(
    (alert) => alert.status === "Acknowledged"
  ).length;

  const resolvedCount = alerts.filter(
    (alert) => alert.status === "Resolved"
  ).length;

  const clearFilters = () => {
    setSeverityFilter("All");
    setStatusFilter("All");
  };

  return (
    <div className="space-y-7">

      {/* Page heading */}
      <section>
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-cyan-400" />

          <p className="text-xs font-semibold tracking-[0.18em] text-cyan-400">
            MISSION NOTIFICATIONS
          </p>
        </div>

        <div className="mt-2 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
              Alert Management
            </h1>

            <p className="mt-2 text-sm leading-6 text-slate-400">
              Review astronaut health alerts and track monitoring actions
              across the mission.
            </p>
          </div>

          <span className="flex w-fit items-center gap-2 rounded-full border border-slate-700 bg-slate-800/60 px-3 py-2 text-xs text-slate-300">
            <span className="h-2 w-2 rounded-full bg-amber-400" />
            {activeCount} Active Notifications
          </span>
        </div>
      </section>

      {/* Summary cards */}
      <section>
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-white">
            Alert Overview
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Current notification status summary
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <SummaryCard
            label="Active Alerts"
            value={activeCount}
            icon={Bell}
            color="text-amber-400"
            description="Awaiting action"
          />

          <SummaryCard
            label="High Severity"
            value={highCount}
            icon={ShieldAlert}
            color="text-red-400"
            description="High-priority notifications"
          />

          <SummaryCard
            label="Acknowledged"
            value={acknowledgedCount}
            icon={CheckCircle2}
            color="text-cyan-400"
            description="Under review"
          />

          <SummaryCard
            label="Resolved"
            value={resolvedCount}
            icon={CircleCheck}
            color="text-emerald-400"
            description="Marked complete"
          />
        </div>
      </section>

      {/* Filters */}
      <section className="astra-panel p-5">
        <div className="mb-5 flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-blue-500/10 p-2">
              <Filter size={18} className="text-blue-400" />
            </div>

            <div>
              <h2 className="font-semibold text-white">
                Filter Alerts
              </h2>

              <p className="mt-0.5 text-xs text-slate-500">
                Narrow notifications by severity and status.
              </p>
            </div>
          </div>

          {(severityFilter !== "All" || statusFilter !== "All") && (
            <button
              onClick={clearFilters}
              className="w-fit text-xs font-medium text-cyan-400 transition hover:text-cyan-300"
            >
              Clear all filters
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label
              htmlFor="severity-filter"
              className="mb-2 block text-xs font-medium text-slate-400"
            >
              Severity Level
            </label>

            <select
              id="severity-filter"
              value={severityFilter}
              onChange={(event) =>
                setSeverityFilter(event.target.value)
              }
              className="w-full rounded-lg border border-slate-700 bg-[#111f35] px-4 py-3 text-sm text-slate-200 outline-none transition focus:border-cyan-400"
            >
              <option value="All">All Severities</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <div>
            <label
              htmlFor="status-filter"
              className="mb-2 block text-xs font-medium text-slate-400"
            >
              Alert Status
            </label>

            <select
              id="status-filter"
              value={statusFilter}
              onChange={(event) =>
                setStatusFilter(event.target.value)
              }
              className="w-full rounded-lg border border-slate-700 bg-[#111f35] px-4 py-3 text-sm text-slate-200 outline-none transition focus:border-cyan-400"
            >
              <option value="All">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Acknowledged">Acknowledged</option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>
        </div>
      </section>

      {/* Alert list */}
      <section>
        <div className="mb-4 flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-lg font-semibold text-white">
              Recent Alerts
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Mission health notification history
            </p>
          </div>

          <span className="text-xs text-slate-500">
            Showing {filteredAlerts.length} of {alerts.length} alerts
          </span>
        </div>

        <div className="space-y-4">
          {filteredAlerts.length > 0 ? (
            filteredAlerts.map((alert) => (
              <AlertCard
                key={alert.id}
                alert={alert}
                onAcknowledge={() =>
                  updateStatus(alert.id, "Acknowledged")
                }
                onResolve={() =>
                  updateStatus(alert.id, "Resolved")
                }
              />
            ))
          ) : (
            <div className="astra-panel px-5 py-12 text-center">
              <Info
                size={32}
                className="mx-auto text-slate-500"
              />

              <h3 className="mt-3 font-medium text-slate-200">
                No matching alerts
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                No notifications match your selected filters.
              </p>

              <button
                onClick={clearFilters}
                className="mt-4 rounded-lg border border-cyan-400/20 px-4 py-2 text-sm font-medium text-cyan-400 transition hover:bg-cyan-400/10"
              >
                Reset Filters
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Prototype notice */}
      <div className="flex items-start gap-3 rounded-xl border border-amber-400/15 bg-amber-400/5 p-4">
        <Info
          size={17}
          className="mt-0.5 shrink-0 text-amber-400"
        />

        <p className="text-xs leading-5 text-slate-400">
          <span className="font-semibold text-amber-400">
            Prototype notice:
          </span>{" "}
          Alert events, severity levels and suggested actions use
          illustrative mock data. Acknowledge and resolve actions
          currently update local page state only. They are not
          connected to a live notification service or validated
          medical alert system.
        </p>
      </div>
    </div>
  );
}

function SummaryCard({
  label,
  value,
  icon: Icon,
  color,
  description,
}) {
  return (
    <div className="astra-panel astra-panel-hover p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">
          {label}
        </p>

        <div className="rounded-lg bg-slate-800/70 p-2">
          <Icon size={19} className={color} />
        </div>
      </div>

      <p className={`mt-4 text-3xl font-bold ${color}`}>
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {description}
      </p>
    </div>
  );
}

function AlertCard({ alert, onAcknowledge, onResolve }) {
  const severity =
    severityStyles[alert.severity] || severityStyles.Low;

  const status =
    statusStyles[alert.status] || statusStyles.Active;

  const AlertIcon =
    alert.severity === "High"
      ? ShieldAlert
      : alert.severity === "Medium"
        ? AlertTriangle
        : Info;

  const title =
    alert.title ||
    alert.name ||
    alert.description ||
    "Health Monitoring Alert";

  const description =
    alert.title && alert.description
      ? alert.description
      : alert.title || alert.name
        ? alert.description || alert.message || ""
        : alert.message || "";

  const astronaut =
    alert.astronaut ||
    alert.astronautName ||
    "Unknown astronaut";

  const metric =
    alert.metrics ||
    alert.metric ||
    alert.category ||
    "Not specified";

  const recommendation =
    alert.recommendation ||
    alert.suggestedAction ||
    "Continue routine health monitoring.";

  return (
    <article className="astra-panel astra-panel-hover p-5">

      {/* Alert header */}
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
        <div className="flex min-w-0 gap-3">
          <div
            className={`mt-0.5 shrink-0 rounded-xl border p-3 ${severity.badge}`}
          >
            <AlertIcon size={20} />
          </div>

          <div className="min-w-0">
            <h3 className="font-semibold text-white">
              {title}
            </h3>

            <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-slate-500">
              <span className="flex items-center gap-1.5">
                <UserRound size={13} />
                {astronaut}
              </span>

              <span className="flex items-center gap-1.5">
                <Clock3 size={13} />
                {alert.time || "Time unavailable"}
              </span>
            </div>
          </div>
        </div>

        <div className="flex shrink-0 flex-wrap items-center gap-2">
          <span
            className={`rounded-full border px-3 py-1 text-xs font-medium ${severity.badge}`}
          >
            {alert.severity || "Low"} Severity
          </span>

          <span
            className={`rounded-full px-3 py-1 text-xs font-medium ${status}`}
          >
            {alert.status || "Active"}
          </span>
        </div>
      </div>

      {/* Alert details */}
      <div className="mt-5 border-t border-slate-800 pt-4">
        {description && (
          <p className="text-sm leading-6 text-slate-400">
            {description}
          </p>
        )}

        <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-2">
          <div className="rounded-lg border border-slate-800 bg-[#111f35] p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Activity size={14} />
              Contributing Metric
            </div>

            <p className="mt-2 text-sm font-medium text-slate-200">
              {metric}
            </p>
          </div>

          <div className="rounded-lg border border-slate-800 bg-[#111f35] p-4">
            <div className="flex items-center gap-2 text-xs text-cyan-400">
              <CheckCircle2 size={14} />
              Suggested Monitoring Action
            </div>

            <p className="mt-2 text-sm leading-5 text-slate-400">
              {recommendation}
            </p>
          </div>
        </div>

        {/* Alert actions */}
        {alert.status !== "Resolved" && (
          <div className="mt-5 flex flex-wrap gap-3">
            {alert.status === "Active" && (
              <button
                onClick={onAcknowledge}
                className="inline-flex items-center gap-2 rounded-lg border border-cyan-400/25 px-4 py-2.5 text-xs font-medium text-cyan-400 transition hover:bg-cyan-400/10"
              >
                <Check size={14} />
                Acknowledge
              </button>
            )}

            <button
              onClick={onResolve}
              className="inline-flex items-center gap-2 rounded-lg border border-emerald-400/20 bg-emerald-400/10 px-4 py-2.5 text-xs font-medium text-emerald-400 transition hover:bg-emerald-400/20"
            >
              <CheckCircle2 size={14} />
              Mark Resolved
            </button>
          </div>
        )}
      </div>
    </article>
  );
}

export default Alerts;
