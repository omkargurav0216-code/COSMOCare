
export const mockAlerts = [
  {
    id: 1,
    title: "Elevated Heart Rate",
    astronaut: "Sarah Chen",
    astronautId: "AST-002",
    severity: "High",
    category: "Cardiovascular",
    time: "10:45 UTC",
    description:
      "Heart rate readings are above the astronaut's illustrative baseline.",
    metrics: "Heart Rate: 88 BPM",
    recommendation:
      "Review recent cardiovascular telemetry and continue monitoring.",
    status: "Active",
  },
  {
    id: 2,
    title: "Reduced Sleep Duration",
    astronaut: "Sarah Chen",
    astronautId: "AST-002",
    severity: "Medium",
    category: "Fatigue",
    time: "09:30 UTC",
    description:
      "Sleep duration is below the illustrative mission target.",
    metrics: "Sleep: 5.8 hours",
    recommendation:
      "Review sleep patterns and recovery trends.",
    status: "Active",
  },
  {
    id: 3,
    title: "Radiation Exposure Update",
    astronaut: "Alex Morgan",
    astronautId: "AST-001",
    severity: "Low",
    category: "Radiation",
    time: "08:15 UTC",
    description:
      "A routine radiation telemetry update has been recorded.",
    metrics: "Exposure: 0.42 mSv",
    recommendation:
      "Continue routine radiation monitoring.",
    status: "Acknowledged",
  },
  {
    id: 4,
    title: "Blood Oxygen Variation",
    astronaut: "Sarah Chen",
    astronautId: "AST-002",
    severity: "Medium",
    category: "Respiratory",
    time: "07:40 UTC",
    description:
      "Blood oxygen readings show a variation from the illustrative baseline.",
    metrics: "SpO₂: 96%",
    recommendation:
      "Review the trend and compare with individual baseline readings.",
    status: "Active",
  },
  {
    id: 5,
    title: "Routine Health Check",
    astronaut: "James Wilson",
    astronautId: "AST-003",
    severity: "Low",
    category: "General",
    time: "06:20 UTC",
    description:
      "Routine health telemetry has been received successfully.",
    metrics: "Monitoring: Complete",
    recommendation:
      "No additional action indicated by this illustrative event.",
    status: "Resolved",
  },
];

// All alert events and severity levels are illustrative prototype data.
// Replace with backend-provided alerts later.
