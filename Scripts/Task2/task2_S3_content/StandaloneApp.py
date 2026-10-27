#!/usr/bin/env python3

import os
import sys
import logging
import time
import urllib.request
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Configuration
LAT = "54.9526"
LONG = "-7.7211"

API_URL = (
    "http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast"
    f"?lat={LAT};long={LONG}"
)

WORK_DIR = "var/app/opt/"
XML_FILE = os.path.join(WORK_DIR, "forecast.xml")

FETCH_INTERVAL = 60

def local_name(tag):
    return tag.rsplit("}", 1)[-1]

def fetch_forecast():
    """Fetch the forecast and print readable values to the console."""

    logging.info("Fetching Met Éireann forecast...")

    try:
        request = urllib.request.Request(
            API_URL,
            headers={"User-Agent": "WeatherApp/1.0"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP error: {response.status}")

            xml_data = response.read()

        root = ET.fromstring(xml_data)

        print("\n" + "=" * 55, flush=True)
        print("       MET ÉIREANN WEATHER FORECAST", flush=True)
        print(f"Location: {LAT}, {LONG}", flush=True)
        print(f"Retrieved: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
        print("=" * 55, flush=True)

        forecast_count = 0

        for time_node in root.iter():
            if local_name(time_node.tag) != "time":
                continue

            forecast_time = time_node.attrib.get("from", "Unknown")

            location = next(
                (
                    node for node in time_node
                    if local_name(node.tag) == "location"
                ),
                None
            )

            if location is None:
                continue

            temperature = "N/A"
            condition = "N/A"

            for node in location.iter():
                name = local_name(node.tag)

                if name == "temperature":
                    temperature = node.attrib.get("value", "N/A")

                elif name == "symbol":
                    condition = node.attrib.get(
                        "name",
                        node.attrib.get("id", "N/A")
                    )

            if temperature == "N/A" and condition == "N/A":
                continue

            print(f"\nForecast time: {forecast_time}", flush=True)
            print(f"Temperature:   {temperature} °C", flush=True)
            print(f"Conditions:    {condition}", flush=True)

            forecast_count += 1

        print("\n" + "-" * 55, flush=True)
        print(f"Total forecast entries: {forecast_count}", flush=True)
        print("=" * 55 + "\n", flush=True)

        logging.info("Forecast successfully processed (%d entries).",
                     forecast_count)

    except Exception:
        logging.exception("Failed to fetch or process forecast.")


def main():
    logging.info("Weather forecast service starting.")
    logging.info("Forecast file: %s", XML_FILE)

    while True:
        fetch_forecast()

        logging.info(
            "Sleeping for %d seconds...",
            FETCH_INTERVAL
        )

        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Weather forecast service stopped.")
        sys.exit(0)
