# Running Track Generator Agent 🏃‍♂️

An intelligent ADK (Agent Development Kit) agent that generates personalized running tracks based on your location using Google Maps API integration. Get multiple route options with detailed information and shareable Google Maps links!

## ✨ Features

- 🗺️ **Location-based track generation**: Create running routes from any address, city, or coordinates
- 📏 **Customizable distances**: Generate tracks for any distance (default: 5km)
- 🏃 **Multiple route options**: Get 3 different track variations for variety
- 🎯 **Detailed track information**: Includes waypoints, estimated time, difficulty, surface type, and scenery
- 🔄 **Circular routes**: Routes that start and end at the same point
- 🔗 **Google Maps integration**: Shareable links for easy navigation and route sharing
- 📱 **Mobile-friendly**: Works on both desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Cloud account with billing enabled
- Google Maps API key

### 1. Clone and Setup

```bash
# Navigate to the running-track directory
cd running-track

# Install dependencies
pip install -r ../requirements.txt
```

### 2. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Geocoding API** (required)
   - **Maps JavaScript API** (optional, for future enhancements)
4. Create credentials → API Key
5. Copy your API key

### 3. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file and add your API key
nano .env
```

Add your API key to the `.env` file:
```env
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
GOOGLE_CLOUD_PROJECT=your-project-id
```

### 4. Set up Application Default Credentials (ADC)

```bash
# Install Google Cloud SDK if not already installed
# On macOS: brew install google-cloud-sdk

# Authenticate with Google Cloud
gcloud auth application-default login

# Set your project
gcloud config set project your-project-id
```

### 5. Run the Agent

```bash
# Start the ADK agent
adk run agent.py
```

## 💬 Usage Examples

### Basic Usage

```
User: "Generate running tracks for San Francisco"
Agent: I'll generate some running tracks for you in San Francisco...

User: "I want 10km tracks in Central Park, New York"
Agent: Creating 10km running tracks in Central Park, New York...

User: "Find 3km running routes near Golden Gate Bridge"
Agent: Generating 3km running tracks near Golden Gate Bridge...
```

### Sample Response

```json
{
  "location": "San Francisco",
  "coordinates": "37.7749,-122.4194",
  "tracks": [
    {
      "id": 1,
      "name": "Running Track 1",
      "distance_km": 5.0,
      "starting_point": "37.7749,-122.4194",
      "waypoints": [
        "37.7849,-122.4094",
        "37.7649,-122.4294",
        "37.7749,-122.4394",
        "37.7849,-122.4194"
      ],
      "estimated_time_minutes": 30,
      "difficulty": "Moderate",
      "surface": "Mixed",
      "scenery": "Urban",
      "google_maps_url": "https://www.google.com/maps/dir/37.7749,-122.4194/37.7849,-122.4094/...",
      "share_url": "https://maps.google.com/?saddr=37.7749,-122.4194&daddr=37.7749,-122.4194&waypoints=..."
    }
  ],
  "total_options": 3
}
```

## 🗺️ Google Maps Integration

### Route Links

Each generated track includes two types of Google Maps links:

1. **Directions URL** (`google_maps_url`): 
   - Opens full directions in Google Maps
   - Shows turn-by-turn navigation
   - Works on desktop and mobile

2. **Share URL** (`share_url`):
   - Mobile-optimized format
   - Easy to share via messaging apps
   - Compatible with Google Maps mobile app

### How to Use the Links

- **Desktop**: Click the link to open in your browser
- **Mobile**: Tap the link to open in Google Maps app
- **Sharing**: Copy and send the link to friends
- **Navigation**: Use for turn-by-turn directions while running

## 📊 Track Information

Each generated track includes comprehensive details:

| Field | Description | Example |
|-------|-------------|----------|
| `id` | Unique track identifier | `1` |
| `name` | Track name | `"Running Track 1"` |
| `distance_km` | Distance in kilometers | `5.0` |
| `starting_point` | GPS coordinates of start | `"37.7749,-122.4194"` |
| `waypoints` | List of route waypoints | `["37.7849,-122.4094", ...]` |
| `estimated_time_minutes` | Estimated completion time | `30` (based on 6 min/km pace) |
| `difficulty` | Route difficulty level | `"Easy"`, `"Moderate"`, `"Challenging"` |
| `surface` | Running surface type | `"Paved"`, `"Mixed"`, `"Trail"`, `"Sidewalk"` |
| `scenery` | Route scenery type | `"Urban"`, `"Park"`, `"Waterfront"`, `"Residential"`, `"Mixed"` |
| `google_maps_url` | Direct Google Maps link | Full directions URL |
| `share_url` | Shareable Google Maps link | Mobile-friendly URL |

## 🛠️ API Reference

### `get_running_tracks` Function

```python
def get_running_tracks(location: str, distance_km: float = 5.0) -> Dict[str, Any]
```

**Parameters:**
- `location` (str): Starting location (address, city, or coordinates)
- `distance_km` (float): Desired track distance in kilometers (default: 5.0)

**Returns:**
- Dictionary containing location info, coordinates, and array of track options

**Example Usage:**
```python
result = get_running_tracks("Central Park, NYC", 3.0)
print(f"Generated {len(result['tracks'])} tracks for {result['location']}")
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "Google Maps API key not found"
**Solution:**
- Ensure `GOOGLE_MAPS_API_KEY` is set in your `.env` file
- Verify the API key is valid and has proper permissions
- Check that the `.env` file is in the correct directory

