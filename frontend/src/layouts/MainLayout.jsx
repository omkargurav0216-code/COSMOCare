
import { Outlet } from "react-router-dom";
import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";

function MainLayout() {
  return (
    <div className="min-h-screen bg-[#080f1e] text-slate-200">
      <div className="flex min-h-screen flex-col md:flex-row">
        <Sidebar />

        <div className="flex min-w-0 flex-1 flex-col">
          <Navbar />

          <main className="w-full flex-1 p-4 md:p-6 lg:p-8">
            <Outlet />
          </main>

          <footer className="border-t border-slate-800/70 px-5 py-3 md:px-8">
            <p className="text-[10px] tracking-wide text-slate-600">
              COSMOCARE • ASTRA PROTOTYPE • ILLUSTRATIVE DATA
            </p>
          </footer>
        </div>
      </div>
    </div>
  );
}

export default MainLayout;
