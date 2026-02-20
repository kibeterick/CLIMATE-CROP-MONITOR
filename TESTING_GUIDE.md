# Climate Crop Monitor - Testing Guide

## Test Environment Setup

### Prerequisites
```cmd
# Activate virtual environment
venv\Scripts\activate

# Ensure all dependencies are installed
pip install -r requirements.txt

# Load test data
python manage.py seed_data
```

## Manual Testing Checklist

### 1. User Authentication Tests

#### TC-01: User Registration
**Steps:**
1. Navigate to http://127.0.0.1:8000/
2. Click "Register"
3. Enter username: "testuser1"
4. Select county: "Kiambu"
5. Enter password: "testpass123"
6. Confirm password: "testpass123"
7. Click "Register"

**Expected Result:** User is created and redirected to dashboard

**Status:** ✅ PASS

#### TC-02: User Login
**Steps:**
1. Navigate to login page
2. Enter username: "testfarmer"
3. Enter password: "testpass123"
4. Click "Login"

**Expected Result:** User is authenticated and sees dashboard

**Status:** ✅ PASS

#### TC-03: User Logout
**Steps:**
1. Login as testfarmer
2. Click "Logout" in navigation

**Expected Result:** User is logged out and redirected to login page

**Status:** ✅ PASS

### 2. Farm Management Tests

#### TC-04: Create New Farm
**Steps:**
1. Login as testfarmer
2. Navigate to "Farms" → "Add New Farm"
3. Enter farm name: "Test Farm"
4. Enter location: "Nakuru"
5. Enter size: "10.5"
6. Select soil type: "Loam"
7. Click "Create Farm"

**Expected Result:** Farm is created with GPS coordinates fetched automatically

**Status:** ✅ PASS

#### TC-05: View Farm List
**Steps:**
1. Login as testfarmer
2. Click "Farms" in navigation

**Expected Result:** All user's farms are displayed with details

**Status:** ✅ PASS

#### TC-06: View Farm Details
**Steps:**
1. Navigate to farm list
2. Click "View Details" on any farm

**Expected Result:** Farm details page shows farm info, weather, crops, and alerts

**Status:** ✅ PASS

### 3. Crop Management Tests

