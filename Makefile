.PHONY: initialize
initialize:
	@echo "Initializing project via uv"
	@uv sync

.PHONY: run-exercise
run_exercise:
	@echo "Running ETL service for exercise"
	@uv run python -m brightwheel_exercise ./data/source1.csv -v
	@uv run python -m brightwheel_exercise ./data/source2.csv -v
	@uv run python -m brightwheel_exercise ./data/source3.csv -v

.PHONY: test
test:
	@echo "Running tests via pytest"
	@uv run pytest -vv
