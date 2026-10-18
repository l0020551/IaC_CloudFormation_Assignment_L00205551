
#!/usr/bin/env bash
set -u

LAT="53.3498"
LONG="-6.2603"

API_URL="http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast?lat=${LAT};long=${LONG}"

for cmd in curl xmllint date; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Missing command: $cmd"
        echo "On Ubuntu/Debian, install curl and libxml2-utils."
        exit 1
    fi
done

# Use the Linux clock, with forecast timestamps in UTC.
NOW=$(date -u -d '+1 minute' '+%Y-%m-%dT%H:00:00Z')
PLUS1=$(date -u -d '+1 hour' '+%Y-%m-%dT%H:00:00Z')
PLUS4=$(date -u -d '+4 hours' '+%Y-%m-%dT%H:00:00Z')
TOMORROW=$(date -u -d '+24 hours' '+%Y-%m-%dT%H:00:00Z')

echo "Fetching Met Éireann forecast..."
echo "Location: $LAT, $LONG"
echo "System time: $(date)"
echo "UTC time:    $(date -u)"

# Keep the curl error visible and fail on HTTP errors.
if ! curl --fail --silent --show-error --location \
    --connect-timeout 10 --max-time 30 \
    "$API_URL" -o /tmp/met-eireann.xml; then
    echo "ERROR: Forecast download failed."
    echo "Test the endpoint using curl -v to diagnose the cause."
    exit 1
fi

XML=/tmp/met-eireann.xml

if ! xmllint --noout "$XML"; then
    echo "ERROR: The response is not valid XML."
    echo "Response preview:"
    head -n 10 "$XML"
    exit 1
fi

parse_weather() {
    local target="$1"
    local label="$2"
    local temp symbol

    temp=$(xmllint --xpath \
      "string(//*[local-name()='time'][@from='$target' and @to='$target']/*[local-name()='location']/*[local-name()='temperature']/@value)" \
      "$XML" 2>/dev/null || true)

    symbol=$(xmllint --xpath \
      "string(//*[local-name()='time'][@from='$target']/*[local-name()='location']/*[local-name()='symbol']/@id)" \
      "$XML" 2>/dev/null || true)

    [ -n "$temp" ] || temp="N/A"
    [ -n "$symbol" ] || symbol="N/A"

    printf '%-20s %s | Temperature: %s C | Condition ID: %s\n' \
      "$label" "$target" "$temp" "$symbol"
}

echo
echo "Forecast checkpoints (UTC)"
echo "---------------------------------------------------------------"
parse_weather "$NOW" "Now"
parse_weather "$PLUS1" "In 1 hour"
parse_weather "$PLUS4" "In 4 hours"
parse_weather "$TOMORROW" "Tomorrow, same hour"
