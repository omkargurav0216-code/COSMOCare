
const astronautId = "AST-001";

// Illustrative chart samples only.
// These records are NOT the historical dataset required by the ML model.

export const mockTelemetry = {
  astronaut_id: astronautId,

  data_type: "illustrative_chart_samples",

  "24h": [
    {
      timestamp: "2026-11-12T00:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 68,
      spo2_percent: 98,
      sleep_chart_hours: 0.8,
      body_temperature_celsius: 36.6,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-12T04:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 65,
      spo2_percent: 99,
      sleep_chart_hours: 1.2,
      body_temperature_celsius: 36.5,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-12T08:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 72,
      spo2_percent: 98,
      sleep_chart_hours: 0.2,
      body_temperature_celsius: 36.8,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-12T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 78,
      spo2_percent: 97,
      sleep_chart_hours: 0,
      body_temperature_celsius: 37.0,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-12T16:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 74,
      spo2_percent: 98,
      sleep_chart_hours: 0,
      body_temperature_celsius: 36.9,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-12T20:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 70,
      spo2_percent: 98,
      sleep_chart_hours: 0.5,
      body_temperature_celsius: 36.7,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
  ],

  "7d": [
    {
      timestamp: "2026-11-06T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 70,
      spo2_percent: 98,
      sleep_chart_hours: 7.5,
      body_temperature_celsius: 36.7,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-07T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 72,
      spo2_percent: 97,
      sleep_chart_hours: 6.8,
      body_temperature_celsius: 36.8,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-08T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 75,
      spo2_percent: 98,
      sleep_chart_hours: 7.2,
      body_temperature_celsius: 36.9,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-09T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 73,
      spo2_percent: 99,
      sleep_chart_hours: 8.0,
      body_temperature_celsius: 36.6,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-10T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 78,
      spo2_percent: 97,
      sleep_chart_hours: 6.2,
      body_temperature_celsius: 37.0,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-11T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 72,
      spo2_percent: 98,
      sleep_chart_hours: 7.5,
      body_temperature_celsius: 36.8,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
    {
      timestamp: "2026-11-12T12:00:00Z",
      astronaut_id: astronautId,
      heart_rate_bpm: 70,
      spo2_percent: 98,
      sleep_chart_hours: 7.8,
      body_temperature_celsius: 36.7,
      fatigue_level_0_10: null,
      radiation_dose_rate_usv_per_hour: null,
    },
  ],
};

// These samples are illustrative UI chart data.
// They are not validated ML input or a complete historical baseline.
// Replace with backend telemetry when the API contract is finalized.
