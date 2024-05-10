from app import db

class RideRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selected_latitude = db.Column(db.Float)
    selected_longitude = db.Column(db.Float)
    current_latitude = db.Column(db.Float)
    current_longitude = db.Column(db.Float)
    active = db.Column(db.String)

    def __init__(self, selected_latitude, selected_longitude, current_latitude, current_longitude, active = "active"):
        self.selected_latitude = selected_latitude
        self.selected_longitude = selected_longitude
        self.current_latitude = current_latitude
        self.current_longitude = current_longitude
        self.active = active

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def to_dict(self):
        return {
            'id': self.id,
            'selected_latitude': self.selected_latitude,
            'selected_longitude': self.selected_longitude,
            'current_latitude': self.current_latitude,
            'current_longitude': self.current_longitude,
            'active': self.active
        }