#### TC-07: Register New Crop
**Steps:**
1. Navigate to farm detail page
2. Click "Add Crop"
3. Select crop type: "Maize"
4. Enter variety: "H614"
5. Enter planting date: (today's date)
6. Enter area: "5.0"
7. Click "Register Crop"

**Expected Result:** Crop is registered and appears in farm's crop list

**Status:** ✅ PASS

#### TC-08: View Crop Details
**Steps:**
1. Navigate to dashboard
2. Click "View" on any active crop

**Expected Result:** Crop details page shows:
- Crop information
- Growth stage
- Yield prediction
- Growth progress
- Weather history

**Status:** ✅ PASS

#### TC-09: Growth Stage Tracking
**Steps:**
1. View crop planted 45 days ago
2. Check current stage

**Expected Result:** System correctly identifies stage as "Vegetative"

**Status:** ✅ PASS

### 4. Weather Integration Tests

#### TC-10: Fetch Weather Data
**Steps:**
1. Navigate to farm detail page
2. Click "Update Weather"
3. Wait for API response

**Expected Result:** 
- Weather data is fetched from API
- New weather record is created
- Success message is displayed
- Weather data appears on farm page

**Status:** ✅ PASS

#### TC-11: Display Current Weather
**Steps:**
1. Navigate to dashboard
2. View "Current Weather" card

**Expected Result:** Shows temperature, humidity, and wind speed

**Status:** ✅ PASS

#### TC-12: Weather History
**Steps:**
1. Navigate to crop detail page
2. Scroll to "Weather History" section

**Expected Result:** Table shows historical weather records with dates

**Status:** ✅ PASS

### 5. Yield Prediction Tests

#### TC-13: Generate Yield Prediction
**Steps:**
1. Navigate to crop with weather data
2. View "Yield Prediction" card

**Expected Result:**
- Predicted yield in bags is displayed
- Confidence score is shown (30-95%)
- Prediction date is visible

**Status:** ✅ PASS

#### TC-14: Prediction Accuracy
**Steps:**
1. Create crop with 30 days of weather data
2. Check prediction confidence

**Expected Result:** Confidence score increases with more data (60%+)

**Status:** ✅ PASS

### 6. Alert System Tests

#### TC-15: Weather Alert Generation
**Steps:**
1. Update weather with temperature > 35°C
2. Check alerts

**Expected Result:** High temperature alert is created automatically

**Status:** ✅ PASS

#### TC-16: View Alerts List
**Steps:**
1. Click "Alerts" in navigation
2. View all alerts

**Expected Result:** All alerts are displayed with severity badges

**Status:** ✅ PASS

#### TC-17: Mark Alert as Read
**Steps:**
1. Navigate to alerts list
2. Click "Mark as Read" on unread alert

**Expected Result:** Alert status changes to read

**Status:** ✅ PASS

### 7. Dashboard Tests

#### TC-18: Dashboard Metrics
**Steps:**
1. Login and view dashboard

**Expected Result:** Dashboard shows:
- Total farms count
- Active crops count
- Alerts count
- Current weather

**Status:** ✅ PASS

#### TC-19: Recent Alerts Display
**Steps:**
1. View dashboard
2. Check "Recent Alerts" section

**Expected Result:** Shows up to 5 most recent unread alerts

**Status:** ✅ PASS

#### TC-20: Active Crops Table
**Steps:**
1. View dashboard
2. Check "Active Crops" table

**Expected Result:** Shows up to 5 active crops with growth stages

**Status:** ✅ PASS

### 8. Navigation Tests

#### TC-21: Navigation Menu
**Steps:**
1. Login as user
2. Check navigation bar

**Expected Result:** Shows Dashboard, Farms, Alerts, Username, Logout

**Status:** ✅ PASS

#### TC-22: Breadcrumb Navigation
**Steps:**
1. Navigate: Dashboard → Farms → Farm Detail → Crop Detail
2. Use back buttons

**Expected Result:** Can navigate back through pages easily

**Status:** ✅ PASS

### 9. Responsive Design Tests

#### TC-23: Mobile View
**Steps:**
1. Open application in mobile browser or resize window
2. Navigate through pages

**Expected Result:** All pages are responsive and usable on mobile

**Status:** ✅ PASS

#### TC-24: Tablet View
**Steps:**
1. Open application in tablet browser
2. Check layout

**Expected Result:** Layout adapts appropriately for tablet screens

**Status:** ✅ PASS

### 10. Admin Panel Tests

#### TC-25: Admin Access
**Steps:**
1. Navigate to http://127.0.0.1:8000/admin/
2. Login with superuser credentials

**Expected Result:** Admin panel is accessible

**Status:** ✅ PASS

#### TC-26: Admin CRUD Operations
**Steps:**
1. Login to admin panel
2. Create, read, update, delete records

**Expected Result:** All CRUD operations work correctly

**Status:** ✅ PASS

## Performance Tests

### Load Time Tests
- **Home Page**: < 1 second ✅
- **Dashboard**: < 2 seconds ✅
- **Farm Detail**: < 2 seconds ✅
- **Crop Detail**: < 3 seconds ✅
- **Weather Update**: < 5 seconds (API dependent) ✅

### Database Query Tests
- **Farm List**: < 100ms ✅
- **Crop List**: < 100ms ✅
- **Weather Records**: < 150ms ✅
- **Predictions**: < 200ms ✅

## Security Tests

### Authentication Tests
- ✅ Unauthenticated users redirected to login
- ✅ Users can only access their own data
- ✅ Passwords are hashed in database
- ✅ CSRF tokens present in forms

### Authorization Tests
- ✅ Users cannot access other farmers' farms
- ✅ Users cannot modify other farmers' crops
- ✅ Admin panel requires superuser access

## API Integration Tests

### OpenWeatherMap API
- ✅ Successful connection with valid API key
- ✅ Proper error handling for invalid API key
- ✅ Timeout handling (10 seconds)
- ✅ Data parsing and storage

## Edge Cases Tests

### TC-27: Empty States
**Test:** View dashboard with no farms
**Expected:** Shows helpful message with "Add Farm" button
**Status:** ✅ PASS

### TC-28: Invalid Location
**Test:** Create farm with non-existent location
**Expected:** Farm is created but coordinates remain null
**Status:** ✅ PASS

### TC-29: No Weather Data
**Test:** View crop with no weather records
**Expected:** Shows message and "Fetch Weather Data" button
**Status:** ✅ PASS

### TC-30: Old Crop
**Test:** View crop planted 150 days ago
**Expected:** Shows "Harvest" stage
**Status:** ✅ PASS

## Usability Tests

### User Feedback
- ✅ Forms are clear and easy to understand
- ✅ Error messages are helpful
- ✅ Success messages confirm actions
- ✅ Navigation is intuitive
- ✅ Icons enhance understanding

### Accessibility
- ✅ Color contrast is sufficient
- ✅ Forms have proper labels
- ✅ Buttons are clearly labeled
- ✅ Error states are visible

## Test Summary

**Total Test Cases**: 30  
**Passed**: 30 ✅  
**Failed**: 0  
**Success Rate**: 100%

## Known Issues

None identified during testing.

## Recommendations

1. Add automated unit tests using Django's TestCase
2. Implement integration tests for API calls
3. Add end-to-end tests using Selenium
4. Set up continuous integration (CI) pipeline
5. Add performance monitoring in production

## Test Data

### Test Accounts
- **Username**: testfarmer
- **Password**: testpass123
- **Farms**: 2 (Green Valley Farm, Sunrise Farm)
- **Crops**: 3 (Maize, Beans, Wheat)

### API Keys Required
- OpenWeatherMap API key (free tier sufficient)

## Running Automated Tests (Future)

```cmd
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test monitor

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Conclusion

All manual test cases have passed successfully. The system is stable, secure, and ready for deployment. The application meets all functional and non-functional requirements specified in the project documentation.

---

**Tested By**: ARON SIGEI  
**Date**: February 2026  
**Status**: ✅ ALL TESTS PASSED
