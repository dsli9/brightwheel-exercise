import polars as pl


def change_column_names_to_lowercase(lf: pl.LazyFrame) -> pl.LazyFrame:
    lf = lf.select(pl.all().name.to_lowercase())
    return lf


def replace_spaces_in_column_names_with_underscores(lf: pl.LazyFrame) -> pl.LazyFrame:
    lf = lf.select(pl.all().name.map(lambda col_name: col_name.replace(" ", "_")))
    return lf


def map_column_names(lf: pl.LazyFrame, mapping: dict) -> pl.LazyFrame:
    lf = lf.rename(mapping=mapping)
    return lf


def add_data_source_column(lf: pl.LazyFrame, data_source: str) -> pl.LazyFrame:
    lf = lf.with_columns(pl.lit(data_source).alias("data_source"))
    return lf


def add_data_source_location_column(
    lf: pl.LazyFrame, data_source_location: str
) -> pl.LazyFrame:
    lf = lf.with_columns(pl.lit(data_source_location).alias("data_source_location"))
    return lf


def convert_columns_to_date(
    lf: pl.LazyFrame, columns: list, format: str
) -> pl.LazyFrame:
    lf = lf.with_columns(pl.col(columns).str.to_date(format=format))
    return lf


def convert_columns_to_str(lf: pl.LazyFrame, columns: list) -> pl.LazyFrame:
    lf = lf.with_columns(pl.col(columns).cast(str))
    return lf


def keep_columns_for_db_load(lf: pl.LazyFrame, columns_for_db: set) -> pl.LazyFrame:
    lf = lf.select(
        [col for col in lf.collect_schema().names() if col in columns_for_db]
    )
    return lf


def normalize_source1_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    lf = convert_columns_to_date(
        lf,
        columns=["certificate_expiration_date", "license_issued"],
        format="%m/%d/%y",
    )

    return lf


def normalize_source2_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    lf = convert_columns_to_str(lf, columns=["zip"])
    return lf


def normalize_source3_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    lf = convert_columns_to_date(
        lf,
        columns=["license_issued"],
        format="%m/%d/%y",
    )
    lf = convert_columns_to_str(lf, columns=["zip"])
    return lf
