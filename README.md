#  AIRFLIGHT LOGGER & EMAIL COMPLAINATOR 

A personal tool that tracks annoying loud aircraft flying over your house, logs them automatically and drafts a complaint email to the airport using Mistral AI.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


*EXAMPLE EMAIL* 


<img width="2814" height="1358" alt="Screenshot_redacted" src="https://github.com/user-attachments/assets/f1894d6e-e6db-4649-a708-0379b831cf3c" />


# What It Does

Two notebooks work together:

`API_FLIGHT_LOG.ipynb` -- Polls the FlightRadar24 API every 40 seconds. If a plane is detected within your coordinate bounds: it logs the flight data to a daily JSON file. for example: `goodrichroad_logs_2025-12-31.json`

`EMAIL_GENERATOR.ipynb` -- Reads that day's log, counts unique flights and uses the Mistral AI API to draft a professional complaint email to the airport. It then sends the complain via Gmail SMTP.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Example Log Entry

Each detected flight is saved like this in json:



```
{
  "fr24_id": "3db9297b",
  "lat": 51.47462,
  "lon": -0.09117,
  "track": 235,
  "alt": 4025,
  "gspeed": 175,
  "vspeed": -320,
  "squawk": "6026",
  "timestamp": "2025-12-31T17:57:12Z",
  "source": "ADSB",
  "hex": "4081BB",
  "callsign": "SHT17N"
}
```

On 31st December 2025, **48 unique flights** were logged over the course of the day. These were mostly British Airways (`BAW`) and Shuttle (`SHT`).

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# How to Install & Run

Requirements

- A [FlightRadar24 API token](https://fr24api.flightradar24.com/)
- A [Mistral AI API key](https://console.mistral.ai/)
- A Gmail account with App Passwords enabled

# Install dependencies


pip install fr24sdk mistralai


# Setup

1. CREATE a `.env` and fill in those:
   - `my_token` your FlightRadar24 API token
   - `bounds` your coordinate box as `"N, S, W, E"` (e.g. `"51.49, 51.45, -0.10, -0.04"`)
   - `api_key` your Mistral API key
   - `email` your email address
   - `password` your email password through SMTP



2. Run `API_FLIGHT_LOG.ipynb` to start logging. It will poll every 40 seconds and save a daily JSON file.

3. At the end of the day, run `EMAIL_GENERATOR.ipynb` to generate and send the complaint email.

## Running continuously 

The logger is currently deployed on [PythonAnywhere](https://www.pythonanywhere.com/) so it runs 24/7 without needing your machine to stay on. Upload the .py and run it as an always-on task.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# VERSION 1.B - - - - - -  Known Limitations & Roadmap 

This is V1 of the project. It definitely works but there are several improvements planned:


# Open Source Flight Data Alternative
FlightRadar24's API is annoyingly a paid service. The goal is to find a free/open source alternative — candidates include:

# Event-Driven Detection.... no polling!
Currently the script asks the API every 40 seconds for planes regardless of whether anything is happening. This is incredibly inefficient and burns API calls unnecessarily. The plan is to switch to a push and/or event-based model so the system only triggers when an aircraft actually enters the coordinate bounds.

# Having to manually trigger the email

In an ideal world one could sit back and endlessly email airports. Need to figure out how to make the code automatically send email at a specific time. 

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Project Structure

```
project
├── API FLIGHT LOG.ipynb
├── EMAIL GENERATOR.ipynb
├── flightlog_YYYY-MM-DD.json
└── README.md

```
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Disclaimer

This project is for personal documentation purposes only. The aim is to record how flight noise affects daily life and share that information with the relevant airport through legitimate channels. No illegal or spammy activity is intended.

# Honest Thoughts

This is meant to mostly be a joke, I was frustrated and planes were so loud! I built this instead of stewing and generally be annoyed at the sky.. Please don't take it too seriously. It's really just a venting mechanism.
