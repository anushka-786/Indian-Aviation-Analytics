from Exploration.carrier import run_carrier_analysis
from Exploration.airport_monthly import run_airport_monthly_analysis
from Exploration.airport_yearly import run_airport_yearly_analysis
from Exploration.international import run_international_analysis
from Exploration.domestic_routes import run_domestic_routes_analysis


def run_all_analyses():

    print("\nSTARTING INDIAN AVIATION ANALYSIS")

    run_carrier_analysis()
    run_airport_monthly_analysis()
    run_airport_yearly_analysis()
    run_international_analysis()
    run_domestic_routes_analysis()

    print("\nALL ANALYSES COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_all_analyses()