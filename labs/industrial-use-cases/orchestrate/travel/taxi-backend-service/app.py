import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# Hardcoded token for demo; you could dynamically generate or store securely.
ACCESS_TOKEN = "R4Nd0mT0k3n"

# We'll store the last set of rides generated, so we can confirm or cancel them.
latest_rides = []
# We'll also store the currently confirmed ride (if any).
confirmed_ride = None

class BookingRequest(BaseModel):
    current_location: str
    destination: str

class ConfirmRequest(BaseModel):
    option_index: int  # The user picks which ride option to confirm (0, 1, or 2)

@app.post("/rides")
def get_ride_options(request: BookingRequest, token: str = Header(...)):
    """
    POST /rides
    Body:
    {
        "current_location": "Street X #123",
        "destination": "Street Y #456"
    }
    Header: token = R4Nd0mT0k3n

    Returns:
    {
        "current_location": "...",
        "destination": "...",
        "ride_options": [
            {
              "name": "Uber X",
              "price": 20-40,
              "arrival_time": ...
            },
            ...
        ]
    }
    """
    # Validate token
    if token != ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token provided.")

    # Generate random ride options
    cheaper_price = random.randint(20, 40)
    medium_price = random.randint(cheaper_price + 1, 65)
    expensive_price = random.randint(medium_price + 1, 87)

    ride_options = [
        {
            "name": "Uber X",
            "price": cheaper_price,
            "arrival_time": random.randint(1, 15)
        },
        {
            "name": "Uber Confort",
            "price": medium_price,
            "arrival_time": random.randint(1, 15)
        },
        {
            "name": "Uber Black",
            "price": expensive_price,
            "arrival_time": random.randint(1, 15)
        }
    ]

    # Store them in a global list so we can confirm/cancel later
    global latest_rides
    latest_rides = ride_options

    # Reset any previous confirmed ride
    global confirmed_ride
    confirmed_ride = None

    return {
        "current_location": request.current_location,
        "destination": request.destination,
        "ride_options": ride_options
    }

@app.post("/confirm")
def confirm_ride(request: ConfirmRequest, token: str = Header(...)):
    """
    POST /confirm
    Body:
    {
        "option_index": 0  # or 1, or 2
    }
    Header: token = R4Nd0mT0k3n

    Returns:
    {
        "message": "Ride confirmed",
        "chosen_ride": { ... ride details ... }
    }
    """
    # Validate token
    if token != ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token provided.")

    global latest_rides, confirmed_ride

    if not latest_rides:
        raise HTTPException(status_code=400, detail="No rides have been requested yet.")

    if request.option_index < 0 or request.option_index >= len(latest_rides):
        raise HTTPException(status_code=400, detail="Invalid ride option index.")

    chosen_ride = latest_rides[request.option_index]
    confirmed_ride = chosen_ride  # Store the confirmed ride

    return {
        "message": "Ride confirmed",
        "chosen_ride": chosen_ride
    }

@app.post("/cancel")
def cancel_ride(token: str = Header(...)):
    """
    POST /cancel
    Header: token = R4Nd0mT0k3n
    
    Cancels the currently confirmed ride (if any).
    """
    # Validate token
    if token != ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token provided.")

    global confirmed_ride
    if confirmed_ride is None:
        raise HTTPException(status_code=400, detail="No ride has been confirmed yet.")

    ride_to_cancel = confirmed_ride
    confirmed_ride = None

    return {
        "message": f"Your ride '{ride_to_cancel['name']}' was canceled successfully."
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
