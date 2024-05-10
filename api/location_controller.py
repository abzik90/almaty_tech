from flask import Blueprint, render_template, request, jsonify
from models.rides import RideRequest, db
from core import solve_for_coords
import os

BING_MAPS_API = os.environ.get("BING_MAPS_API_KEY")
print(BING_MAPS_API)

rides_bp = Blueprint('rides', __name__)

@rides_bp.route('/')
def index():
    return render_template("index.html", api_key=BING_MAPS_API)
@rides_bp.route('/random')
def random_coords():
    return render_template("random.html", api_key=BING_MAPS_API)
@rides_bp.route('/driver')
def driver_page():
    return render_template("driver.html", api_key=BING_MAPS_API)
@rides_bp.route('/driver-new')
def driver_new_page():
    return render_template("driver-new.html", api_key=BING_MAPS_API)

@rides_bp.route('/submit-location', methods=['POST'])
def submit_location():
    data = request.json
    selected_latitude = data.get('selected_latitude')
    selected_longitude = data.get('selected_longitude')
    current_latitude = data.get('current_latitude')
    current_longitude = data.get('current_longitude')
    
    # Create a new RideRequest object
    ride_request = RideRequest(selected_latitude, selected_longitude, current_latitude, current_longitude)
    print(ride_request.to_dict())
    try:
        # Add the new ride request to the database session
        db.session.add(ride_request)
        # Commit the session to persist the changes to the database
        db.session.commit()
        return 'Location submitted successfully!'
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        return str(e), 500
@rides_bp.route('/ride-requests', methods=['GET'])
def get_ride_requests():
    ride_requests = RideRequest.get_all()
    ride_requests_data = [
        request.to_dict()
        for request in ride_requests
    ]
    return jsonify(ride_requests_data)
@rides_bp.route('/provide-routes', methods=['GET'])
def update_and_pack_coordinates():
    # Retrieve 10 rows with status "active" from the database
    active_requests = RideRequest.query.filter_by(active='active').limit(5).all()

    # Check if there are active requests
    if not active_requests:
        return jsonify({'message': 'No active ride requests found'}), 404

    # Update the status of the retrieved rows to "expired"
    for request in active_requests:
        request.active = 'expired'
    
   

    # Pack the coordinates of the active requests into a single array
    coordinates_array = []
    for request in active_requests:
        coordinates_array.append([request.current_latitude, request.current_longitude])
        coordinates_array.append([request.selected_latitude, request.selected_longitude])
    # Return the packed coordinates as a JSON response
    print(coordinates_array)
    # Commit the changes to the database
    db.session.commit()
    return jsonify({'route': solve_for_coords(coordinates_array)})
@rides_bp.route('/unexpire', methods=['GET'])
def unexpire_upd():
    # Retrieve 10 rows with status "active" from the database
    active_requests = RideRequest.query.filter_by(active='expired').all()

    # Check if there are active requests
    if not active_requests:
        return jsonify({'message': 'No active ride requests found'}), 404

    # Update the status of the retrieved rows to "expired"
    for request in active_requests:
        request.active = 'active'
    
    # Commit the changes to the database
    db.session.commit()
    return jsonify({'success': True})