
import { lazy, Suspense } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
} from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

// Lazy-loaded pages
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Astronauts = lazy(() => import("./pages/Astronauts"));
const AstronautDetails = lazy(() => import("./pages/AstronautDetails"));
const HealthMonitoring = lazy(() => import("./pages/HealthMonitoring"));
const RiskAssessment = lazy(() => import("./pages/RiskAssessment"));
const Alerts = lazy(() => import("./pages/Alerts"));
const MissionTimeline = lazy(() => import("./pages/MissionTimeline"));
const Assistant = lazy(() => import("./pages/Assistant"));
const Simulation = lazy(() => import("./pages/Simulation"));

// Loading fallback
function LoadingFallback() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#080f1e]">
      <div className="text-center">
        <div className="mx-auto mb-4 h-10 w-10 animate-spin rounded-full border-4 border-slate-700 border-t-cyan-400" />

        <p className="text-sm font-medium text-cyan-400">
          Loading mission module...
        </p>

        <p className="mt-2 text-xs text-slate-500">
          ASTRA Mission Control
        </p>
      </div>
    </div>
  );
}

// 404 page
function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[#080f1e] px-4 text-center">
      <p className="text-sm font-semibold tracking-widest text-cyan-400">
        ASTRA MISSION CONTROL
      </p>

      <h1 className="mt-4 text-7xl font-bold text-white">
        404
      </h1>

      <h2 className="mt-4 text-xl font-semibold text-slate-200">
        Mission module not found
      </h2>

      <p className="mt-3 max-w-md text-sm leading-6 text-slate-400">
        The requested destination does not exist or may have been moved.
        Return to the mission dashboard to continue.
      </p>

      <Link
        to="/"
        className="mt-7 rounded-lg bg-cyan-500 px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
      >
        Return to Dashboard
      </Link>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          {/* Main application layout */}
          <Route element={<MainLayout />}>
            <Route path="/" element={<Dashboard />} />

            {/* Astronaut modules */}
            <Route path="/astronauts" element={<Astronauts />} />
            <Route
              path="/astronauts/:id"
              element={<AstronautDetails />}
            />

            {/* Health and risk modules */}
            <Route
              path="/health"
              element={<HealthMonitoring />}
            />
            <Route
              path="/risk"
              element={<RiskAssessment />}
            />

            {/* Mission management modules */}
            <Route path="/alerts" element={<Alerts />} />
            <Route
              path="/timeline"
              element={<MissionTimeline />}
            />

            {/* AI and simulation modules */}
            <Route path="/assistant" element={<Assistant />} />
            <Route path="/simulation" element={<Simulation />} />
          </Route>

          {/* Invalid URL fallback */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

export default App;
