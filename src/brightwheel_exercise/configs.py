from brightwheel_exercise.normalization import (
    normalize_source1_data,
    normalize_source2_data,
    normalize_source3_data,
)

COLUMN_NAME_MAPPINGS = {
    "source1": {
        "name": "company",
        "credential_type": "license_type",
        "credential_number": "license_number",
        "status": "license_status",
        "expiration_date": "certificate_expiration_date",
        "address": "address1",
        "first_issue_date": "license_issued",
        "primary_contact_name": "first_name",
        "primary_contact_role": "title",
    },
    "source2": {
        "type_license": "license_type",
        "accepts_subsidy": "accepts_financial_aid",
        "primary_caregiver": "first_name",
        "total_cap": "capacity",
    },
    "source3": {
        "operation_name": "company",
        "address": "address1",
        "phone": "phone1",
        "type": "facility_type",
        "status": "license_status",
        "issue_date": "license_issued",
        "email_address": "email"
    }
}

COLUMNS_FOR_DB = {
    "first_name",
    "language",
    "last_name",
    "email",
    "phone",
    "phone2",
    "title",
    "company",
    "curriculum_type",
    "accepts_financial_aid",
    "ages_served",
    "capacity",
    "max_age",
    "min_age",
    "operator",
    "facility_type",
    "website_address",
    "schedule",
    "address1",
    "address2",
    "city",
    "state",
    "county",
    "zip",
    "license_status",
    "license_issued",
    "license_number",
    "license_renewed",
    "license_type",
    "licensee_name",
    "certificate_expiration_date",
    "provider_id",
    "data_source",
    "data_source_location",
}

NORMALIZATION_FUNC_MAPPING = {
    "source1": normalize_source1_data,
    "source2": normalize_source2_data,
    "source3": normalize_source3_data,
}
