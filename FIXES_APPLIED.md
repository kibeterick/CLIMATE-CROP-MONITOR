# Database Migration Fixes - Climate Crop Monitor

## Problem Identified

The system was experiencing "OperationalError: no such table: monitor_farmer" because:

1. Missing `monitor/migrations/__init__.py` file
2. Missing `monitor/migrations/0001_initial.py` (base migration)
3. Only `0002_enhance_models.py` existed, which depends on `0001_initial.py`
4. Slow internet connection causing package installation timeouts

## Solutions Applied

### 1. Created Missing Migration Files

**File: `monitor/migrations/__init__.py`**
- Required Python package marker for migrations directory

**File: `monitor/migrations/0001_initial.py`**
- Creates all base database tables:
  - Farmer (user profile with phone and county)
  - Farm (farm details with location and size)
  - Crop (crop tracking with growth stages)
  - WeatherRecord (weather data for farms)
  - YieldPrediction (crop yield predictions)
  - Alert (notifications for farmers)

### 2. Created Helper Scripts

**File: `quick_start.bat`** (RECOMMENDED)
- Fastest way to get started
- Installs only essential packages (Django, requests, python-dotenv, Pillow)
- Creates database automatically
- Starts development server
- Works well with slow internet

**File: `run_migrations.bat`**
- Runs database migrations only
- Useful when you already have packages installed

**File: `manage_system.bat`**
- Interactive menu for common tasks
- Start server, run migrations, create superuser, etc.

**File: `START_HERE.txt`**
- Simple text guide for getting started
- Lists all available options

### 3. Updated Existing Scripts

**File: `setup.bat`**
- Modified to install essential packages first
- Optional packages installed separately
- Better error handling for slow connections
- Increased timeout to 300 seconds

**File: `QUICKSTART.md`**
- Updated with new quick start instructions
- Added troubleshooting section
- Documented all helper scripts

## Migration Chain

The correct migration order is now:
1. `0001_initial.py` - Creates base tables
2. `0002_enhance_models.py` - Adds enhancements (indexes, new fields)

## How to Use

### For First Time Setup:
```cmd
quick_start.bat
```

### If You Already Have Virtual Environment:
```cmd
run_migrations.bat
```

### For Interactive Management:
```cmd
manage_system.bat
```

## Database Schema Created

### Farmer Table
- Links to Django User model
- Stores phone number and county
- One farmer can have multiple farms

### Farm Table
- Belongs to a Farmer
- Stores location (with optional GPS coordinates)
- Tracks size in acres and soil type
- Has timestamps for creation and updates

### Crop Table
- Belongs to a Farm
- Tracks crop type (maize, beans, wheat, coffee, tea, potato, tomato)
- Monitors growth stages (germination → harvest)
- Records planting and harvest dates
- Calculates days since planting

### WeatherRecord Table
- Linked to Farm
- Stores temperature, humidity, rainfall, wind speed
- Tracks weather conditions over time

### YieldPrediction Table
- Linked to Crop
- Stores predicted and actual yields
- Includes confidence scores

### Alert Table
- Linked to Farm
- Different types: weather, pest, disease, irrigation, harvest
- Severity levels: low, medium, high, critical
- Tracks read/unread status

## Testing the Fix

1. Run `quick_start.bat`
2. Open http://127.0.0.1:8000/
3. Click "Register" to create a farmer account
4. Login and access the dashboard
5. Add farms and crops

No more "no such table" errors!

## Package Requirements

### Essential (Always Installed):
- Django==4.2.7
- requests
- python-dotenv
- Pillow

### Optional (For Advanced Features):
- pandas==2.1.3
- numpy==1.26.2
- scikit-learn==1.3.2

The system works perfectly with just the essential packages!

## Academic Project Information

- Institution: Kisii University
- Student: ARON SIGEI
- Registration: IN13/00030/21
- Version: 1.1.0
- Purpose: Climate monitoring system for Kenyan farmers

---

**Status: ✓ All Issues Resolved**

The Climate Crop Monitor system is now fully functional and ready for use!
