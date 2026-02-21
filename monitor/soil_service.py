"""
Soil Analysis and Measurement Service
"""
from decimal import Decimal


class SoilAnalysisService:
    """Soil analysis and recommendations for farmers"""
    
    @staticmethod
    def analyze_soil_ph(ph_value, crop_type=None):
        """Analyze soil pH"""
        ph = float(ph_value)
        
        if ph < 5.5:
            classification = 'Acidic'
            status = 'needs_lime'
        elif ph < 7.0:
            classification = 'Slightly Acidic'
            status = 'good'
        elif ph == 7.0:
            classification = 'Neutral'
            status = 'excellent'
        elif ph < 8.0:
            classification = 'Slightly Alkaline'
            status = 'good'
        else:
            classification = 'Alkaline'
            status = 'needs_sulfur'
        
        recommendations = []
        if status == 'needs_lime':
            recommendations.append("Add agricultural lime to raise pH")
        elif status == 'needs_sulfur':
            recommendations.append("Add sulfur to lower pH")
        
        return {
            'ph_value': ph,
            'classification': classification,
            'status': status,
            'recommendations': recommendations
        }
    
    @staticmethod
    def analyze_nutrients(nitrogen, phosphorus, potassium):
        """Analyze NPK levels"""
        
        def classify(value):
            v = float(value)
            if v < 30:
                return 'Low', 'Add fertilizer'
            elif v < 60:
                return 'Medium', 'Maintain levels'
            else:
                return 'High', 'Sufficient'
        
        n_level, n_rec = classify(nitrogen)
        p_level, p_rec = classify(phosphorus)
        k_level, k_rec = classify(potassium)
        
        return {
            'nitrogen': {'level': n_level, 'recommendation': n_rec},
            'phosphorus': {'level': p_level, 'recommendation': p_rec},
            'potassium': {'level': k_level, 'recommendation': k_rec}
        }
    
    @staticmethod
    def analyze_soil_moisture(moisture_percentage):
        """Analyze soil moisture"""
        moisture = float(moisture_percentage)
        
        if moisture < 20:
            status = 'Dry'
            recommendation = 'Irrigation needed immediately'
        elif moisture < 40:
            status = 'Low'
            recommendation = 'Consider irrigation soon'
        elif moisture < 70:
            status = 'Optimal'
            recommendation = 'Moisture level is good'
        else:
            status = 'Saturated'
            recommendation = 'Improve drainage, reduce watering'
        
        return {
            'moisture': moisture,
            'status': status,
            'recommendation': recommendation
        }
    
    @staticmethod
    def get_soil_recommendations(soil_type, crop_type):
        """Get recommendations based on soil and crop type"""
        recommendations = []
        
        # Soil-specific recommendations
        if soil_type == 'sandy':
            recommendations.append("Add organic matter to improve water retention")
            recommendations.append("Apply fertilizer more frequently in small amounts")
        elif soil_type == 'clay':
            recommendations.append("Add organic matter to improve drainage")
            recommendations.append("Avoid overwatering to prevent waterlogging")
        elif soil_type == 'loam':
            recommendations.append("Ideal soil! Maintain organic matter levels")
        
        # Crop-specific recommendations
        if crop_type == 'maize':
            recommendations.append("Maize needs well-drained soil with pH 5.5-7.0")
        elif crop_type == 'beans':
            recommendations.append("Beans prefer slightly acidic soil (pH 6.0-7.5)")
        elif crop_type == 'coffee':
            recommendations.append("Coffee thrives in acidic volcanic soil (pH 5.0-6.5)")
        elif crop_type == 'tea':
            recommendations.append("Tea needs acidic soil (pH 4.5-6.0)")
        
        return recommendations
