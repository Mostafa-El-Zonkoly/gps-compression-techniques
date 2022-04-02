class Point: 
    def __init__(self, longitude, latitude, heading=0, accelration=0,timestamp=0, speed=0):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.heading = float(heading)
        self.acceleration = float(accelration)
        self.timestamp = float(timestamp)
        self.speed = float(speed)
        

