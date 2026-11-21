import pandas as pd
from adaptive_pipeline.engines.pandas_engine import clean

START = pd.Timestamp("2024-01-15 12:00")

# Each row breaks AT MOST ONE rule
# (label, minutes, distance, fare, should_keep)
CASES = [
    ("valid",                10,    2.5,  12.0, True),
    ("duration below 1",     0.5,   2.5,  12.0, False),
    ("duration exactly 1",   1,     2.5,  12.0, True),   # boundary
    ("duration exactly 180", 180,   2.5,  12.0, True),   # boundary
    ("duration above 180",   181,   2.5,  12.0, False),
    ("distance zero",        10,    0.0,  12.0, False),
    ("distance negative",    10,   -3.0,  12.0, False),
    ("fare zero",            10,    2.5,   0.0, False),
    ("fare negative",        10,    2.5,  -5.0, False),
    ("dropoff missing",      None,  2.5,  12.0, False),
]

EXPECTED_KEPT = [i for i, case in enumerate(CASES) if case[4]] #[0, 2, 3]


def id_of(label):
    return [case[0] for case in CASES].index(label)


def make_trips():
    minutes = pd.Series([case[1] for case in CASES], dtype="float64")
    return pd.DataFrame({
        "trip_id": range(len(CASES)),
        "tpep_pickup_datetime": START,
        "tpep_dropoff_datetime": START + pd.to_timedelta(minutes, unit="m"),
        "trip_distance": [case[2] for case in CASES],
        "fare_amount": [case[3] for case in CASES],
    })


def test_keeps_only_valid_rows():
    result = clean(make_trips())
    assert result["trip_id"].tolist() == EXPECTED_KEPT


def test_boundaries_are_kept():
    kept = clean(make_trips())["trip_id"].tolist()
    assert id_of("duration exactly 1") in kept
    assert id_of("duration exactly 180") in kept


def test_missing_values_are_dropped():
    kept = clean(make_trips())["trip_id"].tolist()
    assert id_of("dropoff missing") not in kept


def test_input_is_not_modified():
    df = make_trips()
    before = df.copy()
    clean(df)
    assert df.equals(before)