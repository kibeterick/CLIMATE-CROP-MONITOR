# Climate Crop Monitor - Quick Start Guide

## FASTEST WAY TO START (2 Minutes!)

### Option 1: Super Quick Start (Recommended)
```cmd
quick_start.bat
```
This automatically:
- Creates virtual environment
- Installs essential packages (Django, requests, python-dotenv, Pillow)
- Sets up database
- Starts the server

Then open http://127.0.0.1:8000/ and click "Register"!

### Option 2: Full Setup with All Features
```cmd
setup.bat
```
Installs everything including optional analytics packages (pandas, numpy, scikit-learn).
Note: May be slow with poor internet connection.

---

## Detailed Setup (If You Need It)

### Step 1: Run Setup
Choose one of the batch files above based on your internet speed.

### Step 2: Get API Key (Optional - for weather features)
1. Visit https://openweathermap.org/api
2. Sign up (free)
3. Copy your API key
4. Open `.env` file
5. Paste: `OPENWEATHER_API_KEY=your-key-here`

### Step 3: Create Admin User (Optional)
```cmd
venv\Scripts\python.exe manage.py createsuperuser
```
Enter username, email (optional), and password.

### Step 4: Load Sample Data (Optional)
```cmd
venv\Scripts\python.exe manage.py seed_data
```
This creates a test farmer account with sample farms and crops.

### Step 5: Start Server
```cmd
python manage.py runserver
```

### Step 6: Access Application
Open browser: http://127.0.0.1:8000/

## Test Credentials (if you ran seed_data)
- Username: `testfarmer`
- Password: `testpass123`

## First Steps in the App

1. **Register/Login**: Create your farmer account
2. **Add Farm**: Click "Add New Farm" and enter details
3. **Register Crop**: Select farm, click "Add Crop"
4. **Update Weather**: Click "Update Weather" on farm page
5. **View Predictions**: Go to crop details to see yield predictions

## Common Commands

### Activate Virtual Environment
```cmd
venv\Scripts\activate
```

### Run Server
```cmd
python manage.py runserver
```

### Create Superuser
```cmd
python manage.py createsuperuser
```

### Access Admin Panel
http://127.0.0.1:8000/admin/

### Load Test Data
```cmd
python manage.py seed_data
```

### Reset Database
```cmd
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Troubleshooting

**Problem**: Can't activate virtual environment  
**Solution**: Run `python -m venv venv` first

**Problem**: Weather not loading  
**Solution**: Check API key in `.env` file

**Problem**: Page not found  
**Solution**: Make sure server is running

## Need Help?

- Read: `INSTALLATION.md` for detailed setup
- Read: `USER_MANUAL.md` for usage guide
- Read: `PROJECT_DOCUMENTATION.md` for technical details

## Project Structure
```
Climate Crop Monitor/
├── manage.py              # Django management
├── setup.bat             # Automated setup
├── requirements.txt      # Dependencies
├── .env                  # Configuration (create from .env.example)
├── ccm_project/          # Project settings
├── monitor/              # Main app
│   ├── models.py         # Database models
│   ├── views.py          # Views
│   ├── urls.py           # URLs
│   ├── weather_service.py    # Weather API
│   └── prediction_service.py # Predictions
└── templates/            # HTML templates
```

## Key Features

✓ Farm Management  
✓ Crop Monitoring  
✓ Weather Tracking  
✓ Yield Predictions  
✓ Smart Alerts  
✓ Analytics Dashboard  

## Support

Developer: ARON SIGEI (IN13/00030/21)  
Institution: Kisii University  
Department: Computing  

---

**Ready to start? Run `setup.bat` now!**


---

## Helper Scripts

We've created several batch files to make your life easier:

### quick_start.bat
The fastest way to get started. Handles everything automatically.

### manage_system.bat
Interactive menu for common tasks:
- Start/stop server
- Run migrations
- Create superuser
- Load sample data
- Update weather data
- Check system status

### run_migrations.bat
Just runs database migrations (useful after updates).

### setup.bat
Full installation with all packages.

---

## Troubleshooting

### "No module named django" error
Run `quick_start.bat` - it will install Django automatically.

### "No such table" error
The database needs to be created. Run:
```cmd
venv\Scripts\python.exe manage.py migrate
```

### Slow internet connection
Use `quick_start.bat` instead of `setup.bat`. It only installs essential packages.
You can add optional analytics packages later:
```cmd
venv\Scripts\pip.exe install pandas numpy scikit-learn
```

### Migration errors
Delete `db.sqlite3` and run `quick_start.bat` again.

---

## What's Fixed in This Version

✓ Created missing migration files (0001_initial.py)
✓ Fixed database setup issues
✓ Added quick start scripts for easy setup
✓ Optimized for slow internet connections
✓ Added management menu for common tasks

Your Climate Crop Monitor system is ready to use!