#### 2. "Unable to geocode location"
**Solution:**
- Check if the location name is spelled correctly
- Try using more specific addresses (e.g., "123 Main St, City, State")
- Ensure the Geocoding API is enabled in Google Cloud Console
- Verify your API key has access to Geocoding API

#### 3. "Your default credentials were not found"
**Solution:**
```bash
# Set up Application Default Credentials
gcloud auth application-default login

# Verify setup
gcloud auth application-default print-access-token
```

#### 4. No tracks generated
**Solution:**
- Check your internet connection
- Verify the API key has sufficient quota
- Try a different, more well-known location
- Check Google Cloud Console for API usage and errors

### Testing Your Setup

#### Test API Key
```bash
curl "https://maps.googleapis.com/maps/api/geocode/json?address=New+York&key=YOUR_API_KEY"
```

#### Test ADC
```bash
python -c "from google.auth import default; print('ADC configured:', bool(default()[0]))"
```

#### Test Environment Variables
```bash
python -c "import os; print('API Key found:', bool(os.getenv('GOOGLE_MAPS_API_KEY')))"
```

## 📁 Project Structure

```
running-track/
├── agent.py              # Main ADK agent with Google Maps integration
├── .env                  # Environment variables (create from .env.example)
├── .env.example          # Template for environment variables
├── README.md             # This documentation
└── __init__.py           # Python package initialization
```

## 🚀 Advanced Usage

### Custom Distance Requests
```
User: "Generate 15km marathon training routes in Boston"
User: "I need short 2km recovery runs in my neighborhood"
User: "Create 8km tempo run tracks with hills"
```

### Location Flexibility
```
User: "Running tracks near 40.7128,-74.0060"  # GPS coordinates
User: "Generate routes in Millennium Park, Chicago"  # Specific landmark
User: "I'm at 123 Main Street, Seattle, WA"  # Full address
```

## 🔮 Future Enhancements

Potential features for future development:
- **Elevation profiles** for hill training routes
- **Weather integration** for optimal running conditions
- **Popular running spots** database integration
- **User preferences** learning and personalization
- **GPX file export** for GPS watches
- **Real-time traffic** consideration for route optimization
- **Social features** for sharing and rating routes
- **Training plan** integration

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the running track generator!

---

**Happy Running! 🏃‍♀️🏃‍♂️**

Generate your perfect running route and hit the pavement with confidence!