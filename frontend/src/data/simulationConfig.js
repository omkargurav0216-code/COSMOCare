
export const simulationConfig = {
  baselineScore: 38,

  defaults: {
    sleep: 7,
    heartRate: 72,
    radiation: 0.3,
  },

  ranges: {
    sleep: {
      min: 2,
      max: 12,
      step: 0.5,
    },
    heartRate: {
      min: 50,
      max: 130,
      step: 1,
    },
    radiation: {
      min: 0,
      max: 2,
      step: 0.1,
    },
  },
};

// These values are illustrative prototype configuration.
// Replace or configure them according to the agreed backend/ML contract.
