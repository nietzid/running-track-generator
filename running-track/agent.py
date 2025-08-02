import os
import random
import requests
from typing import Dict, List, Any
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

def get_running_tracks(location: str, distance_km: float = 5.0) -> Dict[str, Any]:
    """
    Generate random running tracks based on user location using Google Maps API.
    
    Args:
        location: The starting location (address, city, or coordinates)
        distance_km: Desired track distance in kilometers (default: 5.0)
    
    Returns:
        Dictionary containing track information with routes, waypoints, and details
    """
    
    # Get Google Maps API key from environment
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        return {
            "error": "Google Maps API key not found. Please set GOOGLE_MAPS_API_KEY environment variable.",
            "tracks": []
        }
    
    try:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json"
        geocode_params = {
            'address': location,
            'key': api_key
        }
        
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_data = geocode_response.json()
        
        if geocode_data['status'] != 'OK' or not geocode_data['results']:
            return {
                "error": f"Unable to geocode location: {location}",
                "tracks": []
            }
        
        location_coords = geocode_data['results'][0]['geometry']['location']
        lat, lng = location_coords['lat'], location_coords['lng']
        
        tracks = []
        
        for i in range(3):
            bearing = random.uniform(0, 360)
            radius_km = distance_km / (2 * 3.14159)  # Convert circumference to radius
            
            # Generate a circular-ish route
            waypoints = []
            num_waypoints = random.randint(4, 6)
            
            for j in range(num_waypoints):
                angle = (360 / num_waypoints) * j + bearing
                lat_offset = (radius_km / 111.32) * 0.5  # Approximate km to degrees
                lng_offset = (radius_km / (111.32 * abs(lat))) * 0.5
                
                new_lat = lat + lat_offset * (1 if j % 2 == 0 else -1) * (j % 3 - 1)
                new_lng = lng + lng_offset * (1 if j % 2 == 0 else -1) * ((j + 1) % 3 - 1)
                
                waypoints.append(f"{new_lat},{new_lng}")
            
            # Generate Google Maps route share link
            route_waypoints = [f"{lat},{lng}"] + waypoints + [f"{lat},{lng}"]  # Return to start
            waypoints_str = "/".join(route_waypoints)
            
            maps_url = f"https://www.google.com/maps/dir/{waypoints_str}"
            
            share_url = f"https://maps.google.com/?saddr={lat},{lng}&daddr={lat},{lng}&waypoints={';'.join(waypoints)}"
            
            track = {
                "id": i + 1,
                "name": f"Running Track {i + 1}",
                "distance_km": round(distance_km, 1),
                "starting_point": f"{lat},{lng}",
                "waypoints": waypoints,
                "estimated_time_minutes": int(distance_km * 6),  # Assuming 6 min/km pace
                "difficulty": random.choice(["Easy", "Moderate", "Challenging"]),
                "surface": random.choice(["Paved", "Mixed", "Trail", "Sidewalk"]),
                "scenery": random.choice(["Urban", "Park", "Waterfront", "Residential", "Mixed"]),
                "google_maps_url": maps_url,
                "share_url": share_url
            }
            
            tracks.append(track)
        
        return {
            "location": location,
            "coordinates": f"{lat},{lng}",
            "tracks": tracks,
            "total_options": len(tracks)
        }
        
    except Exception as e:
        return {
            "error": f"Error generating tracks: {str(e)}",
            "tracks": []
        }

running_track_agent = Agent(
    model='gemini-2.5-flash',
    name='running_track_agent',
    description='Generate random running tracks based on location using Google Maps API',
    instruction="""You are a running track generator assistant. Help users find great running routes based on their location.

Your capabilities:
- Generate multiple running track options based on any location (address, city, or coordinates)
- Provide track details including distance, estimated time, difficulty, and surface type
- Create circular routes that start and end at the same point
- Generate Google Maps shareable links for easy navigation and sharing
- Suggest different route variations for variety

When users ask for running tracks:
1. Ask for their location (if not provided)
2. Ask for preferred distance (if not specified, default to 5km)
3. Use the get_running_tracks function to generate options
4. Present the tracks clearly with all relevant details
5. Include waypoints for navigation
6. Provide Google Maps links that users can click to open routes directly

Be encouraging and provide practical running advice along with the routes. Always mention that users can click the Google Maps links to open the routes in their browser or mobile app for turn-by-turn navigation.""",
    tools=[get_running_tracks]
)

root_agent = running_track_agent
