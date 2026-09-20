from flask import Flask, request, jsonify, render_template_string
import requests
GREEN = "\033[92m"
RESET = "\033[0m"

GREEN = "\033[92m"
RESET = "\033[0m"

print(GREEN + r"""
██████╗  █████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝
██║  ██║███████║██████╔╝█████╔╝ █████╗  ██╔██╗ ██║███████║█████╔╝ █████╗
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝  ██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝
██████╔╝██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║██║  ██║██║  ██╗███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
""" + RESET)

app = Flask(__name__)

LOCATION_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Location Demo</title>
</head>
<body>

<h2>Location Permission</h2>
<p>Please allow location access to continue.</p>

<script>
function requestLocation() {
    if (!navigator.geolocation) {
        alert("Geolocation is not supported by this browser.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function(position) {

            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            fetch("/save_location", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    lat: lat,
                    lon: lon
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    window.location.href = "/front";
                }
            })
            .catch(error => {
                console.error(error);
            });

        },

        function(error) {
            if (error.code === 1) {
                alert("Location permission was denied.");
            } else if (error.code === 2) {
                alert("Location information is unavailable.");
            } else if (error.code === 3) {
                alert("Location request timed out.");
            }
        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

requestLocation();
</script>

</body>
</html>
"""

FRONT_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Location Result</title>
</head>
<body>

<h1>Location Result</h1>

<p><b>Latitude:</b> {{ lat }}</p>
<p><b>Longitude:</b> {{ lon }}</p>

<p><b>Approximate Address:</b> {{ address }}</p>

</body>
</html>
"""

saved_location = {
    "lat": None,
    "lon": None,
    "address": "Unknown"
}


@app.route("/")
def home():
    return render_template_string(LOCATION_PAGE)


@app.route("/save_location", methods=["POST"])
def save_location():

    data = request.get_json()

    lat = data.get("lat")
    lon = data.get("lon")

    if lat is None or lon is None:
        return jsonify({
            "status": "error",
            "message": "Coordinates missing"
        }), 400

    saved_location["lat"] = lat
    saved_location["lon"] = lon

    # Reverse geocoding using OpenStreetMap Nominatim
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "json"
            },
            headers={
                "User-Agent": "LocationDemo/1.0"
            },
            timeout=10
        )

        result = response.json()

        saved_location["address"] = result.get(
            "display_name",
            "Address not found"
        )

    except Exception as e:
        print("Geocoding error:", e)
        saved_location["address"] = "Could not determine address"

    print("Latitude:", lat)
    print("Longitude:", lon)
    print("Address:", saved_location["address"])

    return jsonify({
        "status": "success"
    })


@app.route("/front")
def front():

    return render_template_string(
        FRONT_PAGE,
        lat=saved_location["lat"],
        lon=saved_location["lon"],
        address=saved_location["address"]
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
