# ✈️ Goodrich Road Flight Logger

A personal tool that tracks aircraft flying over your house, logs them, and automatically drafts complaint emails to the airport using AI.

---

## What It Does

Two notebooks work together:

**`API_FLIGHT_LOG.ipynb`** — Polls the FlightRadar24 API every 40 seconds. If a plane is detected within your coordinate bounds, it logs the flight data to a daily JSON file (e.g. `goodrichroad_logs_2025-12-31.json`).

**`EMAIL_GENERATOR.ipynb`** — Reads that day's log, counts unique flights, and uses the Mistral AI API to draft a professional complaint email to the airport. It then sends it via Gmail SMTP.

---

## Example Log Entry

Each detected flight is saved like this:

```json
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

On 31st December 2025, **48 unique flights** were logged over the course of the day — mostly British Airways (`BAW`), Shuttle (`SHT`), and various international carriers.

---

## How to Install & Run

### Requirements

- Python 3.x
- A [FlightRadar24 API token](https://fr24api.flightradar24.com/)
- A [Mistral AI API key](https://console.mistral.ai/)
- A Gmail account with [App Passwords](https://support.google.com/accounts/answer/185833) enabled

### Install dependencies

```bash
pip install fr24sdk mistralai
```

### Setup

1. Open `API_FLIGHT_LOG.ipynb` and fill in:
   - `my_token` — your FlightRadar24 API token
   - `bounds` — your coordinate box as `"N, S, W, E"` (e.g. `"51.49, 51.45, -0.10, -0.04"`)

2. Open `EMAIL_GENERATOR.ipynb` and fill in:
   - `api_key` — your Mistral API key
   - Your name, address, airport name, and email credentials in the relevant placeholders

3. Run `API_FLIGHT_LOG.ipynb` to start logging. It will poll every 40 seconds and save a daily JSON file.

4. At the end of the day, run `EMAIL_GENERATOR.ipynb` to generate and send the complaint email.

### Running continuously (without your laptop)

The logger is currently deployed on **[PythonAnywhere](https://www.pythonanywhere.com/)** so it runs 24/7 without needing your machine to stay on. Upload the notebook (or convert it to a `.py` script) and run it as an always-on task.

---

## Version 1 — Known Limitations & Roadmap

This is **version 1** of the project. It works, but there are several improvements planned:

### 🔐 Security: Move secrets to `.env`
Right now API keys, email credentials, and personal details are typed directly into the notebooks. The next step is to use a `.env` file with `python-dotenv` so sensitive info is never hardcoded.

```bash
pip install python-dotenv
```

```python
# .env
FR24_TOKEN=your_token_here
MISTRAL_KEY=your_key_here
EMAIL=your@email.com
EMAIL_PASSWORD=yourapppassword
```

### 💸 Open Source Flight Data Alternative
FlightRadar24's API is a paid service. The goal is to find a free/open source alternative — candidates include:
- [**OpenSky Network**](https://opensky-network.org/) — free REST API, no SDK required
- [**dump1090**](https://github.com/flightaware/dump1090) — run your own ADS-B receiver with a cheap RTL-SDR dongle (~£25) and receive flight data locally for free

### ⚡ Event-Driven Detection (instead of polling)
Currently the script asks the API "are there any planes?" every 40 seconds, regardless of whether anything is happening. This is inefficient and burns API calls unnecessarily. The plan is to switch to a **push/event-based model** — so the system only triggers when an aircraft actually enters the coordinate bounds, rather than constantly checking.

---

## Project Structure

```
📁 project/
├── API_FLIGHT_LOG.ipynb         # Polls FR24, logs flights to JSON
├── EMAIL_GENERATOR.ipynb        # Reads logs, drafts & sends email
└── goodrichroad_logs_YYYY-MM-DD.json  # Daily flight log (auto-generated)
```

---

## ⚠️ Disclaimer

This project is for personal documentation purposes only. The aim is to record how flight noise affects daily life and share that information with the relevant airport through legitimate channels. No illegal or spammy activity is intended.

## 😅 Honestly Though

This is mostly a joke. I was frustrated, planes were loud, and I needed to do something with that energy — so I built this instead of just stewing about it. Please don't take it too seriously. It's a venting mechanism that happens to involve Python.
