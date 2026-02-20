# Climate Crop Monitor - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Managing Farms](#managing-farms)
4. [Managing Crops](#managing-crops)
5. [Weather Monitoring](#weather-monitoring)
6. [Yield Predictions](#yield-predictions)
7. [Alerts and Notifications](#alerts-and-notifications)

## Getting Started

### Registration
1. Navigate to the home page
2. Click "Register"
3. Enter your username, county, and password
4. Click "Register" to create your account

### Login
1. Click "Login" on the home page
2. Enter your username and password
3. Click "Login" to access the dashboard

## Dashboard Overview

The dashboard provides a quick overview of your farming operations:

- **Total Farms**: Number of registered farms
- **Active Crops**: Number of crops currently being monitored
- **Alerts**: Number of unread alerts
- **Current Weather**: Real-time weather for your primary farm
- **Recent Alerts**: Latest notifications requiring attention
- **Active Crops Table**: List of all crops with growth stages

## Managing Farms

### Adding a New Farm
1. Click "Farms" in the navigation menu
2. Click "Add New Farm"
3. Fill in the form:
   - Farm Name (e.g., "Green Valley Farm")
   - Location/City (e.g., "Kiambu")
   - Farm Size in acres
   - Soil Type (optional)
4. Click "Create Farm"

The system will automatically fetch GPS coordinates based on the location.

### Viewing Farm Details
1. Go to "Farms" menu
2. Click "View Details" on any farm card
3. View:
   - Farm information
   - Latest weather data
   - Registered crops
   - Recent alerts

### Updating Weather Data
1. Open farm details
2. Click "Update Weather" button
3. System fetches current weather from OpenWeatherMap API
4. Data is saved and displayed

## Managing Crops

### Registering a New Crop
1. Navigate to a farm's detail page
2. Click "Add Crop"
3. Fill in the form:
   - Crop Type (Maize, Beans, Wheat, etc.)
   - Variety (optional)
   - Planting Date
   - Area Planted in acres
4. Click "Register Crop"

### Viewing Crop Details
1. Click on any crop from the dashboard or farm page
2. View:
   - Crop information
   - Days since planting
   - Current growth stage
   - Yield prediction
   - Growth progress
   - Weather history

### Growth Stages
The system automatically tracks crop growth stages:
1. **Germination**: Initial sprouting phase
2. **Vegetative**: Active growth phase
3. **Flowering**: Reproductive phase begins
4. **Fruiting**: Fruit/grain development
5. **Maturity**: Crop reaches full maturity
6. **Harvest**: Ready for harvesting

## Weather Monitoring

### Real-Time Weather Data
The system displays:
- Temperature (°C)
- Humidity (%)
- Rainfall (mm)
- Wind Speed (m/s)
- Weather Description

### Weather History
View historical weather data for each farm:
1. Go to crop details
2. Scroll to "Weather History" section
3. View table with date, temperature, humidity, and rainfall

## Yield Predictions

### How Predictions Work
The system uses:
- Historical weather data
- Crop type and growth stage
- Area planted
- Temperature, rainfall, and humidity patterns

### Viewing Predictions
1. Navigate to crop details
2. View "Yield Prediction" card showing:
   - Predicted yield in bags
   - Confidence score (%)
   - Prediction date

### Prediction Accuracy
- Higher confidence scores indicate more reliable predictions
- Accuracy improves with more weather data
- Based on optimal growing conditions for each crop type

## Alerts and Notifications

### Types of Alerts
- **Weather Alerts**: Extreme temperatures, heavy rain
- **Pest Alerts**: Conditions favorable for pests
- **Disease Alerts**: Disease risk warnings
- **Irrigation Alerts**: Water stress indicators
- **Harvest Alerts**: Optimal harvest time notifications

### Viewing Alerts
1. Click "Alerts" in the navigation menu
2. View all alerts with:
   - Severity level (Low, Medium, High, Critical)
   - Alert type
   - Message details
   - Farm location
   - Timestamp

### Managing Alerts
- Unread alerts are highlighted
- Click "Mark as Read" to acknowledge
- Dashboard shows count of unread alerts

## Best Practices

### For Accurate Predictions
1. Update weather data regularly (at least weekly)
2. Register crops immediately after planting
3. Keep farm location information accurate
4. Monitor alerts frequently

### Data Management
1. Register all your farms and plots
2. Keep crop information up to date
3. Review predictions before harvest planning
4. Check weather alerts daily during critical growth stages

### Using the System Effectively
1. **Planning**: Use predictions for harvest logistics
2. **Resource Management**: Monitor weather for irrigation decisions
3. **Risk Management**: Act on alerts to prevent crop losses
4. **Record Keeping**: System maintains complete history

## Supported Crops

Currently supported crops:
- Maize
- Beans
- Wheat
- Coffee
- Tea
- Potato
- Tomato

Each crop has specific:
- Optimal temperature ranges
- Growth stage durations
- Base yield expectations

## Tips for Farmers

1. **Check weather daily** during planting and harvest seasons
2. **Act on high-severity alerts** immediately
3. **Compare predictions** with actual yields to improve planning
4. **Keep records** of actual harvest for future reference
5. **Update location data** if you move or add new farms

## Technical Support

For assistance:
- Contact: ARON SIGEI
- Email: [contact information]
- Institution: Kisii University, Department of Computing

## Frequently Asked Questions

**Q: How often should I update weather data?**
A: At least once per week, or daily during critical periods.

**Q: Why is my yield prediction low?**
A: Check weather conditions - unfavorable temperature or rainfall affects predictions.

**Q: Can I edit crop information after registration?**
A: Currently, contact admin for modifications. Future versions will include edit functionality.

**Q: What if my location isn't found?**
A: Try using the nearest major town or city name.

**Q: How accurate are the predictions?**
A: Accuracy improves with more data. Confidence scores above 70% are generally reliable.
