# NHS A&E Data Pipeline

A Python and SQL pipeline for published NHS England A&E statistics, loading monthly
files into DuckDB with repeatable refreshes, data quality checks, a data dictionary
and provider-level reporting.

## What this project demonstrates
- Data ingestion from a real published government dataset
- Three-layer warehouse design: raw → reporting → audit
- Idempotent loads (rerunning the same file does not create duplicates)
- Five automated data quality checks with evidence they catch bad data
- Derived metrics calculated from components rather than trusting source totals
- Data dictionary covering field definitions, source and update frequency
- Refresh log recording every load attempt and outcome

## Architecture
NHS England Website
│
▼ Monthly CSV files
data/raw/
│
▼ load into
raw.ae_monthly (all values stored as VARCHAR — original data preserved)
│
▼ quality checks → audit.quality_issues
reporting.ae_monthly (cleaned, typed, TOTAL rows excluded)
│
▼
docs/ae_provider_report.csv


## How to run

```bash
pip install duckdb pandas openpyxl requests
```

Open `notebooks/01_pipeline.ipynb` and run all cells in order.
Open `notebooks/02_report.ipynb` after closing the pipeline connection.

## Dataset

Five months of data: November 2025 to March 2026.
Source: NHS England A&E Attendances and Emergency Admissions
https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/

## Key findings (November 2025 – March 2026)

- National Type 1 four-hour performance ranged from 57.0% to 63.9%,
  well below the 95% national standard
- January 2026 had the worst performance (57.0%) and the highest
  12+ hour waits from decision to admit (71,517) — consistent with winter pressure
- March 2026 showed improvement (63.9%) with the fewest 12+ hour waits (46,665)
- University Hospitals Plymouth had the lowest Type 1 performance
  in March 2026 at 37.4%

## Reporting considerations

NHS England notes several factors that affect interpretation:

- **Provider reconfigurations:** Mergers and reclassifications mean changes
  between months do not always reflect changes in patient activity
- **Late submissions:** Files marked revised contain corrected data submitted
  after initial publication — always use the most recent revised file
- **February:** Shorter month means lower raw attendance counts are expected
  and should not be interpreted as a reduction in demand
- **TOTAL row:** Each source file contains a pre-calculated summary row
  (org_code = TOTAL) which is excluded from the reporting table;
  all totals in this pipeline are derived from provider-level rows

## Data quality checks

Five checks run automatically after each load:

| Check | Severity | Description |
|---|---|---|
| MISSING_ORG_CODE | ERROR | Flags rows where org_code is null or blank |
| DUPLICATE_ORG_MONTH | ERROR | Flags duplicate period and org_code combinations |
| NEGATIVE_COUNTS | ERROR | Flags negative attendance values |
| PERFORMANCE_OUT_OF_RANGE | WARNING | Flags four_hour_pct_type1 outside 0–100 |
| WITHIN_4H_EXCEEDS_TOTAL | ERROR | Flags where within_4h_type1 exceeds type1_attendances |

All checks were verified against a deliberately introduced bad row.

## Files

| File | Description |
|---|---|
| notebooks/01_pipeline.ipynb | Full pipeline: load, checks, transform |
| notebooks/02_report.ipynb | National summary and provider report |
| docs/data_dictionary.md | Field definitions, sources and reporting considerations |
| docs/ae_provider_report.csv | Provider-level report output |
| docs/download_log.csv | Record of source files, URLs and download dates |
