
import {
  Radio,
  Clock3,
} from "lucide-react";

function Navbar() {
  return (
    <header className="sticky top-0 z-20 flex min-h-16 items-center justify-between border-b border-slate-800/80 bg-[#0b1425]/95 px-4 backdrop-blur-xl md:px-8">

      {/* Mission Identity */}
      <div>
        <div className="flex items-center gap-2">
          <p className="text-sm font-semibold tracking-wide text-white">
            Mission Operations
          </p>

          <span className="hidden rounded border border-blue-400/20 bg-blue-400/10 px-2 py-0.5 text-[9px] font-semibold tracking-wider text-blue-300 sm:inline-flex">
            ASTRA-01
          </span>
        </div>

        <p className="mt-0.5 text-[11px] text-slate-500">
          Astronaut Health & Risk Monitoring
        </p>
      </div>

      {/* Mission Status */}
      <div className="flex items-center gap-3 sm:gap-5">

        {/* Telemetry Information */}
        <div className="hidden items-center gap-2 sm:flex">
          <Radio size={15} className="text-cyan-400" />
          <span className="text-[11px] text-slate-400">
            Telemetry Preview
          </span>
        </div>

        {/* Monitoring Information */}
        <div className="hidden items-center gap-2 md:flex">
          <Clock3 size={14} className="text-slate-500" />
          <span className="text-[11px] text-slate-400">
            Mission Monitoring
          </span>
        </div>

        {/* Prototype Status */}
        <div className="flex items-center gap-2 rounded-full border border-amber-400/10 bg-amber-400/5 px-3 py-1.5">
          <span className="h-2 w-2 rounded-full bg-amber-400" />

          <span className="text-[11px] font-medium text-amber-300">
            Demo Mode
          </span>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
