### AI generated script

#!/usr/bin/env python3
import os
import sys
import logging
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import pymysql

# Setup basic logging to replicate the echo commands
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
LAT = "54.9526"
LONG = "-7.7211"
API_URL = f"http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast?lat={LAT};long={LONG}"

WORK_DIR = "./opt/weather-app"
XML_FILE = os.path.join(WORK_DIR, "forecast.xml")

def local_name(tag):
    return tag.rsplit("}", 1)[-1]

def main():
    logging.info("Fetching Met Éireann forecast...")
    
    while True:
        try:
            # Replicates curl --fail --connect-timeout 10
            req = urllib.request.Request(API_URL, headers={"User-Agent": "WeatherApp/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP error: {response.status}")
                
                # Ensure work directory exists and save file
                os.makedirs(WORK_DIR, exist_ok=True)
                with open(XML_FILE, "wb") as f:
                    f.write(response.read())
                    
        except Exception as e:
            logging.error(f"Failed to fetch forecast from API: {e}")
            sys.exit(1)

        # 2. Parse forecast XML 
        try:
            root = ET.parse(XML_FILE).getroot()
        except Exception as e:
            logging.error(f"Failed to parse XML file: {e}")
            sys.exit(1)

        records = []
        for time_node in root.iter():
            if local_name(time_node.tag) != "time":
                continue

            forecast_time = time_node.attrib.get("from")
            if not forecast_time:
                continue

            location = next(
                (node for node in time_node if local_name(node.tag) == "location"),
                None
            )
            if location is None:
                continue

            temperature = None
            condition = None

            for node in location.iter():
                name = local_name(node.tag)
                if name == "temperature":
                    temperature = node.attrib.get("value")
                elif name == "symbol":
                    condition = node.attrib.get("id")

            try:
                dt = datetime.fromisoformat(forecast_time.replace("Z", "+00:00"))
                if dt.tzinfo is not None:
                    dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            except ValueError:
                continue

            records.append((
                dt,
                temperature if temperature not in (None, "") else None,
                condition,
                LAT,
                LONG
            ))

        if not records:
            logging.error("No forecast records found in XML")
            sys.exit(1)

        # 3. Database Insertion
        try:
            conn = pymysql.connect(
                host=os.environ["DB_HOST"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                database=os.environ["DB_NAME"],
                connect_timeout=10,
                autocommit=False
            )
        except KeyError as e:
            logging.error(f"Missing required database environment variable: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            sys.exit(1)

        try:
            with conn.cursor() as cur:
                cur.executemany("""
                    INSERT INTO weather_observations
                    (forecast_time, temperature_c, condition_id,
                    location_lat, location_lon)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    temperature_c = VALUES(temperature_c),
                    condition_id = VALUES(condition_id),
                    fetched_at = CURRENT_TIMESTAMP
                """, records)

            conn.commit()
            logging.info(f"Processed {len(records)} forecast records successfully")
        except Exception as e:
            conn.rollback()
            logging.error(f"Database transaction failed: {e}")
            sys.exit(1)
        finally:
            conn.close()
        time.sleep(60) # wait a minute.
if __name__ == "__main__":
    main()