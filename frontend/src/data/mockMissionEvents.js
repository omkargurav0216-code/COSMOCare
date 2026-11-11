
import {
  Activity,
  Bell,
  ShieldCheck,
  Radio,
  Rocket,
} from "lucide-react";

export const mockMissionEvents = [
  {
    id: 1,
    date: "09 Nov 2026",
    time: "10:45 UTC",
    title: "Elevated Heart Rate Detected",
    description:
      "An elevated heart rate indicator was recorded for Sarah Chen.",
    astronaut: "Sarah Chen · AST-002",
    category: "Health Alert",
    color: "text-red-400",
    bg: "bg-red-400/10",
    icon: Bell,
    status: "Alert",
  },
  {
    id: 2,
    date: "09 Nov 2026",
    time: "09:30 UTC",
    title: "Sleep Telemetry Updated",
    description:
      "Sleep duration telemetry was received and added to the monitoring dataset.",
    astronaut: "Sarah Chen · AST-002",
    category: "Health Monitoring",
    color: "text-amber-400",
    bg: "bg-amber-400/10",
    icon: Activity,
    status: "Monitoring",
  },
  {
    id: 3,
    date: "09 Nov 2026",
    time: "08:15 UTC",
    title: "Radiation Telemetry Received",
    description:
      "Routine radiation exposure measurements were successfully recorded.",
    astronaut: "Alex Morgan · AST-001",
    category: "Telemetry",
    color: "text-cyan-400",
    bg: "bg-cyan-400/10",
    icon: Radio,
    status: "Recorded",
  },
  {
    id: 4,
    date: "09 Nov 2026",
    time: "07:00 UTC",
    title: "Health Monitoring System Check",
    description:
      "The monitoring system completed an illustrative operational check.",
    astronaut: "Mission Operations",
    category: "System Event",
    color: "text-emerald-400",
    bg: "bg-emerald-400/10",
    icon: ShieldCheck,
    status: "Complete",
  },
  {
    id: 5,
    date: "08 Nov 2026",
    time: "18:30 UTC",
    title: "Mission Monitoring Initiated",
    description:
      "Crew health monitoring and telemetry collection were initialized.",
    astronaut: "Mission Operations",
    category: "Mission Event",
    color: "text-purple-400",
    bg: "bg-purple-400/10",
    icon: Rocket,
    status: "Complete",
  },
];

// All mission events are illustrative prototype data.
// Replace with backend-provided events during integration.
