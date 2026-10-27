#!/usr/bin/env python3
import os
import pymysql
from flask import Flask, render_template_string

app = Flask(__name__)

# Database connection configuration helper
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),#, "127.0.0.1"),
        user=os.environ.get("DB_USER"),#, "root"),
        password=os.environ.get("DB_PASSWORD"),#, "my_secret_password"),
        database=os.environ.get("DB_NAME"),#, "my_local_db"),
        cursorclass=pymysql.cursors.DictCursor # Returns data as dictionaries
        ## add to bashrc to work Locally
    )

# HTML Template defined directly as a string for easy single-file local setup
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Weather Dashboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 0 20px; background-color: #f5f7fa; color: #333; }
        h1 { color: #1a202c; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #edf2f7; }
        th { background-color: #4a5568; color: white; font-weight: 600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.5px; }
        tr:hover { background-color: #f7fafc; }
        .null-value { color: #a0aec0; font-style: italic; }
        .refresh-btn { background-color: #3182ce; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 0.9rem; text-decoration: none; display: inline-block; }
        .refresh-btn:hover { background-color: #2b6cb0; }
    </style>
</head>
<body>
    <h1>Met Éireann Forecast Live Log for ATU Donegal Campus</h1>
    <p>Location ATU Donegal Campus Coordinates: <strong>{{ lat }}°, {{ lon }}°</strong></p>
    <a href="/" class="refresh-btn">🔄 Refresh Data</a>
    
    <table>
        <thead>
            <tr>
                <th>Forecast Time (UTC)</th>
                <th>Temperature (°C)</th>
                <th>Condition ID</th>
                <th>Last Synced At</th>
            </tr>
        </thead>
        <tbody>
            {% for row in observations %}
            <tr>
                <td>{{ row.forecast_time.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                <td>
                    {% if row.temperature_c is not none %}
                        <strong>{{ row.temperature_c }}°C</strong>
                    {% else %}
                        <span class="null-value">Pending...</span>
                    {% endif %}
                </td>
                <td>{{ row.condition_id or 'Unknown' }}</td>
                <td>{{ row.fetched_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="4" style="text-align: center; color: #718096;">No records found in database. Run your backend weather collector script!</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    observations = []
    lat, lon = "54.9526", "-7.7211" # Default configuration tags
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Pull the latest 50 entries sorted chronologically
            cur.execute("""
                SELECT forecast_time, temperature_c, condition_id, fetched_at, location_lat, location_lon 
                FROM weather_observations 
                ORDER BY forecast_time DESC 
                LIMIT 50;
            """)
            observations = cur.fetchall()
            if observations:
                lat = observations[0]['location_lat']
                lon = observations[0]['location_lon']
        conn.close()
    except Exception as e:
        print(f"Web Dashboard Database Error: {e}")

    return render_template_string(HTML_TEMPLATE, observations=observations, lat=lat, lon=lon)

if __name__ == '__main__':
    # Launch locally on port 5000
    app.run(host='127.0.0.1', port=80, debug=True)
