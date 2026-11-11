
import {
  Rocket,
  Activity,
  Bell,
  ShieldCheck,
  Clock,
  CalendarDays,
  Info,
} from "lucide-react";

import { mockMissionEvents } from "../data/mockMissionEvents";

function MissionTimeline() {
  const events = mockMissionEvents;

  // Derive summary counts from centralized event data.
  const totalEvents = events.length;

  const healthAlerts = events.filter(
    (event) => event.category === "Health Alert"
  ).length;

  const systemEvents = events.filter(
    (event) => event.category === "System Event"
  ).length;

  return (
    <div className="space-y-7">

      {/* Page heading */}
      <section>
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-cyan-400" />

          <p className="text-xs font-semibold tracking-[0.18em] text-cyan-400">
            MISSION ACTIVITY LOG
          </p>
        </div>

        <h1 className="mt-2 text-2xl font-bold tracking-tight text-white sm:text-3xl">
          Mission Timeline
        </h1>

        <p className="mt-2 text-sm leading-6 text-slate-400">
          Chronological overview of mission operations and astronaut
          health-monitoring events.
        </p>
      </section>

      {/* Mission overview */}
      <section className="astra-panel p-5">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
          <div className="flex items-center gap-3">
            <div className="rounded-xl border border-cyan-400/15 bg-cyan-400/10 p-3">
              <Rocket className="text-cyan-400" size={23} />
            </div>

            <div>
              <p className="text-xs font-medium tracking-wider text-slate-500">
                ACTIVE MISSION
              </p>

              <h2 className="mt-1 text-lg font-semibold text-white">
                ASTRA-01
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Mission Operations Timeline
              </p>
            </div>
          </div>

          <div className="flex w-fit items-center gap-2 rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2.5">
            <CalendarDays size={17} className="text-cyan-400" />

            <span className="text-xs text-slate-400">
              Mission Activity History
            </span>
          </div>
        </div>
      </section>

      {/* Event summary */}
      <section>
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-white">
            Activity Overview
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Summary of recorded mission events
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Summary
            label="Total Events"
            value={totalEvents}
            icon={Activity}
            description="Recorded activities"
          />

          <Summary
            label="Health Alerts"
            value={String(healthAlerts).padStart(2, "0")}
            icon={Bell}
            description="Astronaut health notifications"
          />

          <Summary
            label="System Events"
            value={String(systemEvents).padStart(2, "0")}
            icon={ShieldCheck}
            description="Mission system activities"
          />
        </div>
      </section>

      {/* Timeline */}
      <section className="astra-panel p-5 sm:p-7">
        <div className="mb-7 flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-lg font-semibold text-white">
              Mission Event History
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Chronological record of mission activities
            </p>
          </div>

          <span className="w-fit rounded-full border border-slate-700 bg-slate-800/50 px-3 py-1.5 text-xs text-slate-400">
            {totalEvents} Recorded Events
          </span>
        </div>

        {events.length > 0 ? (
          <div className="space-y-0">
            {events.map((event, index) => {
              const Icon = event.icon || Activity;

              return (
                <div
                  key={event.id ?? index}
                  className="relative flex gap-4 sm:gap-6"
                >
                  {/* Timeline marker and connector */}
                  <div className="flex shrink-0 flex-col items-center">
                    <div
                      className={`z-10 flex h-11 w-11 items-center justify-center rounded-xl border border-white/5 ${
                        event.bg || "bg-slate-800"
                      }`}
                    >
                      <Icon
                        size={20}
                        className={event.color || "text-cyan-400"}
                      />
                    </div>

                    {index !== events.length - 1 && (
                      <div className="min-h-24 w-px flex-1 bg-gradient-to-b from-slate-700 to-slate-800/30" />
                    )}
                  </div>

                  {/* Event information */}
                  <div className="min-w-0 flex-1 pb-8">
                    <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
                      <span className="text-xs font-semibold tracking-wide text-cyan-400">
                        {event.category}
                      </span>

                      <div className="flex items-center gap-2 text-xs text-slate-500">
                        <Clock size={13} />
                        <span>{event.time}</span>
                      </div>
                    </div>

                    <div className="mt-2 rounded-xl border border-slate-800/80 bg-slate-900/30 p-4 transition hover:border-slate-700">
                      <h3 className="font-semibold text-white">
                        {event.title}
                      </h3>

                      <p className="mt-2 text-sm leading-6 text-slate-400">
                        {event.description}
                      </p>

                      <div className="mt-4 flex flex-wrap items-center gap-3">
                        {event.astronaut && (
                          <span className="text-xs text-slate-500">
                            {event.astronaut}
                          </span>
                        )}

                        {event.status && (
                          <span
                            className={`rounded-full px-3 py-1 text-xs font-medium ${
                              event.bg || "bg-slate-800"
                            } ${
                              event.color || "text-slate-400"
                            }`}
                          >
                            {event.status}
                          </span>
                        )}
                      </div>

                      <div className="mt-3 border-t border-slate-800/70 pt-3">
                        <p className="text-xs text-slate-500">
                          {event.date}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="py-12 text-center">
            <Info
              size={32}
              className="mx-auto text-slate-500"
            />

            <h3 className="mt-3 font-medium text-slate-200">
              No mission events available
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Mission activity records will appear here when available.
            </p>
          </div>
        )}
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
          Timeline entries and event details use illustrative sample data.
          Actual mission events will be populated through backend
          integration after the API contract is finalized.
        </p>
      </div>
    </div>
  );
}

function Summary({
  label,
  value,
  icon: Icon,
  description,
}) {
  return (
    <div className="astra-panel astra-panel-hover p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">
          {label}
        </p>

        <div className="rounded-lg bg-slate-800/70 p-2">
          <Icon size={19} className="text-cyan-400" />
        </div>
      </div>

      <p className="mt-4 text-3xl font-bold text-white">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {description}
      </p>
    </div>
  );
}

export default MissionTimeline;
