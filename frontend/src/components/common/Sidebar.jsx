
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  Activity,
  ShieldAlert,
  Bell,
  Clock,
  Bot,
  SlidersHorizontal,
  Satellite,
  Orbit,
} from "lucide-react";

const navigation = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard },
  { name: "Astronauts", path: "/astronauts", icon: Users },
  { name: "Health Monitoring", path: "/health", icon: Activity },
  { name: "Risk Assessment", path: "/risk", icon: ShieldAlert },
  { name: "Alerts", path: "/alerts", icon: Bell },
  { name: "Mission Timeline", path: "/timeline", icon: Clock },
  { name: "AI Assistant", path: "/assistant", icon: Bot },
  { name: "Simulation", path: "/simulation", icon: SlidersHorizontal },
];

function Sidebar() {
  return (
    <>
      {/* Mobile Brand Header */}
      <div className="flex items-center gap-3 border-b border-slate-800 bg-[#0b1425] px-4 py-3 md:hidden">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-cyan-400/20 bg-cyan-400/10">
          <Satellite size={20} className="text-cyan-400" />
        </div>

        <div>
          <h1 className="text-sm font-bold tracking-[0.16em] text-white">
            COSMOCARE
          </h1>
          <p className="text-[9px] uppercase tracking-wider text-slate-500">
            ASTRA Mission Platform
          </p>
        </div>
      </div>

      {/* Desktop Sidebar */}
      <aside className="hidden w-64 shrink-0 flex-col border-r border-slate-800/80 bg-[#0b1425] md:flex">
        <div className="border-b border-slate-800/80 px-5 py-6">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-cyan-400/20 bg-gradient-to-br from-blue-500/20 to-cyan-400/10">
              <Satellite className="h-6 w-6 text-cyan-400" />
            </div>

            <div>
              <h1 className="text-lg font-bold tracking-[0.16em] text-white">
                COSMOCARE
              </h1>
              <p className="mt-0.5 text-[10px] font-medium uppercase tracking-[0.18em] text-slate-500">
                Astronaut Health Systems
              </p>
            </div>
          </div>

          <div className="mt-5 flex items-center gap-2 rounded-lg border border-cyan-400/10 bg-cyan-400/[0.04] px-3 py-2">
            <Orbit size={15} className="text-cyan-400" />
            <span className="text-xs font-medium tracking-wide text-cyan-300">
              ASTRA MISSION PLATFORM
            </span>
          </div>
        </div>

        <nav
          aria-label="Main navigation"
          className="flex-1 space-y-1 overflow-y-auto px-3 py-5"
        >
          <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-600">
            Mission Workspace
          </p>

          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === "/"}
                className={({ isActive }) =>
                  `group relative flex items-center gap-3 rounded-xl px-3 py-3 text-[13px] font-medium transition-all duration-200 ${
                    isActive
                      ? "border border-cyan-400/15 bg-gradient-to-r from-blue-500/15 to-cyan-400/5 text-cyan-300 shadow-[inset_2px_0_0_#22d3ee]"
                      : "border border-transparent text-slate-400 hover:bg-slate-800/60 hover:text-white"
                  }`
                }
              >
                <Icon
                  size={18}
                  strokeWidth={1.8}
                  className="shrink-0 transition-colors group-hover:text-cyan-300"
                />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-slate-800/80 p-4">
          <div className="rounded-xl border border-slate-800 bg-[#101c30] p-3">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400 shadow-[0_0_8px_#22d3ee]" />
              <span className="text-[11px] font-semibold tracking-wide text-slate-300">
                PROTOTYPE ENVIRONMENT
              </span>
            </div>

            <p className="mt-2 text-[11px] leading-relaxed text-slate-500">
              Astronaut health monitoring and risk assessment interface.
            </p>
          </div>

          <p className="mt-4 text-center text-[10px] tracking-wider text-slate-600">
            COSMOCARE • ASTRA PROJECT
          </p>
        </div>
      </aside>

      {/* Mobile Navigation */}
      <nav
        aria-label="Mobile navigation"
        className="flex gap-1 overflow-x-auto border-b border-slate-800 bg-[#0b1425] px-3 py-2 md:hidden"
      >
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              title={item.name}
              className={({ isActive }) =>
                `flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-xs transition ${
                  isActive
                    ? "bg-cyan-400/10 text-cyan-300"
                    : "text-slate-400 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              <Icon size={16} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>
    </>
  );
}

export default Sidebar;
