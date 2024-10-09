import argparse
import logging
from pathlib import Path

import polars as pl
from adbc_driver_postgresql import dbapi

from brightwheel_exercise import normalization
from brightwheel_exercise.configs import (
    COLUMN_NAME_MAPPINGS,
    COLUMNS_FOR_DB,
    NORMALIZATION_FUNC_MAPPING,
)
from brightwheel_exercise.db.utils import (
    create_database_engine,
    get_database_url,
    migrate_database,
)
from brightwheel_exercise.utils import set_up_logging

logger = logging.getLogger(__name__)


class ETLService:
    def __init__(self, data_location: str | Path):
        self.data_location = data_location
        # currently deriving data source from data location/file name, but ideally this would be derived from
        # a more consistent/stable source
        self.data_source = str(data_location).split("/")[-1].split(".")[0]

    def read_data(self) -> pl.LazyFrame:
        logger.info(
            f"Reading data. Data source: {self.data_source}. Source location: {self.data_location}"
        )
        lf = pl.scan_csv(self.data_location)
        return lf

    def normalize_data(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        logger.info(
            f"Normalizing data. Data source: {self.data_source}. Source location: {self.data_location}"
        )
        # column name normalization
        lf = normalization.change_column_names_to_lowercase(lf)
        lf = normalization.replace_spaces_in_column_names_with_underscores(lf)
        lf = normalization.map_column_names(
            lf, mapping=COLUMN_NAME_MAPPINGS[self.data_source]
        )

        # source-specific normalization
        source_normalization_func = NORMALIZATION_FUNC_MAPPING.get(self.data_source)
        if source_normalization_func:
            lf = source_normalization_func(lf)

        # add additional columns
        lf = normalization.add_data_source_column(lf, data_source=self.data_source)
        lf = normalization.add_data_source_location_column(
            lf, data_source_location=str(self.data_location)
        )

        # keep necessary columns
        lf = normalization.keep_columns_for_db_load(lf, columns_for_db=COLUMNS_FOR_DB)

        return lf
    
    def load_data_into_db(self, df: pl.DataFrame) -> None:
        logger.info(
            f"Inserting data into database. Data source: {self.data_source}. "
            f"Source location: {self.data_location}. Destination: brightwheel.leads"
        )
        with dbapi.connect(uri=get_database_url()) as conn:
            with conn.cursor() as cursor:
                # Delete existing records if they come from the same file/source currently being loaded.
                cursor.execute(
                    f"DELETE FROM brightwheel.leads WHERE data_source_location = '{self.data_location}'"
                )
                df.write_database(
                    table_name="brightwheel.leads",
                    connection=conn,
                    if_table_exists="append",
                    engine="adbc",
                )
            conn.commit()

    def run(self) -> None:
        logger.info(
            f"Starting ETL process. Data source: {self.data_source}. Source location: {self.data_location}."
        )

        lf = self.read_data()
        lf = self.normalize_data(lf)

        df = lf.collect()
        self.load_data_into_db(df)

        logger.info(
            f"ETL process complete. Data source: {self.data_source}. Source location: {self.data_location}."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load data from given file into database"
    )

    parser.add_argument(
        "filepath",
        type=Path,
        help="Path to the file that is getting loaded into the database.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help=(
            "Increase level of feedback output. Use -vv for even more detail. "
            "Log level defaults to 'WARNING'"
        ),
        action="count",
        default=0,
        dest="verbosity",
    )

    return parser.parse_args()


def main() -> None:
    # Parse command line arguments
    args = parse_args()
    set_up_logging(args.verbosity)

    # Run database migrations to make sure tables are available and up-to-date.
    db_engine = create_database_engine()
    migrate_database(db_engine)

    # Run the ETL service
    etl_service = ETLService(data_location=args.filepath)
    etl_service.run()
