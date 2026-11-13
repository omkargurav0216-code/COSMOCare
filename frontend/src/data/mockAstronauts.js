
export const mockAstronauts = [
  {
    astronaut_id: "AST-001",
    name: "Alex Morgan",
    role: "Mission Commander",
    mission: "ASTRA-01",
    status: "Normal",
    age: 42,

    // Illustrative telemetry values
    heart_rate_bpm: 72,
    spo2_percent: 98,
    body_temperature_celsius: 36.8,
    sleep_hours_last_24h: 7.5,

    // Awaiting validated measurements
    fatigue_level_0_10: null,
    radiation_dose_rate_usv_per_hour: null,

    baseline: "Normal",
  },
  {
    astronaut_id: "AST-002",
    name: "Sarah Chen",
    role: "Flight Engineer",
    mission: "ASTRA-01",
    status: "Monitoring",
    age: 36,

    heart_rate_bpm: 88,
    spo2_percent: 96,
    body_temperature_celsius: 37.1,
    sleep_hours_last_24h: 5.8,

    fatigue_level_0_10: null,
    radiation_dose_rate_usv_per_hour: null,

    baseline: "Normal",
  },
  {
    astronaut_id: "AST-003",
    name: "James Wilson",
    role: "Medical Officer",
    mission: "ASTRA-01",
    status: "Normal",
    age: 39,

    heart_rate_bpm: 68,
    spo2_percent: 99,
    body_temperature_celsius: 36.6,
    sleep_hours_last_24h: 8.0,

    fatigue_level_0_10: null,
    radiation_dose_rate_usv_per_hour: null,

    baseline: "Normal",
  },
  {
    astronaut_id: "AST-004",
    name: "Elena Rodriguez",
    role: "Research Specialist",
    mission: "ASTRA-01",
    status: "Normal",
    age: 34,

    heart_rate_bpm: 75,
    spo2_percent: 98,
    body_temperature_celsius: 36.9,
    sleep_hours_last_24h: 7.2,

    fatigue_level_0_10: null,
    radiation_dose_rate_usv_per_hour: null,

    baseline: "Normal",
  },
];

// Illustrative prototype records, not actual astronaut telemetry.
// Replace with validated backend-provided records during integration.
