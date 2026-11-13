"""
COSMOCare - Synthetic Astronaut Telemetry Generator

Generates simulated astronaut health telemetry for developing
and testing the COSMOCare machine-learning pipeline.

IMPORTANT:
All generated records are synthetic and are not real astronaut data.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# Reproducibility: running the script again produces the same dataset.
RANDOM_SEED = 42

# Dataset configuration
NUM_ASTRONAUTS = 4
DAYS = 14
READINGS_PER_DAY = 24

ASTRONAUT_IDS = [
    "ASTRO_001",
    "ASTRO_002",
    "ASTRO_003",
    "ASTRO_004",
]


def generate_telemetry(seed=RANDOM_SEED):
    """Generate synthetic hourly telemetry for multiple astronauts."""

    rng = np.random.default_rng(seed)
    """Generate synthetic hourly telemetry for multiple astronauts."""

    records = []

    start_time = pd.Timestamp("2026-01-01 00:00:00")

    for astronaut_id in ASTRONAUT_IDS:

        # Individual baseline characteristics
        baseline_hr = rng.uniform(60, 75)
        baseline_spo2 = rng.uniform(96, 99)
        baseline_temp = rng.uniform(36.3, 37.0)

        for hour in range(DAYS * READINGS_PER_DAY):

            timestamp = start_time + pd.Timedelta(hours=hour)

            # Simulated activity
            activity_level = rng.uniform(10, 90)

            # Simulated physiological measurements
            heart_rate = (
                baseline_hr
                + (activity_level * 0.25)
                + rng.normal(0, 3)
            )

            spo2 = baseline_spo2 + rng.normal(0, 0.5)

            body_temperature = (
                baseline_temp + rng.normal(0, 0.15)
            )

            # Daily sleep estimate, repeated for hourly records
            if hour % 24 == 0:
                daily_sleep = rng.uniform(5.5, 9.0)

            # Fatigue influenced partly by sleep
            fatigue = (
                5.0
                - (daily_sleep - 7.0) * 0.7
                + rng.normal(0, 0.8)
            )

            fatigue = np.clip(fatigue, 0, 10)

            # Simulated radiation dose rate
            radiation_dose_rate = rng.uniform(0.1, 0.5)

            # Anomaly labels
            anomaly_label = 0
            anomaly_type = "normal"

            # Introduce occasional simulated unusual readings
            if rng.random() < 0.04:

                anomaly_label = 1

                anomaly_type = rng.choice([
                    "elevated_heart_rate",
                    "low_spo2",
                    "elevated_temperature",
                    "high_fatigue",
                    "elevated_radiation",
                ])

                if anomaly_type == "elevated_heart_rate":
                    heart_rate += rng.uniform(25, 40)

                elif anomaly_type == "low_spo2":
                    spo2 -= rng.uniform(3, 6)

                elif anomaly_type == "elevated_temperature":
                    body_temperature += rng.uniform(1.0, 1.5)

                elif anomaly_type == "high_fatigue":
                    fatigue = rng.uniform(8.5, 10)

                elif anomaly_type == "elevated_radiation":
                    radiation_dose_rate += rng.uniform(1.0, 2.0)

            records.append({
                "astronaut_id": astronaut_id,
                "timestamp": timestamp,
                "heart_rate_bpm": round(heart_rate, 2),
                "spo2_percent": round(spo2, 2),
                "sleep_hours_last_24h": round(daily_sleep, 2),
                "body_temperature_celsius": round(
                    body_temperature, 2
                ),
                "radiation_dose_rate_usv_per_hour": round(
                    radiation_dose_rate, 3
                ),
                "activity_level_percent": round(
                    activity_level, 2
                ),
                "fatigue_level_0_10": round(fatigue, 2),
                "anomaly_label": anomaly_label,
                "anomaly_type": anomaly_type,
                "data_source": "synthetic",
            })

    return pd.DataFrame(records)


def main():
    """Generate and save the telemetry dataset."""

    dataset = generate_telemetry()

    # Find the ml directory regardless of the working directory.
    ml_directory = Path(__file__).resolve().parents[2]

    output_directory = ml_directory / "data" / "raw"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "astronaut_telemetry.csv"

    dataset.to_csv(output_file, index=False)

    print("COSMOCare synthetic dataset generated successfully!")
    print(f"Dataset location: {output_file}")
    print(f"Total records: {len(dataset)}")
    print(f"Total astronauts: {dataset['astronaut_id'].nunique()}")
    print(f"Anomaly records: {dataset['anomaly_label'].sum()}")

    print("\nFirst five records:")
    print(dataset.head().to_string(index=False))


if __name__ == "__main__":
    main()