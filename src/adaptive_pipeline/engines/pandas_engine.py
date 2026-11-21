import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:

    """
    Remove invalid trips.

    A row is kept only if ALL of these hold:
      - trip duration is between 1 and 180 minutes (both ends included)
      - trip_distance > 0
      - fare_amount > 0
    Rows with missing values in these columns are dropped too, because
    comparisons with NaN/NaT are False. The input is not modified and
    all columns are returned unchanged.
    """

    trip_min = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60

    valid_duration = ((trip_min >= 1) & (trip_min <= 180))
    valid_distance = (df["trip_distance"] > 0)
    valid_fare = (df["fare_amount"] > 0)
    
    return df[valid_duration & valid_distance & valid_fare]