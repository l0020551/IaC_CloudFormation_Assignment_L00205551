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

WORK_DIR = "/opt/"#"./opt/weather-app"
XML_FILE = os.path.join(WORK_DIR, "forecast.xml")

def local_name(tag):
    return tag.rsplit("}", 1)[-1]

def init_database():
    """Establishes initial connection and ensures the schema layout exists."""
    try:
        conn = pymysql.connect(
            host=os.environ.get("DB_HOST"),#, "127.0.0.1"),
            user=os.environ.get("DB_USER"),# "root"),
            password=os.environ.get("DB_PASSWORD"),# "my_secret_password"),
            database=os.environ.get("DB_NAME"),# "my_local_db"),
            connect_timeout=10,
            autocommit=True  # DDL statements auto-commit natively
        )
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_observations (
                    forecast_time DATETIME,
                    location_lat VARCHAR(20),
                    location_lon VARCHAR(20),
                    temperature_c DECIMAL(5,2) NULL,
                    condition_id VARCHAR(50) NULL,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (forecast_time, location_lat, location_lon)
                );
            """)
        conn.close()
        logging.info("Database schema verification successful.")
    except Exception as e:
        logging.error(f"Database initialization critical failure: {e}")
        sys.exit(1)

def main():
    # 1. Guarantee table exists BEFORE entering the download loop
    init_database()
    
    while True:
        logging.info("Fetching Met Éireann forecast...")
        try:
            req = urllib.request.Request(API_URL, headers={"User-Agent": "WeatherApp/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP error: {response.status}")
                
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

            for node in location:
                name = local_name(node.tag)
                if name == "temperature":
                    temperature = node.attrib.get("value")
                elif name == "symbol":
                    condition = node.attrib.get("id")

            if temperature is None and condition is None:
                continue

            try:
                dt = datetime.fromisoformat(forecast_time.replace("Z", "+00:00"))
                if dt.tzinfo is not None:
                    dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            except ValueError:
                continue

            records.append((
                dt,
                temperature if temperature not in (None, "") else None,
                condition if condition not in (None, "") else None,
                LAT,
                LONG
            ))

        if not records:
            logging.error("No forecast records found in XML")
            sys.exit(1)

        # 3. Database Insertion
        try:
            conn = pymysql.connect(
                host=os.environ.get("DB_HOST", "127.0.0.1"),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", "my_secret_password"),
                database=os.environ.get("DB_NAME", "my_local_db"),
                connect_timeout=10,
                autocommit=False
            )
        except Exception as e:
            logging.error(f"Database connection failed during runtime execution: {e}")
            sys.exit(1)

        try:
            with conn.cursor() as cur:
                cur.executemany("""
                    INSERT INTO weather_observations
                    (forecast_time, temperature_c, condition_id, location_lat, location_lon)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    temperature_c = COALESCE(VALUES(temperature_c), weather_observations.temperature_c),
                    condition_id = COALESCE(VALUES(condition_id), weather_observations.condition_id),
                    fetched_at = CURRENT_TIMESTAMP
                """, records)

            conn.commit()
            logging.info(f"Successfully processed and merged {len(records)} forecast records.")
        except Exception as e:
            conn.rollback()
            logging.error(f"Database transaction failed: {e}")
            sys.exit(1)
        finally:
            conn.close()
            
        logging.info("Sleeping for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    main()


