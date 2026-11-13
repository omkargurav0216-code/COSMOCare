"""
Generate an independent synthetic validation dataset for COSMOCare.
The original training dataset remains unchanged.
"""

from pathlib import Path
from .generate_synthetic_data import generate_telemetry

# Different seed from the training dataset.
VALIDATION_SEED = 2026


def main():
    """Generate and save the validation dataset."""

    dataset = generate_telemetry(seed=VALIDATION_SEED)

    # Locate the ml directory.
    ml_directory = Path(__file__).resolve().parents[2]

    output_directory = ml_directory / "data" / "validation"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "astronaut_validation.csv"

    dataset.to_csv(output_file, index=False)

    print("Validation dataset generated successfully!")
    print(f"Dataset location: {output_file}")
    print(f"Total records: {len(dataset)}")
    print(f"Total astronauts: {dataset['astronaut_id'].nunique()}")
    print(f"Normal records: {(dataset['anomaly_label'] == 0).sum()}")
    print(f"Anomaly records: {(dataset['anomaly_label'] == 1).sum()}")


if __name__ == "__main__":
    main()