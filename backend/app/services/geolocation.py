import geocoder

def get_device_location():
    try:
        g = geocoder.ip('me')  # Retrieves location based on IP
        if g.ok:
            latitude, longitude = g.latlng
            return {"latitude": latitude, "longitude": longitude}
        else:
            return {"error": "Unable to fetch location"}
    except Exception as e:
        return {"error": str(e)}