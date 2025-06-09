"""
Business logic and external API services for flights app.
"""
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional
import logging

try:
    from ryanair import Ryanair
    from ryanair.types import Flight
except ImportError:
    raise ImportError("ryanair-py is required. Install with: pip install ryanair-py")

logger = logging.getLogger(__name__)

class FlightSearchService:
    """Service class to handle flight search operations."""
    
    def filter_by_time_range(self, flights: List, time_range: str) -> List:
        """Filter flights by departure time range."""
        if time_range == "ANY":
            return flights
        
        time_ranges = {
            "EARLY_MORNING": (6, 9),
            "MORNING": (9, 12),
            "AFTERNOON": (12, 17),
            "EVENING": (17, 21),
            "NIGHT": [(21, 24), (0, 6)]  # Night spans midnight
        }
        
        if time_range not in time_ranges:
            return flights
        
        filtered_flights = []
        range_def = time_ranges[time_range]
        
        for flight in flights:
            hour = flight.departureTime.hour
            
            if time_range == "NIGHT":
                # Special handling for night time (spans midnight)
                if (hour >= 21) or (hour < 6):
                    filtered_flights.append(flight)
            else:
                start_hour, end_hour = range_def
                if start_hour <= hour < end_hour:
                    filtered_flights.append(flight)
        
        return filtered_flights
    
    def search_flights(self, search_params: Dict) -> Dict:
        """
        Search for one-way flights based on parameters.
        
        Args:
            search_params: Dictionary containing search parameters
                - departure_airport: str
                - destinations: List[str]
                - currency: str
                - departure_date: date
                - departure_end_date: date
                - departure_time: str
        
        Returns:
            Dictionary with search results and metadata
        """
        try:
            api = Ryanair(currency=search_params['currency'])
            
            departure_start = search_params['departure_date']
            departure_end = search_params['departure_end_date']
            
            logger.info(f"Searching flights from {search_params['departure_airport']} "
                       f"between {departure_start} and {departure_end}")
            
            # Search one-way flights
            flights = api.get_cheapest_flights(
                search_params['departure_airport'],
                departure_start,
                departure_end
            )
            
            # Filter out any flights after the intended end date (safety check)
            flights = [f for f in flights if f.departureTime.date() <= departure_end]
            
            # Filter by destinations if specified
            destinations = search_params.get('destinations', [])
            if destinations and 'ALL' not in destinations:
                flights = [f for f in flights if f.destination in destinations]
            
            # Filter by time range if specified
            departure_time = search_params.get('departure_time', 'ANY')
            flights = self.filter_by_time_range(flights, departure_time)
            
            # Sort by price
            flights_sorted = sorted(flights, key=lambda f: f.price)
            
            # Convert to dict format
            flight_results = []
            for flight in flights_sorted:
                flight_results.append({
                    'price': flight.price,
                    'currency': flight.currency,
                    'flight_number': flight.flightNumber,
                    'departure_time': flight.departureTime.strftime('%Y-%m-%d %H:%M'),
                    'destination': flight.destination,
                    'destination_full': flight.destinationFull
                })
            
            results = {
                'flights': flight_results,
                'total_count': len(flight_results),
                'search_info': {
                    'departure_airport': search_params['departure_airport'],
                    'departure_start': departure_start.strftime('%Y-%m-%d'),
                    'departure_end': departure_end.strftime('%Y-%m-%d'),
                    'currency': search_params['currency'],
                    'destinations': destinations,
                    'departure_time': departure_time,
                }
            }
            
            logger.info(f"Found {len(flight_results)} flights")
            return {'success': True, 'data': results}
            
        except Exception as e:
            logger.error(f"Error searching flights: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_available_destinations(self, departure_airport: str) -> Dict:
        """
        Get available destination airports for a given departure airport.
        
        Args:
            departure_airport: IATA code of departure airport
            
        Returns:
            Dictionary with available destinations
        """
        try:
            logger.info(f"Starting destination lookup for {departure_airport}")
            api = Ryanair(currency="EUR")  # Currency doesn't matter for destination lookup
            
            # Search for flights in the near future to get available destinations
            departure_date = date.today() + timedelta(days=1)
            end_date = departure_date + timedelta(days=30)  # Search 30 days ahead
            
            logger.info(f"Searching flights from {departure_airport} between {departure_date} and {end_date}")
            
            flights = api.get_cheapest_flights(departure_airport, departure_date, end_date)
            logger.info(f"Found {len(flights)} flights")
            
            # Extract unique destinations
            destinations = {}
            for flight in flights:
                destinations[flight.destination] = flight.destinationFull
            
            # Sort by airport code
            sorted_destinations = dict(sorted(destinations.items()))
            
            logger.info(f"Found {len(sorted_destinations)} unique destinations for {departure_airport}")
            
            return {
                'success': True, 
                'destinations': sorted_destinations,
                'count': len(sorted_destinations)
            }
            
        except Exception as e:
            logger.error(f"Error getting destinations for {departure_airport}: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {'success': False, 'error': str(e), 'destinations': {}}

# Global service instance
flight_service = FlightSearchService()