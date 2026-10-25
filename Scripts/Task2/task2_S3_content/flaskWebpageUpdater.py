### Disclosure, AI generated webpage updater:
from flask import Flask, jsonify
import os
import pymysql

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5
    )

@app.route("/weather/latest")
def latest_weather():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT forecast_time, fetched_at,
                       temperature_c, condition_id,
                       location_lat, location_lon
                FROM weather_observations
                WHERE location_lat = %s AND location_lon = %s
                ORDER BY forecast_time ASC
                LIMIT 1
            """, (54.9526, -7.7211))
            row = cur.fetchone()

        if row is None:
            return jsonify({"error": "No forecast data available"}), 404

        for key in ("forecast_time", "fetched_at"):
            if row[key] is not None:
                row[key] = row[key].isoformat() + "Z"

        return jsonify(row)
    finally:
        conn.close()

@app.route("/weather/forecast")
def weather_forecast():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT forecast_time, fetched_at,
                       temperature_c, condition_id
                FROM weather_observations
                WHERE location_lat = %s AND location_lon = %s
                ORDER BY forecast_time ASC
                LIMIT 100
            """, (54.9526, -7.7211))

            rows = cur.fetchall()

        for row in rows:
            for key in ("forecast_time", "fetched_at"):
                if row[key] is not None:
                    row[key] = row[key].isoformat() + "Z"

        return jsonify(rows)
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
