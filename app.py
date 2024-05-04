from flask import Flask, render_template, request
import os

app = Flask(__name__, static_url_path='/static')

API_KEY = os.environ.get('YANDEX_MAPS_API_KEY')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pickup_location = request.form["pickupLocation"]
        dropoff_location = request.form["dropoffLocation"]
        # Process pickup_location and dropoff_location
        # (e.g., save them to a database, calculate the route, etc.)
        return "Ride request received from {} to {}".format(pickup_location, dropoff_location)
    return render_template("index.html", api_key=API_KEY)

if __name__ == "__main__":
    app.run(debug=True)
