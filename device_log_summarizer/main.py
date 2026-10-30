#!/usr/bin/env python3
"""Device Log Summarizer CLI for the Software Engineering Intern assessment."""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


def clean_sensor_readings(values, upper_limit=500.0):
    """
    Convert valid values to floats.
    Drop None, unconvertible values, and negative values.
    Clip values above upper_limit.
    """
    cleaned = []
    for value in values:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue

        if not math.isfinite(number) or number < 0:
            continue

        cleaned.append(min(number, upper_limit))

    return cleaned


def load_and_aggregate(csv_path):
    """Read telemetry CSV and aggregate metrics for each device_id."""
    csv_path = Path(csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    required_columns = {"device_id", "status", "temperature"}
    grouped = defaultdict(lambda: {
        "total_records": 0,
        "temperature_sum": 0.0,
        "temperature_count": 0,
        "error_count": 0,
    })

    skipped_rows = 0
    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV is empty or has no header.")

        missing = required_columns - set(reader.fieldnames)
        if missing:
            raise ValueError(
                "CSV is missing required column(s): " + ", ".join(sorted(missing))
            )

        for row in reader:
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            raw_temperature = row.get("temperature")

            if not device_id:
                skipped_rows += 1
                continue

            # Count a valid device record even if its temperature is invalid.
            stats = grouped[device_id]
            stats["total_records"] += 1

            if status == "ERROR":
                stats["error_count"] += 1

            cleaned = clean_sensor_readings([raw_temperature])
            if cleaned:
                stats["temperature_sum"] += cleaned[0]
                stats["temperature_count"] += 1
            else:
                skipped_rows += 1

    results = []
    for device_id, stats in sorted(grouped.items()):
        average = (
            stats["temperature_sum"] / stats["temperature_count"]
            if stats["temperature_count"] else None
        )
        results.append({
            "device_id": device_id,
            "total_records": stats["total_records"],
            "average_temperature": round(average, 2) if average is not None else None,
            "error_count": stats["error_count"],
        })

    # Assessment requirement: exclude devices whose average temperature is above 80.0.
    filtered_results = [
        item for item in results
        if item["average_temperature"] is None
        or item["average_temperature"] <= 80.0
    ]

    return filtered_results, skipped_rows, len(results)


def write_json(results, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)


def print_summary(results):
    headers = ("DEVICE ID", "TOTAL RECORDS", "AVG TEMP", "ERROR COUNT")
    rows = [
        (
            item["device_id"],
            str(item["total_records"]),
            "N/A" if item["average_temperature"] is None
            else f'{item["average_temperature"]:.2f}',
            str(item["error_count"]),
        )
        for item in results
    ]

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]
    print("\n" + " | ".join(headers[i].ljust(widths[i]) for i in range(4)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(4)))


def main():
    parser = argparse.ArgumentParser(
        description="Clean sensor readings, summarize device telemetry, and export JSON."
    )
    parser.add_argument(
        "--csv", default="data/device_telemetry.csv",
        help="Input CSV path (default: data/device_telemetry.csv)"
    )
    parser.add_argument(
        "--json", default="output/device_summary.json",
        help="Output JSON path (default: output/device_summary.json)"
    )
    args = parser.parse_args()

    try:
        results, skipped_rows, device_count = load_and_aggregate(args.csv)
        write_json(results, args.json)
        print_summary(results)
        print(f"\nDevices found: {device_count}")
        print(f"Devices retained after avg-temperature filter: {len(results)}")
        print(f"Invalid/missing temperature or device rows skipped: {skipped_rows}")
        print(f"JSON saved to: {args.json}")
    except (FileNotFoundError, ValueError, OSError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
