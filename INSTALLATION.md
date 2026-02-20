# Climate Crop Monitor - Installation Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection for API access

## Installation Steps

### 1. Automated Setup (Windows)
Run the setup script:
```cmd
setup.bat
```

### 2. Manual Setup

#### Step 1: Create Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Step 2: Install Dependencies
```cmd
pip install -r requirements.txt
```

#### Step 3: Configure Environment
Copy `.env.example` to `.env`:
```cmd
copy .env.example .env
```

Edit `.env` and add your OpenWeatherMap API key:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
OPENWEATHER_API_KEY=your-api-key-here
```

To get a free API key:
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key
4. Copy it to your .env file

#### Step 4: Run Migrations
```cmd
python manage.py makemigrations
python manage.py migrate
```

#### Step 5: Create Superuser
```cmd
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

#### Step 6: Run Development Server
```cmd
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Initial Setup

### 1. Access the Application
- Open your browser and go to http://127.0.0.1:8000/
- Register a new farmer account or login

### 2. Add Your First Farm
- Click "Add New Farm"
- Enter farm details (name, location, size)
- The system will automatically fetch coordinates

### 3. Register Crops
- Select a farm
- Click "Add Crop"
- Enter crop details and planting date

### 4. Update Weather Data
- Go to farm details
- Click "Update Weather"
- System will fetch current weather data

## Admin Panel
Access the admin panel at: http://127.0.0.1:8000/admin/
- Username: (your superuser username)
- Password: (your superuser password)

## Troubleshooting

### Issue: Module not found
Solution: Make sure virtual environment is activated
```cmd
venv\Scripts\activate
```

### Issue: Weather data not loading
Solution: Check your API key in .env file

### Issue: Database errors
Solution: Delete db.sqlite3 and run migrations again
```cmd
del db.sqlite3
python manage.py migrate
```

## Project Structure
```
Climate Crop Monitor/
├── ccm_project/          # Django project settings
├── monitor/              # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configuration
│   ├── weather_service.py    # Weather API integration
│   └── prediction_service.py # Yield prediction logic
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Support
For issues or questions, contact: ARON SIGEI (IN13/00030/21)
Kisii University - Department of Computing
