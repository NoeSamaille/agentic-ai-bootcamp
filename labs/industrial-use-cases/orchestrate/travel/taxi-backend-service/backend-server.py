import random

def main():
    print("=== Welcome to the Uber-like Booking System ===\n")
    
    # 1. Get user input
    current_location = input("Enter your current location (Street + Number): ")
    destination = input("Enter your destination address: ")
    
    # 2. Generate three ride options:
    #    Ensuring: Uber X < Uber Confort < Uber Black in price
    cheaper_price = random.randint(20, 40)       # Price range for cheapest
    medium_price = random.randint(cheaper_price + 1, 65)
    expensive_price = random.randint(medium_price + 1, 87)
    
    uber_x_arrival     = random.randint(1, 15)   # random arrival times in minutes
    uber_confort_arrival = random.randint(1, 15)
    uber_black_arrival   = random.randint(1, 15)
    
    ride_options = [
        {"name": "Uber X",       "price": cheaper_price,  "arrival_time": uber_x_arrival},
        {"name": "Uber Confort", "price": medium_price,   "arrival_time": uber_confort_arrival},
        {"name": "Uber Black",   "price": expensive_price,"arrival_time": uber_black_arrival}
    ]
    
    # 3. Display the ride options
    print("\nWe have the following ride options for you:\n")
    for i, option in enumerate(ride_options, start=1):
        print(f"{i}. {option['name']}")
        print(f"   Estimated Price      : €{option['price']}")
        print(f"   Arrival Time         : {option['arrival_time']} minute(s) from now")
        print("")

    # 4. Let user choose one of the 3 options
    choice = input("Which option do you choose? (Enter 1, 2, or 3): ")
    
    # Validate input
    while choice not in ["1", "2", "3"]:
        choice = input("Invalid choice. Please enter 1, 2, or 3: ")
    
    chosen_ride = ride_options[int(choice) - 1]
    
    # 5. Show confirmation
    print("\n=== Ride Confirmation ===")
    print(f"You have chosen: {chosen_ride['name']}")
    print(f"Price: €{chosen_ride['price']}")
    print(f"Driver will arrive in about {chosen_ride['arrival_time']} minute(s).")
    print(f"Pickup location: {current_location}")
    print(f"Destination: {destination}")
    print("\nThank you for using our service!\n")

if __name__ == "__main__":
    main()
