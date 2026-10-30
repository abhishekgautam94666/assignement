# PROMPT_LOG.md

## Initial AI prompt

"Write a Python script that loads the JSON output from the device telemetry aggregation task and generates a bar chart comparing the average temperature per device using matplotlib."

## Issue found during review

A first/basic chart implementation can produce crowded or overlapping device labels when there are many devices. It may also fail when the JSON list is empty or when a device has no valid average temperature.

## Follow-up prompt used to fix it

"Please make the chart robust and readable: validate that the JSON file exists and contains a list, skip records with a null average temperature, show a clear error if there is no chartable data, rotate and right-align x-axis labels, add axis titles and a chart title, add value labels to bars, use tight_layout, and save the chart to an output PNG file."

## Human review / validation

- Reviewed the JSON field names against the Section 2 output.
- Confirmed the chart reads `device_id` and `average_temperature`.
- Added readable labels and layout handling.
- Added validation for missing JSON and empty chart data.
