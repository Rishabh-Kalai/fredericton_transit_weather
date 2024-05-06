import pandas as pd
import datetime as dt
pd.options.mode.chained_assignment = None

# Read the Constants from the Constants.py file
import constants as CONSTANTS

transit_data = pd.read_csv("data/Fredericton_Hotspot_Transit_Preprocessed.csv")
transit_data["Start_Date"] = pd.to_datetime(
    transit_data["Start_Date"], format="%Y-%m-%d"
).dt.date
# Convert the Start_Time column to datetime format and normalize it to 24-hour format, and retain just the hour of the day
transit_data["Start_Time"] = pd.to_datetime(transit_data["Start_Time"]).dt.time
# Read every value as string, as we will be converting the values to DateTime objects later
transit_schedule_data = pd.read_excel(
    "data\\resources\\Fredericton Transit Schedule\\Fredericton_Transit_Schedule.xlsx",
    sheet_name=None,
    header=0,
    index_col=None,
    dtype=str,
)
transit_data_for_routes = []
# STEP 1: Pre-Processing of the Dataframes
# For each of the values in the Start_Time column, find out where it lies in the schedule based on that
# Assign the boarding_stop(column_name) value, for each row
for route, schedule in transit_schedule_data.items():
    transit_data_for_route = transit_data[transit_data["Route"] == route].copy().reset_index(drop=True)
    # Create a new column to store the boarding_stop value
    transit_data_for_route["Boarding_Stop"] = [float("nan")]*transit_data_for_route.shape[0]
    schedule_df = pd.DataFrame(columns=["Boarding_Stop"])
    for column_name in schedule.columns:
        for element in schedule[column_name]:
            schedule_df.loc[element, "Boarding_Stop"] = column_name
    # Change index to a Column = Stop_Time
    schedule_df.reset_index(inplace=True)
    schedule_df.rename({"index": "Stop_Time"}, axis=1, inplace=True)
    # Drop any rows with missing values
    schedule_df.dropna(inplace=True)
    # Convert the Stop_Time column to datetime format and normalize it to 24-hour format
    schedule_df["Stop_Time"] = pd.to_datetime(schedule_df["Stop_Time"]).dt.time
    # Sort by the Stop_Time column
    schedule_df.sort_values("Stop_Time", inplace=True)
    schedule_df.reset_index(drop=True, inplace=True)
    # Find the closest time in the schedule for each row in the transit_data_for_route DataFrame, that is after the Start_Time
    for index, row in transit_data_for_route.iterrows():
        start_time = row["Start_Time"]
        # Assume that users board the bus 2 minutes before the scheduled departure time
        # So add 2 minutes to the Start_Time, it is already a time object
        if start_time.minute < 58:
            start_time = dt.time(start_time.hour, start_time.minute + 2)
        else:
            start_time = dt.time(start_time.hour + 1, (start_time.minute - 58))
        # Find the closest time in the schedule for each row in the transit_data_for_route DataFrame, that is after the Start_Time
        closest_time = schedule_df[schedule_df["Stop_Time"] >= start_time][
            "Stop_Time"
        ].min()
        # Find the boarding_stop value for the closest_time
        boarding_stop = schedule_df[schedule_df["Stop_Time"] == closest_time][
            "Boarding_Stop"
        ].values
        if len(boarding_stop) >= 1:
            boarding_stop = boarding_stop[0]
            # Assign the boarding_stop value to the row in the transit_data_for_route DataFrame
            transit_data_for_route.loc[index, "Boarding_Stop"] = boarding_stop
        else:
            pass
    # Append transit data for the current route to a list to be concatenated later
    transit_data_for_routes.append(transit_data_for_route)
transit_data = pd.concat(transit_data_for_routes)
transit_data.dropna(inplace=True)
transit_data.reset_index(drop=True, inplace=True)

""" WEATHER DATA PRE-PROCESSING """
weather_data = pd.read_csv("data/Daily_Weather.csv")
relevant_weather_attributes = [
    # Temperature-related Variables
    "max_temperature",  # Influences rider comfort on hot days
    "avg_temperature",  # Provides overall daily weather comfort
    "min_temperature",  # Influences rider comfort on cold days
    # Humidity-related Variables
    "max_relative_humidity",  # High humidity can affect comfort
    "avg_relative_humidity",  # Average humidity level's impact on comfort
    "min_relative_humidity",  # Low humidity can affect comfort
    # Wind-related Variables
    "max_wind_speed",  # Strong winds can impact comfort
    "avg_wind_speed",  # Average daily wind speed
    # Precipitation-related Variables
    "precipitation",  # Presence of precipitation in general
    "rain",  # Rain's impact on transit usage
    "snow",  # Snow's impact on transit usage
    # Daylight-related Variables
    "sunrise_hh",  # Morning sunlight's influence on commuter ridership
    # Visibility-related Variables
    "avg_visibility",  # Average daily visibility
]

# Normalise the Sunrise Time to 24-hour format, and retain just the hour of the day
weather_data["sunrise_hh"] = pd.to_datetime(weather_data["sunrise_hhmm"]).dt.hour
weather_data.drop("sunrise_hhmm", axis=1, inplace=True)
weather_data = weather_data[["date"] + relevant_weather_attributes]
weather_data["date"] = pd.to_datetime(weather_data["date"], infer_datetime_format=True).dt.date
# Merge the two datasets on the date column
transit_weather_data = pd.merge(
    transit_data, weather_data, left_on="Start_Date", right_on="date"
)
transit_weather_data.drop("Start_Date", axis=1, inplace=True)
# Convert the column names to lowercase
transit_weather_data.columns = transit_weather_data.columns.str.lower()

# Data Preparation: Data Wrangling & Feature Engineering
""" Date & Time Features """
# Create Separate columns for day, month and year - Date Columns
transit_weather_data["day"] = transit_weather_data["date"].apply(lambda x: x.day)
transit_weather_data["day_of_week"] = transit_weather_data["date"].apply(lambda x: x.weekday())
# Sunday=0, Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5, Saturday=6
transit_weather_data["day_of_week"] = transit_weather_data["day_of_week"].map(
    {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    }
)
# Define time labels
time_labels = ['Morning', 'Mid-Day', 'Evening']
# Create a new column for time category
transit_weather_data['part_of_day'] = pd.cut(transit_weather_data[CONSTANTS.START_TIME].dt.hour, bins=[6, 11, 17, 24], labels=time_labels)
transit_weather_data["week_of_year"] = transit_weather_data["date"].apply(lambda x: x.isocalendar()[1])
transit_weather_data["month"] = transit_weather_data["date"].apply(lambda x: x.month)
transit_weather_data["year"] = transit_weather_data["date"].apply(lambda x: x.year)
# Create a new column 'month_year' by combining 'month' and 'year' and sort the DataFrame by this column
transit_weather_data['month_year'] = transit_weather_data.apply(lambda row: row['date'].strftime('%b-%Y'), axis=1)
# Assign Season based on the month of the year: Winter (Dec-Apr), Summer (May-Aug), Fall (Sep-Nov)
transit_weather_data["Season"] = transit_weather_data["date"].apply(
    lambda x: "Winter"
    if x.month in [12, 1, 2, 3, 4]
    else ("Summer" if x.month in [5, 6, 7, 8] else "Fall")
)
# Assign popularity levels to the transit_weather_data DataFrame, as 'overall_popularity'
transit_weather_data.reset_index(drop=True, inplace=True)
transit_weather_data.drop_duplicates(inplace=True)
# Write out the pre-processed transit data to a CSV file with weather attributes
transit_weather_data.to_csv("data/Transit_Weather.csv", index=False)