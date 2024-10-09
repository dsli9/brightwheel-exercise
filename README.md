# Brightwheel Data Engineer Exercise

Git repository containing code for Brightwheel's data engineer exercise.

## Environment Setup

This project uses `uv` as its environment and package management tool of choice. Information how to install `uv` can be found here: https://docs.astral.sh/uv/getting-started/installation/

This project also uses Docker to spin up a local Postgres database, and as such, it would be useful to have Docker Desktop installed: https://www.docker.com/products/docker-desktop/

## Project Initialization

To initialize this project, run `make install`. This will download the relevant Python version (if necessary), create a virtual environment, and install dependencies in the virtual environment via `uv`.
If you do not want to use `uv`, you can download the relevant Python version (>=3.12 for this project) and create a virtual environment using your tool of choice, and then install dependencies via pip (`pip install -e .`).

## Tests

This project has some basic unit tests which can be run with the following command: `make test`. This will run tests via `pytest`.

## Running the ETL Service

Before attempting to run the ETL service locally for this exercise, run `docker compose up -d` to ensure that the local Postgres
database has been spun up.

The service can be run by using the command `uv run python -m brightwheel_exercise {filepath} -v`. CLI options are as follows:
```
usage: __main__.py [-h] [-v] filepath

Load data from given file into database

positional arguments:
  filepath       Path to the file that is getting loaded into the database.

options:
  -h, --help     show this help message and exit
  -v, --verbose  Increase level of feedback output. Use -vv for even more detail. Log level defaults to 'WARNING'
```

Since the ETL service is designed to run on a single file, we can ingest all the data relevant to this exercise by doing:
```
uv run python -m brightwheel_exercise ./data/source1.csv -v
uv run python -m brightwheel_exercise ./data/source2.csv -v
uv run python -m brightwheel_exercise ./data/source3.csv -v
```

Alternatively, the `make run-exercise` command can be used to run the service for the provided data files.

## Tradeoffs and Additional Notes

One thing I noticed is that in the exercise instructions, the output schema had `license_number` as a numeric data type, but I ended up turning this into a character varying data type because
license numbers aren't actual numbers you would do math on, and I can envision a world where `license_number` has leading 0s or even letters.

Given the time constraints, I made quite a few tradeoffs:
- I have some secrets (database password, username, etc.) hardcoded here but this should definitely NOT happen in the real world. Secrets should be kept somewhere like AWS Secrets Manager and then injected at runtime.
- I essentially did the bare minumum to get all the exercise data loaded into the database. There was definitely a lot more data cleaning and transformation that could have been done in order to extract additional information (such as ages served, address info, schedule, etc.) or address things like duplicate leads. If I had more time, I would have done more data cleaning and manipulation before loading into the database.
- I mapped column names to the best of my ability, but with more time, I could have done more research. Additionally, I think in the real world, I would be asking someone with more domain expertise for help here. 
- Test coverage is lacking, and ideally, all relevant functions and processes would be tested.
- There is some basic logging but there is definitely room for better logging as well as exception handling.
- Docstrings and documentation are a bit weak, and with more time I would go back and improve them.
- Database migrations are run as part of the ETL service, but it might honestly be better to have these migrations run as part of a separate, manual process. 
- Configs are all in Python, but for a lot of the mappings and configs, it might be preferable to have them be located in some other file type, like yaml.


## Long Term Considerations

In terms of infrastructure, I would probably set it up so that every time a file gets uploaded, some sort of compute gets triggered as a result that will take this file, process it, and load it into the appropriate destination. 
- For example, assuming we're in an AWS environment, maybe files get uploaded or transferred to an s3 bucket. We can set event rules via eventbridge that will listen for "object created" events from the relevant s3 bucket and then launch a lambda or some other compute to process the file and load it into some database or data warehouse. We can also set up alerting via CloudWatch Alarms so that we get notified whenever a job fails.
- This setup allows for parallel processing, so if multiple files get uploaded at the same time, each file would get processed in separate jobs at the same time, allowing for increased efficiency.
- In some cases, it might make sense to decouple the data processing/transformation from the loading. If we go this route, intermediate results can get stored elsewhere to be picked up by a separate loading job at a later time, and it could be helpful to have some more intentional orchestration here via AWS step functions or Airflow.
- Ideally, some level of data validation would occur before loading it into the final destination to make sure we're not loading faulty data.
- The current implementation uses Polars to process data, and this should be fairly performant in a single-machine context. If the data get pretty big, we can try to scale up a single machine as much as possible, and if data really gets too big, we could try and leverage the distributed processing capabilities of Spark. This would require a different implementation, and it would also require the use of EMR or AWS Glue to run Spark jobs.
  - An alternative might be to use a more ELT approach, doing the minimum processing necessary to get the data into a data warehouse and then doing transforms within the data warehouse to get the data to a more clean and useable state.

To handle the fact that files can come from many different sources and have changing schemas, it could be useful to have robust and generalizeable configs that can also be merged with and overwriten by soruce-specific configs as needed. That way, integrating a new data source would mostly involve config changes rather than code changes, and would not require some totally new pipeline to be built. 
- For example, we could have general configs that tell the code how to map column names (e.g. "name" and "operation_name" get mapped to "company"), and this config gets used for all data sources because it works. If we encounter a data source with a new mapping that doesn't break existing mappings, we could just add it to a general list (e.g. now "name", "operation_name", and "company_name" map to "company"). If it does conflict, we can create source-specific config that only accounts for "company_name" for that specific source. Apologies in advance if this is not well-articulated.
- In general, it would be nice to standardize and set expectations upstream as often as possible, but I recognize that might not always be feasible.

The exercise instructions mention that each file load will include a refresh of existing and net new records, and I think there are few options on how to handle this.
- If we don't care about the past data, we could just delete the existing data in the database before inserting data from the same source.
- If we do care about the existing data in the database, we could add some sort of indicator that helps tag existing data as old and data coming from the new file load (refresh + net new) as new. Old data could also be moved to a separate table.
- If we are particuarly interested in the net new records, we would need some way to check records against all previously existing records.
