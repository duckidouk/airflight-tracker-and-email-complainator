# %%
import json
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from fr24sdk.client import Client

load_dotenv()
my_token = os.getenv("my_token")
bounds = os.getenv("bounds")  # N, S, W, E

call_unique = []
flight_log = []
seriazable = {}


def get_daily_filename():
    # Create a filename like logs/date.json
    today = datetime.now().strftime("%Y-%m-%d")
    return f"flightlog_{today}.json"


def load_daily_log():
    # Load today's log file if it exists
    global flight_log

    FILENAME = get_daily_filename()

    try:
        with open(FILENAME, "r") as f:
            flight_log = json.load(f)
    except:
        flight_log = []  # new day → fresh list


def save_daily_log():
    # Save today's updated flight log
    FILENAME = get_daily_filename()

    with open(FILENAME, "w") as f:
        json.dump(flight_log, f)


def flight_check():
    global flight_log

    load_daily_log()

    with Client(api_token=my_token) as client:
        flights = client.live.flight_positions.get_light(bounds=bounds)
        print(f"\nFlights returned: {len(flights.data)}")

        if flights.data is not None:
            for f in flights.data:
                seriazable = f.model_dump()
                print(seriazable)
                flight_log.append(seriazable)

        elif flights.data is None:
            pass

    save_daily_log()

    if flight_log[-1] is not None:
        print(
            f"\nThe latest flight was {flight_log[-1]['callsign']} and was detected in the sky at {flight_log[-1]['timestamp']}"
        )
    else:
        print("--There hasn't been any flights recorded today--")


def unique_list():
    global flight_log, call_unique

    for flights in flight_log:
        if flights["callsign"] not in call_unique:
            call_unique.append(flights["callsign"])
    print(f"\nThere has been {len(call_unique)} flights logged today")


while True:
    print(
        "---------------------------------------------------------------------------------------------------------------------------------------\n"
    )
    flight_check()
    unique_list()
    print(
        "\n\n---------------------------------------------------------------------------------------------------------------------------------------\n"
    )
    time.sleep(40)


# %%
