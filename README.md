# Software Weather Satellite

A zero-cost, software-only "weather satellite": a Python script that fetches
live weather data and pushes a plain-text report to your phone, running
automatically on a schedule via GitHub Actions.

- **Data source:** [Open-Meteo](https://open-meteo.com/) — free, no API key.
- **Notifications:** [ntfy](https://ntfy.sh/) — free, no account, no API key.
- **Scheduler:** GitHub Actions — free and unlimited on public repos.

## 1. Install the ntfy app on your phone

- Android: [Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
- iOS: [App Store](https://apps.apple.com/us/app/ntfy/id1625396347)

Open the app and subscribe to a **unique, hard-to-guess topic name**,
e.g. `sumit-weather-report-8271`. Anyone who knows this exact name can
read your messages, so pick something random and don't share it.

## 2. Create a GitHub repository

1. Create a new **public** repository (public = unlimited free Actions minutes).
2. Push these files to it:
   - `weather_report.py`
   - `requirements.txt`
   - `.github/workflows/weather_report.yml`

## 3. Add your settings as repository secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**.
Add these four secrets:

| Secret name     | Example value            |
|-----------------|---------------------------|
| `LATITUDE`      | `22.5726`                 |
| `LONGITUDE`     | `88.3639`                 |
| `NTFY_TOPIC`    | `sumit-weather-report-8271` |
| `LOCATION_NAME` | `Kolkata`                 |

(Secrets, not plain variables, so the topic name doesn't sit in public logs.)

## 4. Test it manually

Go to the **Actions** tab in your repo → **Weather Satellite Report** →
**Run workflow**. Within a minute or so, you should get a push notification
on your phone with the current weather report.

## 5. Let it run automatically

The workflow is already scheduled to run **every hour** (`cron: "0 * * * *"`,
in UTC). You don't need to do anything else — GitHub runs it for you, for free,
as long as the repo stays public.

## Changing the schedule

Edit the `cron` line in `.github/workflows/weather_report.yml`. For example:

- Every 30 minutes: `*/30 * * * *`
- Every 3 hours: `0 */3 * * *`
- Twice a day (6am & 6pm UTC): `0 6,18 * * *`

## Running it locally (optional, for testing)

```bash
pip install -r requirements.txt
export LATITUDE="22.5726"
export LONGITUDE="88.3639"
export NTFY_TOPIC="sumit-weather-report-8271"
export LOCATION_NAME="Kolkata"
python weather_report.py
```
