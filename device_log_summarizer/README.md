# Device Log Summarizer CLI

A Python command-line tool for the TestRight Nanosystems Software Engineering Intern assessment.

## Requirements

- Python 3.9+
- Matplotlib (only needed for chart generation)

Install dependency:

```bash
python -m pip install -r requirements.txt
```

## Project structure

```text
device_log_summarizer/
├── main.py
├── chart.py
├── data/
│   └── device_telemetry.csv
├── output/
├── requirements.txt
└── PROMPT_LOG.md
```

## Run Section 1 and Section 2

From the project folder:

```bash
python main.py
```

Or provide custom paths:

```bash
python main.py --csv data/device_telemetry.csv --json output/device_summary.json
```

The program:
1. Converts valid sensor values to floats.
2. Drops `None`, non-numeric, non-finite and negative readings.
3. Clips values above 500.0 to 500.0.
4. Groups telemetry by `device_id`.
5. Calculates record count, average valid temperature and ERROR count.
6. Excludes devices whose average temperature is above 80.0.
7. Writes the remaining records to JSON and prints a terminal summary.

**CSV note:** The assessment refers to a provided `device_telemetry.csv`, but that input file was not included with the screenshots. The included CSV is sample data for testing. Replace it with the actual assessment CSV before final submission.

## Run Section 3 chart

```bash
python -m pip install matplotlib
python chart.py
```

The chart is saved to `output/average_temperature_chart.png`.

## Robustness

- Clear error if the CSV file is missing.
- Clear error if required columns are missing.
- Handles empty files and invalid temperature values.
- Handles empty output for chart generation.
- Uses UTF-8 CSV reading, including BOM-compatible `utf-8-sig`.
