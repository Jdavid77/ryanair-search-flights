"""
Models for the flights app - DATABASE-FREE VERSION

Since we're running without a database, we don't need any Django models.
All data comes directly from the Ryanair API and is processed in memory.
"""

# No models needed! 
# All flight data comes from the Ryanair API in real-time
# No database storage required for this stateless application

# If you need data structures, use Python classes instead of Django models:

class FlightResult:
    """Simple Python class to represent a flight result."""
    
    def __init__(self, price, currency, flight_number, departure_time, destination, destination_full):
        self.price = price
        self.currency = currency
        self.flight_number = flight_number
        self.departure_time = departure_time
        self.destination = destination
        self.destination_full = destination_full
    
    def __str__(self):
        return f"{self.flight_number}: {self.price} {self.currency} to {self.destination}"

class SearchParameters:
    """Simple Python class to represent search parameters."""
    
    def __init__(self, departure_airport, destinations, currency, departure_date, departure_end_date, departure_time):
        self.departure_airport = departure_airport
        self.destinations = destinations
        self.currency = currency
        self.departure_date = departure_date
        self.departure_end_date = departure_end_date
        self.departure_time = departure_time
    
    def __str__(self):
        return f"Search: {self.departure_airport} -> {self.destinations} ({self.departure_date} to {self.departure_end_date})"