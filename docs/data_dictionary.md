# NHS A&E Pipeline — Data Dictionary

**Source:** NHS England A&E Attendances and Emergency Admissions  
**URL:** https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/  
**Update frequency:** Monthly (published on the 2nd Thursday of each month, covering the previous month)  
**Downloaded by:** Manual download from NHS England website  

---

## Table: reporting.ae_monthly

| Field | Type | Description | Derived from | Notes |
|---|---|---|---|---|
| period | DATE | First day of the reporting month e.g. 2026-03-01 | period_raw column in source | Source format is MSitAE-MARCH-2026; parsed in pipeline |
| org_code | VARCHAR | NHS ODS provider code e.g. RRK | Org Code | Used to identify providers consistently across months |
| parent_org | VARCHAR | NHS England regional team | Parent Org | May change if provider moves region |
| org_name | VARCHAR | Provider name as published | Org name | May change following mergers or reconfigurations |
| type1_attendances | INTEGER | Attendances at Type 1 (major) A&E departments | A&E attendances Type 1 | Excludes UTCs and walk-in centres |
| type2_attendances | INTEGER | Attendances at Type 2 (single specialty) A&E departments | A&E attendances Type 2 | |
| other_attendances | INTEGER | Attendances at other departments including UTCs | A&E attendances Other A&E Department | Definition expanded over time — see NHS guidance |
| total_attendances | INTEGER | Sum of Type 1, Type 2 and other attendances | Derived | Calculated in pipeline; not taken from source TOTAL row |
| over_4h_type1 | INTEGER | Type 1 attendances not discharged, admitted or transferred within 4 hours | Attendances over 4hrs Type 1 | |
| over_4h_type2 | INTEGER | Type 2 attendances over 4 hours | Attendances over 4hrs Type 2 | |
| over_4h_other | INTEGER | Other department attendances over 4 hours | Attendances over 4hrs Other Department | |
| total_over_4h | INTEGER | Sum of all attendances over 4 hours | Derived | Calculated in pipeline |
| within_4h_type1 | INTEGER | Type 1 attendances seen within 4 hours | Derived | type1_attendances minus over_4h_type1 |
| four_hour_pct_type1 | DOUBLE | Percentage of Type 1 attendances within 4 hours | Derived | within_4h_type1 / type1_attendances * 100; national target is 95% |
| wait_4_12h_dta | INTEGER | Patients waiting 4-12 hours from decision to admit to admission | Patients who have waited 4-12 hs from DTA to admission | DTA = Decision To Admit |
| wait_12plus_dta | INTEGER | Patients waiting 12 or more hours from decision to admit | Patients who have waited 12+ hrs from DTA to admission | Key measure of hospital flow pressure |
| emergency_admissions_type1 | INTEGER | Emergency admissions arriving via Type 1 A&E | Emergency admissions via A&E - Type 1 | |
| emergency_admissions_type2 | INTEGER | Emergency admissions arriving via Type 2 A&E | Emergency admissions via A&E - Type 2 | |
| emergency_admissions_other | INTEGER | Emergency admissions arriving via other departments | Emergency admissions via A&E - Other A&E department | |
| other_emergency_admissions | INTEGER | Emergency admissions not via A&E | Other emergency admissions | |
| source_file | VARCHAR | Filename this row was loaded from | Pipeline metadata | Use to trace back to original downloaded file |
| loaded_at | TIMESTAMP | When this row was inserted into the pipeline | Pipeline metadata | |

---

## Table: audit.refresh_log

Records every file load attempt.

| Field | Description |
|---|---|
| load_id | Unique identifier for each load run |
| source_file | Filename loaded |
| publication_month | Month covered by the file e.g. MARCH-2026 |
| started_at | When the load began |
| completed_at | When the load finished |
| rows_loaded | Rows inserted into raw.ae_monthly |
| status | success, failed or running |
| notes | Error message if status is failed |

---

## Table: audit.quality_issues

Records every quality problem detected.

| Field | Description |
|---|---|
| issue_id | Unique identifier |
| load_id | Links to refresh_log |
| check_name | Name of the check that fired |
| severity | ERROR or WARNING |
| description | Human-readable description of the problem |
| affected_rows | Number of rows affected |
| detected_at | When the check ran |

---

## Reporting considerations

NHS England notes several factors that affect interpretation of this data:

- **Provider reconfigurations:** Mergers, splits and reclassifications mean that 
  changes between months do not always reflect changes in patient activity.
- **Late submissions:** Some providers submit revised figures after initial publication. 
  Files marked revised in the filename contain corrected data.
- **February:** Shorter month means lower raw attendance counts are expected 
  and should not be interpreted as a drop in demand.
- **Type 3 / Other departments:** The definition of this category has changed 
  over time. Long-run comparisons should account for this.
- **TOTAL row:** Each source file contains a pre-calculated TOTAL summary row 
  with org_code = TOTAL. This row is excluded from the reporting table.
