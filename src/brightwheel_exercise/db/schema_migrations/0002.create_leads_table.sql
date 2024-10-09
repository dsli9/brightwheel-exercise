--
-- file: 0002.create_leads_table.sql
--

CREATE TABLE brightwheel.leads (
    id SERIAL PRIMARY KEY,
    
    -- information about person/lead
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    phone2 TEXT,
    title TEXT,
    language TEXT,
    
    -- company/facility info
    company TEXT,
    curriculum_type TEXT,
    accepts_financial_aid TEXT,
    ages_served TEXT,
    capacity NUMERIC,
    max_age NUMERIC,
    min_age NUMERIC,
    operator TEXT,
    facility_type TEXT,
    website_address TEXT,
    schedule TEXT,

    -- address info, for company/facility
    address1 TEXT,
    address2 TEXT,
    city TEXT,
    state TEXT,
    county TEXT,
    zip TEXT,
    
    -- licensing info for company/facility
    license_status TEXT,
    license_issued DATE,
    license_number TEXT,
    license_renewed DATE,
    license_type TEXT,
    licensee_name TEXT,
    certificate_expiration_date DATE,
    provider_id TEXT,
    
    -- added columns
    data_source TEXT,
    data_source_location TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
