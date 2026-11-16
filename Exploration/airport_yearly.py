import pandas as pd
from pathlib import Path


project_dir = Path(__file__).resolve().parents[1]
file_path = project_dir / "Datasets" / "airport_yearly.csv"

airport_yearly = pd.read_csv(file_path)


def run_airport_yearly_analysis():

    print("\nINDIAN AIRPORT YEARLY ANALYSIS")
    print("=" * 45)

    # Basic dataset inspection

    print("\nDATASET DIMENSIONS")
    print("Shape:", airport_yearly.shape)

    print("\nCOLUMN NAMES")
    print(airport_yearly.columns.tolist())

    print("\nFIRST FIVE RECORDS")
    print(airport_yearly.head().to_string(index=False))

    print("\nDATA TYPES")
    print(airport_yearly.dtypes)

    print("\nMISSING VALUES")
    print(airport_yearly.isnull().sum())

    print("\nDUPLICATE ROWS")
    print(airport_yearly.duplicated().sum())

    # Check data ranges and passenger values

    print("\nYEAR RANGE")
    print(
        airport_yearly["year"].min(),
        "-",
        airport_yearly["year"].max()
    )

    print("\nPASSENGER VALIDATION")
    print(
        "Negative passengers:",
        (airport_yearly["passengers"] < 0).sum()
    )

    print(
        "Zero passengers:",
        (airport_yearly["passengers"] == 0).sum()
    )

    # Explore airport categories

    print("\nAIRPORT CATEGORY ANALYSIS")

    print("Unique categories:")
    print(airport_yearly["category"].unique())

    print("\nRecords per category:")
    print(airport_yearly["category"].value_counts())

    print("\nPASSENGERS BY CATEGORY")

    category_traffic = (
        airport_yearly.groupby("category")["passengers"]
        .sum()
        .sort_values(ascending=False)
    )

    print(category_traffic)

    # Calculate annual passenger traffic

    print("\nANNUAL PASSENGER TRAFFIC")

    yearly_traffic = (
        airport_yearly.groupby("year")["passengers"]
        .sum()
        .reset_index()
    )

    print(yearly_traffic.to_string(index=False))

    # Calculate year-on-year growth

    yearly_traffic["growth_percentage"] = (
        yearly_traffic["passengers"].pct_change() * 100
    )

    print("\nYEAR-ON-YEAR PASSENGER GROWTH")

    print(yearly_traffic.to_string(index=False))

    # Identify airports with the highest passenger traffic

    print("\nTOP 10 AIRPORTS BY TOTAL PASSENGERS")

    airport_ranking = (
        airport_yearly.groupby("airport")["passengers"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(airport_ranking)

    # Identify the busiest airport for each year

    print("\nBUSIEST AIRPORT BY YEAR")

    airport_yearly_totals = (
        airport_yearly.groupby(["year", "airport"])["passengers"]
        .sum()
        .reset_index()
    )

    busiest_airports = airport_yearly_totals.loc[
        airport_yearly_totals.groupby("year")["passengers"].idxmax()
    ].sort_values("year")

    print(busiest_airports.to_string(index=False))

    # Compare airport counts across years

    print("\nNUMBER OF AIRPORTS REPORTED PER YEAR")

    airport_counts = (
        airport_yearly.groupby("year")["airport"]
        .nunique()
    )

    print(airport_counts)


    # Investigate zero-passenger records

    print("\nZERO-PASSENGER RECORDS")

    zero_records = airport_yearly[
        airport_yearly["passengers"] == 0
    ]

    print(zero_records.to_string(index=False))

    # Compare domestic and international traffic by year

    print("\nDOMESTIC VS INTERNATIONAL TRAFFIC BY YEAR")

    category_trends = (
        airport_yearly.groupby(["year", "category"])["passengers"]
        .sum()
        .unstack(fill_value=0)
    )

    print(category_trends)

    # Identify airports with the highest passenger growth

    print("\nTOP 10 AIRPORTS BY PASSENGER GROWTH (2015–2025)")

    airport_growth = (
        airport_yearly.pivot_table(
            index="airport",
            columns="year",
            values="passengers",
            aggfunc="sum"
        )
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

    
    print("\nAIRPORT YEARLY ANALYSIS COMPLETED")


if __name__ == "__main__":
    run_airport_yearly_analysis()