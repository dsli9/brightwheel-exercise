import polars as pl
import pytest
from brightwheel_exercise import normalization


@pytest.fixture
def test_data() -> pl.LazyFrame:
    data = {
        "TEST": [0, 2],
        "test1": [0, 2],
        "Hello There": [1, 1],
    }
    lf = pl.LazyFrame(data)
    return lf


def test_change_column_names_to_lowercase(test_data: pl.LazyFrame):
    lf = normalization.change_column_names_to_lowercase(test_data)
    assert lf.collect_schema().names() == ["test", "test1", "hello there"]


def test_replace_spaces_in_column_names_with_underscores(test_data: pl.LazyFrame):
    lf = normalization.replace_spaces_in_column_names_with_underscores(test_data)
    assert lf.collect_schema().names() == ["TEST", "test1", "Hello_There"]
