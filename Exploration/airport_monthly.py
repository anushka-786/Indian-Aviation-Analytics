import pandas as pd
from pathlib import Path


# Load the airport monthly dataset

project_dir = Path(__file__).resolve().parents[1]
file_path = project_dir / "Datasets" / "airport_monthly.csv"

airport_monthly = pd.read_csv(file_path)


def run_airport_monthly_analysis():

    print("\nINDIAN AIRPORT MONTHLY ANALYSIS")
    print("=" * 45)

    # Basic dataset inspection

    print("\nDATASET DIMENSIONS")
    print("Shape:", airport_monthly.shape)

    print("\nCOLUMN NAMES")
    print(airport_monthly.columns.tolist())

    print("\nFIRST FIVE RECORDS")
    print(airport_monthly.head().to_string(index=False))

    # Check data quality

    print("\nDATA TYPES")
    print(airport_monthly.dtypes)

    print("\nMISSING VALUES")
    print(airport_monthly.isnull().sum())

    print("\nDUPLICATE ROWS")
    print(airport_monthly.duplicated().sum())

    # Check year and month coverage

    print("\nYEAR AND MONTH RANGES")

    print(
        "Year range:",
        airport_monthly["year"].min(),
        "-",
        airport_monthly["year"].max()
    )

    print(
        "Month range:",
        airport_monthly["month"].min(),
        "-",
        airport_monthly["month"].max()
    )

    print("\nAVAILABLE MONTHS PER YEAR")

    month_counts = airport_monthly.groupby(
        "year"
    )["month"].nunique()

    print(month_counts)

    # Check passenger values

    print("\nPASSENGER VALIDATION")

    print(
        "Negative passengers:",
        (airport_monthly["passengers"] < 0).sum()
    )

    print(
        "Zero passengers:",
        (airport_monthly["passengers"] == 0).sum()
    )

    # Check whether passengers equal arrivals plus departures

    print("\nPASSENGER CONSISTENCY CHECK")

    passenger_mismatches = airport_monthly[
        airport_monthly["passengers"]
        != airport_monthly["departures"] + airport_monthly["arrivals"]
    ]

    print("Total records:", len(airport_monthly))
    print("Passenger mismatches:", len(passenger_mismatches))

    if not passenger_mismatches.empty:
        print("\nMISMATCH RECORDS")
        print(passenger_mismatches.to_string(index=False))

    # Find the latest available month

    latest_record = airport_monthly.sort_values(
        ["year", "month"]
    ).iloc[-1]

    print("\nLATEST AVAILABLE DATA")
    print("Year:", latest_record["year"])
    print("Month:", latest_record["month"])

    # Count unique airports

    print("\nAIRPORT ANALYSIS")

    print(
        "Number of unique airports:",
        airport_monthly["airport"].nunique()
    )

    print("\nTOP 10 AIRPORTS BY TOTAL PASSENGERS")

    airport_ranking = (
        airport_monthly.groupby("airport")["passengers"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(airport_ranking)

    # Find airports with the lowest passenger traffic

    print("\nBOTTOM 10 AIRPORTS BY TOTAL PASSENGERS")

    lowest_airports = (
        airport_monthly.groupby("airport")["passengers"]
        .sum()
        .sort_values()
        .head(10)
    )

    print(lowest_airports)

    # Analyse monthly passenger trends

    print("\nMONTHLY PASSENGER TRENDS")

    monthly_trends = (
        airport_monthly.groupby(["year", "month"])["passengers"]
        .sum()
        .reset_index()
    )

    print("\nFIRST 10 MONTHLY TOTALS")
    print(monthly_trends.head(10).to_string(index=False))

    print("\nHIGHEST PASSENGER TRAFFIC MONTH")

    highest_month = monthly_trends.loc[
        monthly_trends["passengers"].idxmax()
    ]

    print(highest_month.to_string())

    print("\nLOWEST PASSENGER TRAFFIC MONTH")

    lowest_month = monthly_trends.loc[
        monthly_trends["passengers"].idxmin()
    ]

    print(lowest_month.to_string())

    # Investigate airport identifiers

    print("\nAIRPORT IDENTIFIER CHECK")

    unusual_airports = airport_monthly[
        ~airport_monthly["airport"].str.match(r"^[A-Z]{3}$")
    ]

    print("Unusual airport identifiers:", unusual_airports["airport"].nunique())
    print(unusual_airports["airport"].value_counts())

    # Identify zero-passenger records

    print("\nZERO-PASSENGER RECORDS")

    zero_passenger_records = airport_monthly[
        airport_monthly["passengers"] == 0
    ]

    print("Total records:", len(zero_passenger_records))
    print(
        zero_passenger_records[
            ["year", "month", "airport", "passengers"]
        ].to_string(index=False)
    )

    # Investigate April 2020

    print("\nAPRIL 2020 PASSENGER TRAFFIC")

    april_2020 = airport_monthly[
        (airport_monthly["year"] == 2020)
        & (airport_monthly["month"] == 4)
    ]

    print("Number of airport records:", len(april_2020))
    print("Total passengers:", april_2020["passengers"].sum())
    print("Total departures:", april_2020["departures"].sum())
    print("Total arrivals:", april_2020["arrivals"].sum())

    # Check reporting coverage for each airport

    print("\nAIRPORT REPORTING COVERAGE")

    airport_coverage = (
        airport_monthly.groupby("airport")
        .agg(
            records=("month", "count"),
            first_year=("year", "min"),
            last_year=("year", "max"),
            months_reported=("month", "nunique")
        )
        .sort_values("records")
    )

    print("\n10 AIRPORTS WITH FEWEST RECORDS")
    print(airport_coverage.head(10))

    
    print("\nAIRPORT MONTHLY ANALYSIS COMPLETED")


if __name__ == "__main__":
    run_airport_monthly_analysis()
