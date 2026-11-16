from pathlib import Path
import pandas as pd


def run_domestic_routes_analysis():

    project_dir = Path(__file__).resolve().parents[1]
    file_path = project_dir / "Datasets" / "domestic_route_monthly.csv"

    routes = pd.read_csv(file_path)

    print("\nDOMESTIC ROUTE ANALYSIS")
    print("=" * 45)

    # Basic dataset inspection

    print("\nDATASET DIMENSIONS")
    print("Shape:", routes.shape)

    print("\nCOLUMN NAMES")
    print(routes.columns.tolist())

    print("\nFIRST FIVE RECORDS")
    print(routes.head())

    print("\nDATA TYPES")
    print(routes.dtypes)

    print("\nMISSING VALUES")
    print(routes.isnull().sum())

    print("\nDUPLICATE RECORDS")
    print(routes.duplicated().sum())

    # Date range and reporting coverage

    print("\nYEAR RANGE")
    print("Minimum year:", routes["year"].min())
    print("Maximum year:", routes["year"].max())

    print("\nMONTH RANGE")
    print("Minimum month:", routes["month"].min())
    print("Maximum month:", routes["month"].max())

    print("\nMONTHS REPORTED PER YEAR")
    print(routes.groupby("year")["month"].nunique())

    print("\nLATEST AVAILABLE DATA")
    latest_year = routes["year"].max()
    latest_month = routes.loc[
        routes["year"] == latest_year, "month"
    ].max()

    print("Latest year:", latest_year)
    print("Latest month:", latest_month)

    # Data quality checks

    print("\nNEGATIVE PASSENGER VALUES")
    print((routes["passengers"] < 0).sum())

    print("\nZERO-PASSENGER RECORDS")
    print((routes["passengers"] == 0).sum())

    print("\nINVALID MONTH VALUES")
    print((~routes["month"].between(1, 12)).sum())

    print("\nDUPLICATE ROUTE-MONTH RECORDS")

    duplicate_routes = routes.duplicated(
        subset=["year", "month", "origin", "destination"]
    ).sum()

    print(duplicate_routes)

    # Route and airport information

    print("\nUNIQUE ORIGIN AIRPORTS")
    print(routes["origin"].nunique())

    print("\nUNIQUE DESTINATION AIRPORTS")
    print(routes["destination"].nunique())

    print("\nUNIQUE DOMESTIC ROUTES")
    print(
        routes[["origin", "destination"]]
        .drop_duplicates()
        .shape[0]
    )

    # Overall passenger traffic

    print("\nTOTAL PASSENGER TRAFFIC")
    print(routes["passengers"].sum())

    print("\nAVERAGE PASSENGERS PER ROUTE RECORD")
    print(routes["passengers"].mean())

    # Annual traffic trends

    print("\nANNUAL PASSENGER TRAFFIC")

    annual_traffic = (
        routes.groupby("year")["passengers"]
        .sum()
    )

    print(annual_traffic)

    print("\nYEAR-OVER-YEAR PASSENGER GROWTH (%)")

    annual_growth = annual_traffic.pct_change() * 100

    print(annual_growth.round(2))

    # Monthly traffic trends

    print("\nMONTHLY PASSENGER TRAFFIC")

    monthly_traffic = (
        routes.groupby(["year", "month"])["passengers"]
        .sum()
    )

    print(monthly_traffic)

    print("\nAVERAGE PASSENGER TRAFFIC BY MONTH")

    average_monthly_traffic = (
        routes.groupby("month")["passengers"]
        .mean()
        .sort_values(ascending=False)
    )

    print(average_monthly_traffic.round(2))

    # Top routes by passenger traffic

    print("\nTOP 10 DOMESTIC ROUTES BY PASSENGER TRAFFIC")

    route_traffic = (
        routes.groupby(["origin", "destination"])["passengers"]
        .sum()
        .sort_values(ascending=False)
    )

    print(route_traffic.head(10))

    print("\nBOTTOM 10 DOMESTIC ROUTES BY PASSENGER TRAFFIC")

    print(route_traffic.tail(10))

    # Busiest origin and destination airports

    print("\nTOP 10 ORIGIN AIRPORTS BY PASSENGER TRAFFIC")

    origin_traffic = (
        routes.groupby("origin")["passengers"]
        .sum()
        .sort_values(ascending=False)
    )

    print(origin_traffic.head(10))

    print("\nTOP 10 DESTINATION AIRPORTS BY PASSENGER TRAFFIC")

    destination_traffic = (
        routes.groupby("destination")["passengers"]
        .sum()
        .sort_values(ascending=False)
    )

    print(destination_traffic.head(10))

    # Busiest routes in each year

    print("\nBUSIEST DOMESTIC ROUTE EACH YEAR")

    yearly_routes = (
        routes.groupby(
            ["year", "origin", "destination"]
        )["passengers"]
        .sum()
        .reset_index()
    )

    busiest_route_each_year = yearly_routes.loc[
        yearly_routes.groupby("year")["passengers"].idxmax()
    ]

    print(
        busiest_route_each_year.to_string(index=False)
    )

    # Top routes by passenger growth

    print("\nTOP 10 ROUTES BY PASSENGER GROWTH (2016–2025)")

    route_growth = routes.pivot_table(
        index=["origin", "destination"],
        columns="year",
        values="passengers",
        aggfunc="sum"
    )

    if 2016 in route_growth.columns and 2025 in route_growth.columns:

        route_growth = route_growth.dropna(
            subset=[2016, 2025]
        )

        route_growth["growth"] = (
            route_growth[2025] - route_growth[2016]
        )

        print(
            route_growth["growth"]
            .sort_values(ascending=False)
            .head(10)
        )

    else:
        print("2016 or 2025 data is unavailable.")

    # Airport reporting coverage

    print("\nAIRPORT REPORTING COVERAGE")

    origin_coverage = (
        routes.groupby("origin")
        .agg(
            records=("month", "count"),
            first_year=("year", "min"),
            last_year=("year", "max")
        )
        .sort_values("records")
    )

    print("\nORIGIN AIRPORT COVERAGE")
    print(origin_coverage.head(10))

    destination_coverage = (
        routes.groupby("destination")
        .agg(
            records=("month", "count"),
            first_year=("year", "min"),
            last_year=("year", "max")
        )
        .sort_values("records")
    )

    print("\nDESTINATION AIRPORT COVERAGE")
    print(destination_coverage.head(10))

    print("\nDOMESTIC ROUTE ANALYSIS COMPLETED")


if __name__ == "__main__":
    run_domestic_routes_analysis()