from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR      = PROJECT_ROOT / "data" / "raw"
DOCS_DIR     = PROJECT_ROOT / "docs"
DB_PATH      = PROJECT_ROOT / "nhs_ae.duckdb"

COLUMN_MAP = {
    "Period"                                                    : "period_raw",
    "Org Code"                                                  : "org_code",
    "Parent Org"                                                : "parent_org",
    "Org name"                                                  : "org_name",
    "A&E attendances Type 1"                                    : "type1_attendances",
    "A&E attendances Type 2"                                    : "type2_attendances",
    "A&E attendances Other A&E Department"                      : "other_attendances",
    "A&E attendances Booked Appointments Type 1"                : "booked_appts_type1",
    "A&E attendances Booked Appointments Type 2"                : "booked_appts_type2",
    "A&E attendances Booked Appointments Other Department"      : "booked_appts_other",
    "Attendances over 4hrs Type 1"                              : "over_4h_type1",
    "Attendances over 4hrs Type 2"                              : "over_4h_type2",
    "Attendances over 4hrs Other Department"                    : "over_4h_other",
    "Attendances over 4hrs Booked Appointments Type 1"          : "over_4h_booked_type1",
    "Attendances over 4hrs Booked Appointments Type 2"          : "over_4h_booked_type2",
    "Attendances over 4hrs Booked Appointments Other Department": "over_4h_booked_other",
    "Patients who have waited 4-12 hs from DTA to admission"   : "wait_4_12h_dta",
    "Patients who have waited 12+ hrs from DTA to admission"   : "wait_12plus_dta",
    "Emergency admissions via A&E - Type 1"                    : "emergency_admissions_type1",
    "Emergency admissions via A&E - Type 2"                    : "emergency_admissions_type2",
    "Emergency admissions via A&E - Other A&E department"      : "emergency_admissions_other",
    "Other emergency admissions"                                : "other_emergency_admissions",
}
