# NHS A&E Data Pipeline

A Python and SQL pipeline for published NHS England A&E statistics, loading monthly
CSV files into DuckDB with repeatable refreshes, data quality checks, a data
dictionary and provider-level reporting.

## Reproducing this project

### 1. Clone the repository

```bash
git clone https://github.com/KJ0211/nhs-ae-pipeline.git
cd nhs-ae-pipeline
pip install duckdb pandas openpyxl requests matplotlib
```

### 2. Download the source files

Go to the NHS England A&E publication page:
**https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/ae-attendances-and-emergency-admissions-2025-26/**

Download the **CSV version** (labelled CSV, ~29KB) for each of these months:

| Month | Section to find on the page |
|---|---|
| November 2025 | November 2025 → Monthly A&E November 2025 (CSV) |
| December 2025 | December 2025 → Monthly A&E December 2025 revised (CSV) |
| January 2026 | January 2026 → Monthly A&E January 2026 revised (CSV) |
| February 2026 | February 2026 → Monthly A&E February 2026 (CSV) |
| March 2026 | March 2026 → Monthly A&E March 2026 revised (CSV) |

Save all five files into the `data/raw/` folder. The filenames will include
random suffixes added by the NHS website — this is expected and handled by the pipeline.

> Always download the **revised** version when one is available.
> Revised files contain corrections submitted after initial publication.

### 3. Run the pipeline

Open `notebooks/01_pipeline.ipynb` and run all cells in order.
Open `notebooks/02_report.ipynb` after completing the pipeline.
Open `notebooks/03_dashboard.ipynb` to view the summary dashboard.

---

## Architecture
NHS England publication page
│
▼ Manual download (5 monthly CSV files)
data/raw/ ← gitignored; download instructions above
│
▼ 01_pipeline.ipynb
raw.ae_monthly All values stored as VARCHAR — original data preserved
│
├──▶ audit.refresh_log One entry per load attempt; never deleted
├──▶ audit.quality_issues Accumulates issues found across all runs
│
▼ Quality checks (5 automated checks)
reporting.ae_monthly Cleaned and typed; rebuilt from raw on every run
│
▼ 02_report.ipynb / 03_dashboard.ipynb
docs/ae_provider_report.csv


## Dataset

Five months: November 2025 to March 2026 (987 provider-month rows after
excluding pre-calculated TOTAL rows).
Source: NHS England A&E Attendances and Emergency Admissions (2025-26 series).

## Key findings

- National Type 1 four-hour performance ranged from 57.0% to 63.9%,
  well below the 95% national standard
- January 2026 was the worst month (57.0%) with 71,517 twelve-hour
  waits from decision to admit — consistent with winter pressure
- March 2026 showed improvement (63.9%) with the fewest 12+ hour waits (46,665)
- University Hospitals Plymouth had the lowest Type 1 performance
  in March 2026 at 37.4%
- February attendances were lower than other months; this is expected
  given the shorter calendar month and is not a reduction in demand

## Data quality checks

| Check | Severity | What it catches |
|---|---|---|
| MISSING_ORG_CODE | ERROR | Rows with null or blank org_code |
| DUPLICATE_ORG_MONTH | ERROR | Duplicate (period, org_code) combinations |
| NEGATIVE_COUNTS | ERROR | Negative attendance values |
| PERFORMANCE_OUT_OF_RANGE | WARNING | four_hour_pct_type1 outside 0–100 |
| WITHIN_4H_EXCEEDS_TOTAL | ERROR | within_4h_type1 greater than type1_attendances |

All checks were verified by deliberately inserting a bad row and confirming
that four checks fired correctly.

## Reporting considerations

- **Provider reconfigurations:** Changes between months do not always reflect
  changes in patient activity; mergers and reclassifications affect continuity
- **Late submissions:** Always use revised files when available
- **TOTAL row:** Each source file contains a pre-calculated summary row
  (org_code = TOTAL) which is excluded from the reporting table;
  all totals are derived from provider-level rows
- **Type 3 / Other departments:** The definition of this category has changed
  over time; long-run comparisons should account for this

## Files

| File | Description |
|---|---|
| notebooks/01_pipeline.ipynb | Load, quality checks, transform |
| notebooks/02_report.ipynb | National summary and provider report |
| notebooks/03_dashboard.ipynb | Visual dashboard |
| docs/data_dictionary.md | Field definitions and reporting considerations |
| docs/ae_provider_report.csv | Provider-level report output |
| docs/download_log.csv | Source files and download dates |
