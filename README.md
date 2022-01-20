# Sport Tracker

## What I want to achieve

- One place where I can see all my sport activities
- These activities are tracked by my Garmin watch (FENIX 6S)
- Data are also in Garmin Connect app
- I want to be able to see:
  - How much time do I spent doing Hiking/Walking/Cycling/Yoga/Strengths
  - The distance (for outdoor activities)
  - on daily/weekly/monthly basis
  - in the context of weekly/monthly/annual goal

## Stages

### 0. Manual

1. Data are exported from Connect app as CSV file
1. CSV file is merged with existing data in Google sheet
1. Google sheet contains 3 additional calculated columns (year, month, day) and pivot table based on these 3 columns + Activity Type, with values Distance, Time, Calories, Total Ascent

### 1. MVP

Goal: automate manual step (merging) from above. Export will be still manual. Visualization will be done in Google sheet.

### 2. Future enhancements

- Use database instead of Google sheet
- Export data from Garmin Connect without human interaction
- Add Goals and goal tracking
- Do it as a client/server architecture with API to store activities
- Create charts in Google studio
- Create dashboard in PowerBI
- Evaluate the possibility to get data directly from the watch, instead of Garmin Connect
- Web that shows the data, including charts

## High level technical requirements

### General requirements for all components

- Use  _logging_ as much as you can (instead of just print) with one global logger configured in .\config\logging.conf. This file can be stored in git
- Settings should be stored in .\config\private.configdef.json both for test and prod environment. These settings should never be committed to git - only examples.
- Use pytest for testing, flake8 for linting
- Tests should be stored in the same folder, with prefix _test__. You can run them by `python -m pytest --capture=no` from current directory

### Client (MVP)

- Reads data exported in CSV format from Garmin Connect
  - These data might overlap with data that are in the sheet already
- Checks existing data for the latest record
- Adds only new data and required columns to the google sheet (or later to the database)
  - Critical columns:
    - Activity Type
    - Date (pay attention to the format!)
    - Title
    - Distance (might be NULL)
    - Calories
    - Time
    - Total Ascent (might be NULL)
  - Optional columns
    - Avg HR
    - Max HR
    - Aerobic TE
    - Total Descent
    - Moving Time
    - Elapsed Time
    - Min Elevation
    - Max Elevation
  - Computed columns (from Date column)
    - year
    - month
    - day
- The client should accept parameters to override default configuration, if needed

### Server (TBD)

## Installation

### Client

- python (using v 3.9)
- [Google libs](https://developers.google.com/sheets/api/quickstart/python) 
  - ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
  
  ``` bash
  conda install -c conda-forge google-api-python-client
  conda install -c conda-forge google-auth-httplib2
  conda install -c conda-forge google-auth-oauthlib
  conda install -c conda-forge oauth2client
  ```y
