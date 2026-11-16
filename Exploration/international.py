import pandas as pd
from pathlib import Path


project_dir = Path(__file__).resolve().parents[1]
file_path = project_dir / "Datasets" / "airport_international_quarterly.csv"

international = pd.read_csv(file_path)


def run_international_analysis():

    print("\nINDIAN AIRPORT INTERNATIONAL ANALYSIS")
    print("=" * 45)

    # Basic dataset inspection

    print("\nDATASET DIMENSIONS")
    print("Shape:", international.shape)

    print("\nCOLUMN NAMES")
    print(international.columns.tolist())

    print("\nFIRST FIVE RECORDS")
    print(international.head().to_string(index=False))

    print("\nDATA TYPES")
    print(international.dtypes)

    print("\nMISSING VALUES")
    print(international.isnull().sum())

    print("\nDUPLICATE ROWS")
    print(international.duplicated().sum())

    # Check year and quarter ranges

    print("\nYEAR RANGE")
    print(
        international["year"].min(),
        "-",
        international["year"].max()
    )

    print("\nQUARTER RANGE")
    print(
        international["quarter"].min(),
        "-",
        international["quarter"].max()
    )

    print("\nAVAILABLE QUARTERS PER YEAR")
    print(international.groupby("year")["quarter"].nunique())

    # Validate passenger values

    print("\nPASSENGER VALIDATION")

    print(
        "Negative passengers:",
        (international["passengers"] < 0).sum()
    )

    print(
        "Zero passengers:",
        (international["passengers"] == 0).sum()
    )

    # Validate passenger totals

    print("\nPASSENGER CONSISTENCY CHECK")

    mismatches = international[
        international["passengers"]
        != international["departures"] + international["arrivals"]
    ]

    print("Total records:", len(international))
    print("Passenger mismatches:", len(mismatches))

    # Count airports

    print("\nAIRPORT ANALYSIS")

    print(
        "Unique airports:",
        international["airport"].nunique()
    )

    # Calculate annual international passenger traffic

    print("\nANNUAL INTERNATIONAL PASSENGER TRAFFIC")

    yearly_traffic = (
        international.groupby("year")["passengers"]
        .sum()
        .reset_index()
    )

    yearly_traffic["growth_percentage"] = (
        yearly_traffic["passengers"].pct_change() * 100
    )

    print(yearly_traffic.to_string(index=False))

    # Compare quarterly passenger traffic

    print("\nQUARTERLY PASSENGER TRAFFIC")

    quarterly_traffic = (
        international.groupby(["year", "quarter"])["passengers"]
        .sum()
        .reset_index()
    )

    print(quarterly_traffic.head(20).to_string(index=False))

    # Identify busiest and least busy quarters

    print("\nHIGHEST INTERNATIONAL TRAFFIC QUARTER")

    highest_quarter = quarterly_traffic.loc[
        quarterly_traffic["passengers"].idxmax()
    ]

    print(highest_quarter.to_string())

    print("\nLOWEST INTERNATIONAL TRAFFIC QUARTER")

    lowest_quarter = quarterly_traffic.loc[
        quarterly_traffic["passengers"].idxmin()
    ]

    print(lowest_quarter.to_string())

    # Rank airports by international passenger traffic

    print("\nTOP 10 AIRPORTS BY INTERNATIONAL PASSENGERS")

    airport_ranking = (
        international.groupby("airport")["passengers"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(airport_ranking)

    # Identify busiest airport for each year

    print("\nBUSIEST INTERNATIONAL AIRPORT BY YEAR")

    airport_yearly = (
        international.groupby(["year", "airport"])["passengers"]
        .sum()
        .reset_index()
    )

    busiest_airports = airport_yearly.loc[
        airport_yearly.groupby("year")["passengers"].idxmax()
    ].sort_values("year")

    print(busiest_airports.to_string(index=False))

    print("\nINTERNATIONAL ANALYSIS COMPLETED")


if __name__ == "__main__":
    run_international_analysis()

        # Identify zero-passenger records

    print("\nZERO-PASSENGER RECORDS")

    zero_records = international[
        international["passengers"] == 0
    ]

    print(zero_records.to_string(index=False))

    # Compare departures and arrivals

    print("\nINTERNATIONAL DEPARTURES VS ARRIVALS BY YEAR")

    movement_by_year = (
        international.groupby("year")[["departures", "arrivals"]]
        .sum()
    )

    print(movement_by_year)

    # Compare quarterly traffic across years

    print("\nAVERAGE PASSENGER TRAFFIC BY QUARTER")

    average_quarterly_traffic = (
        international.groupby("quarter")["passengers"]
        .mean()
        .sort_values(ascending=False)
    )

    print(average_quarterly_traffic)

    # Identify airports with the highest passenger growth

    print("\nTOP 10 AIRPORTS BY PASSENGER GROWTH (2015–2025)")

    airport_growth = international.pivot_table(
        index="airport",
        columns="year",
        values="passengers",
        aggfunc="sum"
    )

    airport_growth = airport_growth.dropna(
        subset=[2015, 2025]
    )

    airport_growth["growth"] = (
        airport_growth[2025] - airport_growth[2015]
    )

    print(
        airport_growth["growth"]
        .sort_values(ascending=False)
        .head(10)
    )

    # Check airport reporting coverage

    print("\nAIRPORT REPORTING COVERAGE")

    airport_coverage = (
        international.groupby("airport")
        .agg(
            records=("quarter", "count"),
            first_year=("year", "min"),
            last_year=("year", "max")
        )
        .sort_values("records")
    )

    print(airport_coverage.head(10))