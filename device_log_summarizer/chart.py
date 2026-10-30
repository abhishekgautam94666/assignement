#!/usr/bin/env python3
"""Create a bar chart of average temperature per device from the JSON summary."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def create_chart(json_path, output_path):
    json_path = Path(json_path)
    if not json_path.is_file():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("JSON must contain a list of device summary records.")

    usable = [
        row for row in records
        if row.get("average_temperature") is not None
    ]
    if not usable:
        raise ValueError("No valid average temperatures found to chart.")

    device_ids = [str(row["device_id"]) for row in usable]
    averages = [float(row["average_temperature"]) for row in usable]

    # Keep labels readable when there are many devices.
    figure_width = max(8, min(14, len(device_ids) * 1.1))
    fig, ax = plt.subplots(figsize=(figure_width, 5.5))
    bars = ax.bar(device_ids, averages)

    ax.set_title("Average Temperature per Device", pad=14)
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.tick_params(axis="x", labelrotation=30)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")

    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", default="output/device_summary.json")
    parser.add_argument("--output", default="output/average_temperature_chart.png")
    args = parser.parse_args()
    try:
        create_chart(args.json, args.output)
    except (FileNotFoundError, ValueError, OSError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
