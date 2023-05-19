import pandas as pd


def prune_weather(old_data):
    new_weather_data = pd.DataFrame()

    new_weather_data['time'] = old_data['%time']
    new_weather_data['outside_temp'] = old_data['Tout']
    new_weather_data['rain'] = old_data['Rain']

    return new_weather_data

def prune_greenhouse_climate(old_data):
    new_greenhouse_data = pd.DataFrame()

    new_greenhouse_data['time'] = old_data['%time']
    new_greenhouse_data['air_temp'] = old_data['Tair']
    new_greenhouse_data['relative_hum'] = old_data['Rhair']
    new_greenhouse_data['lamp_status'] = old_data['AssimLight']

    return new_greenhouse_data

def prune_resources(old_data):
    new_resources_data = pd.DataFrame()

    new_resources_data['time'] = old_data['%Time ']
    new_resources_data['heat_cons'] = old_data['Heat_cons']
    new_resources_data['elec_cons_high'] = old_data['ElecHigh']
    new_resources_data['elec_cons_low'] = old_data['ElecLow']
    new_resources_data['irrigation_water'] = old_data['Irr']
    new_resources_data['draom_water'] = old_data['Drain']

    return new_resources_data

def prune_production(old_data):
    new_production_data = pd.DataFrame()

    new_production_data['time'] = old_data['%time']
    new_production_data['prod_qual_a'] = old_data['ProdA']
    new_production_data['prod_qual_b'] = old_data['ProdB']

    return new_production_data


if __name__ == '__main__':
    # Read all the data
    weather_data = prune_weather(pd.read_csv("../data/Weather/Weather.csv"))
    greenhouse_climate_data = prune_greenhouse_climate(pd.read_csv("../data/TheAutomators/GreenhouseClimate.csv"))
    resources_data = prune_resources(pd.read_csv("../data/TheAutomators/Resources.csv"))
    production_data = prune_production(pd.read_csv("../data/TheAutomators/Production.csv"))

    # Merge data from weather and greenhouse climate as they contain the exact same timestamps
    merged_greenhouse_weather = greenhouse_climate_data.merge(weather_data)

    # Drop NaN values
    merged_greenhouse_weather.dropna(axis=0, how='any', subset=None, inplace=True)
    resources_data.dropna(axis=0, how='any', subset=None, inplace=True)
    production_data.dropna(axis=0, how='any', subset=None, inplace=True)

    # Write data to csv files
    merged_greenhouse_weather.to_csv("../processed_data/greenhouse_weather.csv")
    resources_data.to_csv("../processed_data/resources.csv")
    production_data.to_csv("../processed_data/production.csv")
