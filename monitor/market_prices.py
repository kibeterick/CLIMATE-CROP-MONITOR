"""
Market prices and economic insights for farmers
"""
from decimal import Decimal
from datetime import datetime


class MarketPriceService:
    """Market price information for crops"""
    
    # Sample market prices (KES per kg) - In production, fetch from real API
    MARKET_PRICES = {
        'maize': {
            'wholesale': Decimal('45.00'),
            'retail': Decimal('60.00'),
            'trend': 'stable',
            'last_updated': '2026-02-20'
        },
        'beans': {
            'wholesale': Decimal('120.00'),
            'retail': Decimal('150.00'),
            'trend': 'rising',
            'last_updated': '2026-02-20'
        },
        'wheat': {
            'wholesale': Decimal('50.00'),
            'retail': Decimal('70.00'),
            'trend': 'falling',
            'last_updated': '2026-02-20'
        },
        'coffee': {
            'wholesale': Decimal('450.00'),
            'retail': Decimal('600.00'),
            'trend': 'rising',
            'last_updated': '2026-02-20'
        },
        'tea': {
            'wholesale': Decimal('350.00'),
            'retail': Decimal('500.00'),
            'trend': 'stable',
            'last_updated': '2026-02-20'
        },
        'potato': {
            'wholesale': Decimal('40.00'),
            'retail': Decimal('55.00'),
            'trend': 'stable',
            'last_updated': '2026-02-20'
        },
        'tomato': {
            'wholesale': Decimal('60.00'),
            'retail': Decimal('80.00'),
            'trend': 'rising',
            'last_updated': '2026-02-20'
        }
    }
    
    @staticmethod
    def get_price(crop_type):
        """Get current market price for crop"""
        return MarketPriceService.MARKET_PRICES.get(crop_type, {
            'wholesale': Decimal('0.00'),
            'retail': Decimal('0.00'),
            'trend': 'unknown',
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        })
    
    @staticmethod
    def calculate_revenue(crop, predicted_yield_kg):
        """Calculate potential revenue from crop"""
        price_info = MarketPriceService.get_price(crop.crop_type)
        
        wholesale_revenue = predicted_yield_kg * price_info['wholesale']
        retail_revenue = predicted_yield_kg * price_info['retail']
        
        return {
            'predicted_yield_kg': predicted_yield_kg,
            'wholesale_price': price_info['wholesale'],
            'retail_price': price_info['retail'],
            'wholesale_revenue': wholesale_revenue,
            'retail_revenue': retail_revenue,
            'price_trend': price_info['trend'],
            'last_updated': price_info['last_updated']
        }
    
    @staticmethod
    def get_all_prices():
        """Get all current market prices"""
        return MarketPriceService.MARKET_PRICES
    
    @staticmethod
    def get_best_crops_to_plant(location='Kenya'):
        """Recommend most profitable crops based on market prices"""
        prices = MarketPriceService.MARKET_PRICES
        
        # Sort by retail price (profitability indicator)
        sorted_crops = sorted(
            prices.items(),
            key=lambda x: x[1]['retail'],
            reverse=True
        )
        
        recommendations = []
        for crop_type, price_info in sorted_crops[:5]:
            recommendations.append({
                'crop': crop_type.title(),
                'retail_price': price_info['retail'],
                'trend': price_info['trend'],
                'profitability': 'High' if price_info['retail'] > 200 else 'Medium' if price_info['retail'] > 100 else 'Standard'
            })
        
        return recommendations


class CostCalculator:
    """Calculate farming costs and profitability"""
    
    # Average costs per acre (KES) - Sample data
    FARMING_COSTS = {
        'maize': {
            'seeds': 3000,
            'fertilizer': 8000,
            'pesticides': 2000,
            'labor': 5000,
            'irrigation': 3000,
            'total': 21000
        },
        'beans': {
            'seeds': 4000,
            'fertilizer': 6000,
            'pesticides': 2500,
            'labor': 4000,
            'irrigation': 2000,
            'total': 18500
        },
        'wheat': {
            'seeds': 3500,
            'fertilizer': 7000,
            'pesticides': 2000,
            'labor': 4500,
            'irrigation': 2500,
            'total': 19500
        },
        'coffee': {
            'seeds': 15000,
            'fertilizer': 12000,
            'pesticides': 5000,
            'labor': 10000,
            'irrigation': 5000,
            'total': 47000
        },
        'tea': {
            'seeds': 12000,
            'fertilizer': 10000,
            'pesticides': 4000,
            'labor': 8000,
            'irrigation': 4000,
            'total': 38000
        },
        'potato': {
            'seeds': 25000,
            'fertilizer': 8000,
            'pesticides': 3000,
            'labor': 6000,
            'irrigation': 3000,
            'total': 45000
        },
        'tomato': {
            'seeds': 5000,
            'fertilizer': 10000,
            'pesticides': 4000,
            'labor': 8000,
            'irrigation': 6000,
            'total': 33000
        }
    }
    
    @staticmethod
    def calculate_profitability(crop, area_acres, predicted_yield_kg):
        """Calculate profit/loss for crop"""
        costs = CostCalculator.FARMING_COSTS.get(crop.crop_type, {})
        total_cost = costs.get('total', 0) * float(area_acres)
        
        revenue_info = MarketPriceService.calculate_revenue(crop, predicted_yield_kg)
        wholesale_revenue = float(revenue_info['wholesale_revenue'])
        retail_revenue = float(revenue_info['retail_revenue'])
        
        return {
            'total_cost': total_cost,
            'cost_breakdown': costs,
            'wholesale_revenue': wholesale_revenue,
            'retail_revenue': retail_revenue,
            'wholesale_profit': wholesale_revenue - total_cost,
            'retail_profit': retail_revenue - total_cost,
            'roi_wholesale': ((wholesale_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            'roi_retail': ((retail_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            'break_even_kg': total_cost / float(revenue_info['wholesale_price']) if revenue_info['wholesale_price'] > 0 else 0
        }
