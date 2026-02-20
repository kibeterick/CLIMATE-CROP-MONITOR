"""
Notification service for SMS and Email alerts
"""
from django.core.mail import send_mail
from django.conf import settings
import requests


class NotificationService:
    """Handle SMS and Email notifications for farmers"""
    
    @staticmethod
    def send_sms(phone_number, message):
        """
        Send SMS notification using Africa's Talking API (FREE tier available)
        For production, sign up at: https://africastalking.com/
        """
        # Demo implementation - replace with actual API credentials
        if not hasattr(settings, 'AFRICASTALKING_API_KEY'):
            print(f"SMS to {phone_number}: {message}")
            return True
        
        try:
            # Africa's Talking API integration
            url = "https://api.africastalking.com/version1/messaging"
            headers = {
                'apiKey': settings.AFRICASTALKING_API_KEY,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'username': settings.AFRICASTALKING_USERNAME,
                'to': phone_number,
                'message': message
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            return response.status_code == 201
            
        except Exception as e:
            print(f"SMS Error: {e}")
            return False
    
    @staticmethod
    def send_email(email, subject, message):
        """Send email notification"""
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Email Error: {e}")
            return False
    
    @staticmethod
    def send_weather_alert(farmer, farm, weather_data):
        """Send weather alert to farmer"""
        temp = weather_data['temperature']
        
        if temp > 35:
            message = f"High Temperature Alert for {farm.name}: {temp}°C. Consider irrigation and shade for crops."
        elif temp < 10:
            message = f"Low Temperature Alert for {farm.name}: {temp}°C. Protect sensitive crops from cold."
        else:
            return False
        
        # Send SMS if phone number available
        if farmer.phone_number:
            NotificationService.send_sms(farmer.phone_number, message)
        
        # Send email if available
        if farmer.user.email:
            NotificationService.send_email(
                farmer.user.email,
                f"Weather Alert - {farm.name}",
                message
            )
        
        return True
    
    @staticmethod
    def send_harvest_reminder(farmer, crop):
        """Send harvest reminder"""
        days_until_harvest = (crop.expected_harvest_date - crop.planting_date).days
        
        message = f"Harvest Reminder: Your {crop.get_crop_type_display()} at {crop.farm.name} is approaching harvest stage. Expected in {days_until_harvest} days."
        
        if farmer.phone_number:
            NotificationService.send_sms(farmer.phone_number, message)
        
        if farmer.user.email:
            NotificationService.send_email(
                farmer.user.email,
                "Harvest Reminder",
                message
            )
        
        return True
    
    @staticmethod
    def send_pest_alert(farmer, farm, pest_name, severity):
        """Send pest/disease alert"""
        message = f"PEST ALERT ({severity}): {pest_name} detected in {farm.location} area. Check your {farm.name} farm immediately."
        
        if farmer.phone_number:
            NotificationService.send_sms(farmer.phone_number, message)
        
        if farmer.user.email:
            NotificationService.send_email(
                farmer.user.email,
                f"Pest Alert - {pest_name}",
                message
            )
        
        return True
