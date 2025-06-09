"""
Views for the flights app - DATABASE-FREE VERSION
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import logging
from datetime import datetime, date

from .forms import FlightSearchForm
from .services import flight_service

logger = logging.getLogger(__name__)

def search_view(request):
    """Main search page view."""
    form = FlightSearchForm()
    
    context = {
        'form': form,
        'page_title': 'Ryanair Flight Search',
    }
    
    return render(request, 'flights/search.html', context)

@require_http_methods(["POST"])
def search_flights_api(request):
    """API endpoint for flight search - NO CSRF REQUIRED."""
    try:
        data = json.loads(request.body)
        
        # Parse and validate input data
        search_params = {
            'departure_airport': data.get('departure_airport', 'FNC'),
            'currency': data.get('currency', 'EUR'),
            'departure_date': datetime.strptime(data.get('departure_date'), '%Y-%m-%d').date(),
            'departure_end_date': datetime.strptime(data.get('departure_end_date'), '%Y-%m-%d').date(),
            'departure_time': data.get('departure_time', 'ANY'),
        }
        
        # Handle destinations
        destination_airport = data.get('destination_airport', 'ALL')
        if destination_airport == 'ALL':
            search_params['destinations'] = ['ALL']
        else:
            search_params['destinations'] = [destination_airport]
        
        # Validate dates
        if search_params['departure_date'] >= search_params['departure_end_date']:
            return JsonResponse({
                'success': False, 
                'error': 'End date must be after departure date.'
            })
        
        if search_params['departure_date'] < date.today():
            return JsonResponse({
                'success': False, 
                'error': 'Departure date cannot be in the past.'
            })
        
        # Search for flights
        result = flight_service.search_flights(search_params)
        
        # Add pagination info if successful
        if result['success']:
            flights = result['data']['flights']
            total_count = len(flights)
            
            # Return paginated data structure that frontend expects
            result['data']['oneway_flights'] = flights
            result['data']['total_flights'] = total_count
        
        return JsonResponse(result)
        
    except ValueError as e:
        logger.error(f"Invalid date format in search request: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'Invalid date format. Please use YYYY-MM-DD.'
        })
    except Exception as e:
        logger.error(f"Error in search_flights_api: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred while searching for flights.'
        })

@require_http_methods(["GET"])
def get_destinations_api(request, departure_airport):
    """API endpoint to get available destinations for a departure airport."""
    try:
        logger.info(f"Getting destinations for: {departure_airport}")
        result = flight_service.get_available_destinations(departure_airport)
        logger.info(f"Destinations result: success={result.get('success')}, count={result.get('count', 0)}")
        return JsonResponse(result)
        
    except Exception as e:
        logger.error(f"Error in get_destinations_api: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': 'An error occurred while fetching destinations.',
            'destinations': {}
        })