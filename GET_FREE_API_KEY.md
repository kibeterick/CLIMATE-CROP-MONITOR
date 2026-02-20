# 🆓 Get Your FREE OpenWeatherMap API Key (Students)

## Why You Need This
Your Climate Crop Monitor needs weather data to work properly. OpenWeatherMap provides **FREE** weather data perfect for student projects!

## What You Get FREE
- ✅ 1,000 API calls per day (more than enough!)
- ✅ Current weather for any location
- ✅ 5-day weather forecast
- ✅ No credit card required
- ✅ Perfect for academic projects

## Step-by-Step Guide (2 minutes)

### Step 1: Go to OpenWeatherMap
Visit: https://openweathermap.org/api

### Step 2: Sign Up (FREE)
- Click "Sign Up" button
- Fill in your details:
  - **Username**: Your choice
  - **Email**: Your student email
  - **Password**: Create a strong password
  - **Company**: "Student Project" or "Kisii University"
  - **Purpose**: "Education"

### Step 3: Verify Email
- Check your email inbox
- Click the verification link
- Login to your account

### Step 4: Get Your API Key
- After login, click on your username (top right)
- Click "My API Keys"
- You'll see a default API key already created
- Copy this key (it looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

### Step 5: Add to Your Project
- Open `add_api_key.bat` in your project folder
- Run it and paste your API key when prompted
- OR manually edit `.env` file and replace `PUT_YOUR_FREE_API_KEY_HERE` with your key

## Example API Key Format
```
OPENWEATHER_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

## Test Your API Key
After adding the key:
1. Run your project: `quick_start.bat`
2. Register/login to your system
3. Add a farm with location
4. Check if weather data appears on dashboard

## Troubleshooting

### "Invalid API key" error
- Wait 10-15 minutes after creating account (activation delay)
- Check if you copied the key correctly (no extra spaces)

### No weather data showing
- Make sure you added the API key correctly
- Check your internet connection
- The system works with demo data even without API key

### API limit exceeded
- Free plan: 1,000 calls/day
- For student projects, this is usually enough
- Reset happens every 24 hours

## Academic Use
This is perfect for your Kisii University project! The free tier provides all the weather data you need for your Climate Crop Monitor system.

## Need Help?
- OpenWeatherMap FAQ: https://openweathermap.org/faq
- Your system works with demo data if you can't get the API key
- Focus on your project functionality first, add real weather data later

---

**Remember**: Your project works perfectly without the API key (uses demo data). The API key just makes it more realistic with real weather information!