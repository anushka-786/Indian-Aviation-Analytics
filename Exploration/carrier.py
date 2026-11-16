import pandas as pd
from pathlib import Path

# 1. LOAD DATASET


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "Datasets" / "carrier_monthly.csv"

carrier_monthly = pd.read_csv(DATA_PATH)


def run_carrier_analysis():

    print("\n" + "=" * 60)
    print("INDIAN AVIATION - AIRLINE DATA EXPLORATION")
    print("=" * 60)



    # 2. BASIC DATASET INSPECTION
   

    print("\nDATASET DIMENSIONS")
    print("Shape:", carrier_monthly.shape)

    print("\nCOLUMN NAMES")
    print(carrier_monthly.columns.tolist())

    print("\nFIRST FIVE RECORDS")
    print(carrier_monthly.head().to_string(index=False))


    # 3. DATA QUALITY CHECK
  

    print("\nDATA TYPES")
    print(carrier_monthly.dtypes)

    print("\nMISSING VALUES")
    print(carrier_monthly.isnull().sum())

    print("\nDUPLICATE ROWS")
    print(carrier_monthly.duplicated().sum())


  
    # 4. DATE RANGE VALIDATION
   

    print("\nYEAR AND MONTH RANGES")

    print(
        "Year range:",
        carrier_monthly["year"].min(),
        "-",
        carrier_monthly["year"].max()
    )

    print(
        "Month range:",
        carrier_monthly["month"].min(),
        "-",
        carrier_monthly["month"].max()
    )


    # Latest available month

    latest = carrier_monthly.sort_values(
        ["year", "month"]
    ).iloc[-1]

    print("\nLATEST AVAILABLE DATA")
    print("Year:", latest["year"])
    print("Month:", latest["month"])


    # Number of available months per year

    print("\nAVAILABLE MONTHS PER YEAR")

    month_counts = carrier_monthly.groupby(
        "year"
    )["month"].nunique()

    print(month_counts)


    # 5. PASSENGER VALIDATION
    

    print("\nPASSENGER VALIDATION")

    print(
        "Negative passengers:",
        (carrier_monthly["passengers"] < 0).sum()
    )

    print(
        "Zero passengers:",
        (carrier_monthly["passengers"] == 0).sum()
    )


    
    # 6. AIRLINE CATEGORY ANALYSIS
    

    print("\nAIRLINE ANALYSIS")

    print("\nUnique Airlines:")
    print(carrier_monthly["airline"].unique())

    print("\nService Types:")
    print(carrier_monthly["service_type"].unique())



    # 7. LOAD FACTOR STATISTICS
    

    print("\nPASSENGER LOAD FACTOR STATISTICS")

    print(
        carrier_monthly["passenger_load_factor"].describe()
    )

    print("\nWEIGHT LOAD FACTOR STATISTICS")

    print(
        carrier_monthly["weight_load_factor"].describe()
    )

    # 8. WEIGHT LOAD FACTOR ANALYSIS

    print("\nWEIGHT LOAD FACTOR BY SERVICE TYPE")

    print(
        carrier_monthly.groupby("service_type")[
            "weight_load_factor"
        ]
        .agg(["count", "mean", "min", "max"])
        .round(2)
    )


    # Investigate values above 100

    unusual_weight_rows = carrier_monthly[
        carrier_monthly["weight_load_factor"] > 100
    ]

    print("\nWEIGHT LOAD FACTOR ABOVE 100")

    print(
        unusual_weight_rows.to_string(index=False)
    )


   
    # 9. WEIGHT LOAD FACTOR VALIDATION
  

    valid_weight_rows = carrier_monthly[
        carrier_monthly["available_tonne_km"] != 0
    ]

    carrier_monthly["calculated_weight_load_factor"] = (
        carrier_monthly["total_tonne_km"].div(
            carrier_monthly["available_tonne_km"].where(
                carrier_monthly["available_tonne_km"] != 0
            )
        ) * 100
    )

    weight_mismatches = carrier_monthly[
        (carrier_monthly["available_tonne_km"] != 0)
        &
        (
            abs(
                carrier_monthly["weight_load_factor"]
                -
                carrier_monthly["calculated_weight_load_factor"]
            ) > 0.01
        )
    ]

    print("\nWEIGHT LOAD FACTOR VALIDATION")

    print("Total records:", len(carrier_monthly))

    print(
        "Zero available tonne km:",
        (carrier_monthly["available_tonne_km"] == 0).sum()
    )

    print(
        "Calculation mismatches:",
        len(weight_mismatches)
    )

    print("\nWEIGHT LOAD FACTOR MISMATCH RECORDS")

    print(
        weight_mismatches[
            [
                "airline",
                "service_type",
                "year",
                "month",
                "total_tonne_km",
                "available_tonne_km",
                "weight_load_factor",
                "calculated_weight_load_factor"
            ]
        ].to_string(index=False)
    )



    # 10. PASSENGER LOAD FACTOR VALIDATION
   

    carrier_monthly["calculated_passenger_load_factor"] = (
        carrier_monthly["passenger_km"].div(
            carrier_monthly["seat_km"].where(
                carrier_monthly["seat_km"] != 0
            )
        ) * 100
    )

    passenger_mismatches = carrier_monthly[
        (carrier_monthly["seat_km"] != 0)
        &
        (
            abs(
                carrier_monthly["passenger_load_factor"]
                -
                carrier_monthly["calculated_passenger_load_factor"]
            ) > 0.01
        )
    ]

    print("\nPASSENGER LOAD FACTOR VALIDATION")

    print("Total records:", len(carrier_monthly))

    print(
        "Zero seat km records:",
        (carrier_monthly["seat_km"] == 0).sum()
    )

    print(
        "Calculation mismatches:",
        len(passenger_mismatches)
    )


    # Investigate values above 100

    print("\nPASSENGER LOAD FACTOR ABOVE 100")

    print(
        carrier_monthly[
            carrier_monthly["passenger_load_factor"] > 100
        ].to_string(index=False)
    )


    print("\nPASSENGER LOAD FACTOR MISMATCH RECORDS")

    print(
        passenger_mismatches[
            [
                "airline",
                "service_type",
                "year",
                "month",
                "passenger_km",
                "seat_km",
                "passenger_load_factor",
                "calculated_passenger_load_factor"
            ]
        ].to_string(index=False)
    )


   
    # 11. ZERO VALUE ANALYSIS
   

    columns_to_check = [
        "aircraft_km",
        "passengers",
        "passenger_km",
        "seat_km",
        "freight_tonnes",
        "mail_tonnes",
        "total_tonne_km",
        "available_tonne_km"
    ]

    print("\nZERO VALUE ANALYSIS")

    for column in columns_to_check:

        zero_count = (
            carrier_monthly[column] == 0
        ).sum()

        print(f"{column}: {zero_count}")



    # 12. ZERO PASSENGER RECORD ANALYSIS
  

    zero_passengers = carrier_monthly[
        carrier_monthly["passengers"] == 0
    ]

    print("\nZERO PASSENGER RECORD ANALYSIS")

    print(
        "Total zero-passenger records:",
        len(zero_passengers)
    )

    print("\nZERO PASSENGER RECORDS BY SERVICE TYPE")

    print(
        zero_passengers["service_type"].value_counts()
    )

    print("\nZERO PASSENGER RECORDS BY AIRLINE")

    print(
        zero_passengers["airline"].value_counts()
    )

    print("\nZERO PASSENGER RECORDS BY AIRLINE AND SERVICE TYPE")

    print(
        zero_passengers.groupby(
            ["airline", "service_type"]
        ).size().to_string()
    )


   
    # 13. OPERATIONAL ACTIVITY IN ZERO-PASSENGER RECORDS
   

    activity_columns = [
        "aircraft_km",
        "freight_tonnes",
        "mail_tonnes",
        "total_tonne_km",
        "seat_km"
    ]

    print("\nOPERATIONAL ACTIVITY IN ZERO-PASSENGER RECORDS")

    for column in activity_columns:

        positive_count = (
            zero_passengers[column] > 0
        ).sum()

        print(
            f"{column}: {positive_count} records with positive values"
        )


    # Activity by airline and service type

    print("\nACTIVITY BY AIRLINE AND SERVICE TYPE")

    activity_summary = zero_passengers.groupby(
        ["airline", "service_type"]
    )[activity_columns].agg(
        lambda x: (x > 0).sum()
    )

    print(activity_summary.to_string())


    print("\n" + "=" * 60)
    print("AIRLINE DATA EXPLORATION COMPLETED")
    print("=" * 60)



# 14. EXECUTION


if __name__ == "__main__":
    run_carrier_analysis()