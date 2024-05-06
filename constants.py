import os
import sys

# GLOBAL CONFIGURATIONS
RANDOM_SEED = 42

# DATASET FILE PATHS
DATASET_DIRECTORY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TRANSIT_WEATHER_DATA_FILE_PATH = os.path.join(DATASET_DIRECTORY_PATH, 'Transit_Weather.csv')

# DATASET FEATURE/COLUMN NAMES
DATE = 'date'
START_TIME = 'start_time'
SESSION_ID = 'session_id'
USER_ID = 'user_id'
ROUTE = 'route'
BOARDING_STOP = 'boarding_stop'

