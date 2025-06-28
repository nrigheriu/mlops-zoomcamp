import pandas as pd
from batch_processing import prepare_data
from helpers import dt


def test_prepare_data():
    """
    Tests data preparation
      * Creation of the duration column
      * Filtering of data depending on the duration value
      * NA imputation to -1
      * Conversion of categorical variables to strings
    """
    
    columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]   

    expected_data = [
        ("-1", "-1", dt(1, 1), dt(1, 10), 9.0),
        ("1", "1", dt(1, 2), dt(1, 10), 8.0),
    ]

    df = pd.DataFrame(data, columns=columns)
    expected_df = pd.DataFrame(expected_data, columns=columns +  ["duration"])

    expected_df = expected_df.astype(
        {"PULocationID": "object", "DOLocationID": "object"}
    )

    df = prepare_data(df, categorical=["PULocationID", "DOLocationID"])

    pd.testing.assert_frame_equal(df, expected_df)