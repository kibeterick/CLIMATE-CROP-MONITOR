"""
Pest and Disease Database for Crop Management
"""


class PestDiseaseDatabase:
    """Database of common pests and diseases affecting Kenyan crops"""
    
    PESTS_DISEASES = {
        'maize': [
            {
                'name': 'Fall Armyworm',
                'type': 'pest',
                'severity': 'high',
                'symptoms': 'Holes in leaves, damaged tassels, frass in whorl',
                'treatment': 'Apply Bt-based pesticides, use pheromone traps, practice crop rotation',
                'prevention': 'Early planting, intercropping with legumes, regular scouting'
            },
            {
                'name': 'Maize Streak Virus',
                'type': 'disease',
                'severity': 'high',
                'symptoms': 'Yellow streaks on leaves, stunted growth',
                'treatment': 'No cure - remove infected plants, control leafhoppers',
                'prevention': 'Use resistant varieties, control leafhopper vectors'
            },
            {
                'name': 'Maize Weevil',
                'type': 'pest',
                'severity': 'medium',
                'symptoms': 'Holes in stored grains, powder in storage',
                'treatment': 'Fumigate storage, use hermetic bags',
                'prevention': 'Proper drying before storage, clean storage facilities'
            }
        ],
        'beans': [
            {
                'name': 'Bean Fly',
                'type': 'pest',
                'severity': 'high',
                'symptoms': 'Wilting seedlings, stem tunneling',
                'treatment': 'Apply systemic insecticides, remove infected plants',
                'prevention': 'Seed treatment, early planting, use resistant varieties'
            },
            {
                'name': 'Angular Leaf Spot',
                'type': 'disease',
                'severity': 'medium',
                'symptoms': 'Angular brown spots on leaves',
                'treatment': 'Apply copper-based fungicides',
                'prevention': 'Use certified seeds, crop rotation, avoid overhead irrigation'
            }
        ],
        'coffee': [
            {
                'name': 'Coffee Berry Disease',
                'type': 'disease',
                'severity': 'critical',
                'symptoms': 'Dark sunken lesions on berries',
                'treatment': 'Apply copper fungicides regularly',
                'prevention': 'Prune for air circulation, remove infected berries'
            },
            {
                'name': 'Coffee Leaf Rust',
                'type': 'disease',
                'severity': 'high',
                'symptoms': 'Orange-yellow spots on leaf undersides',
                'treatment': 'Apply systemic fungicides',
                'prevention': 'Use resistant varieties, proper spacing, shade management'
            }
        ],
        'tea': [
            {
                'name': 'Tea Mosquito Bug',
                'type': 'pest',
                'severity': 'high',
                'symptoms': 'Distorted shoots, brown lesions',
                'treatment': 'Apply approved insecticides',
                'prevention': 'Regular pruning, remove alternate hosts'
            },
            {
                'name': 'Blister Blight',
                'type': 'disease',
                'severity': 'high',
                'symptoms': 'Translucent spots on young leaves',
                'treatment': 'Apply copper fungicides',
                'prevention': 'Proper spacing, avoid overhead irrigation'
            }
        ],
        'potato': [
            {
                'name': 'Late Blight',
                'type': 'disease',
                'severity': 'critical',
                'symptoms': 'Dark water-soaked lesions on leaves and tubers',
                'treatment': 'Apply metalaxyl or mancozeb fungicides',
                'prevention': 'Use certified seeds, hill properly, destroy infected plants'
            },
            {
                'name': 'Potato Tuber Moth',
                'type': 'pest',
                'severity': 'high',
                'symptoms': 'Tunnels in tubers, leaf mining',
                'treatment': 'Apply Bt-based insecticides',
                'prevention': 'Deep planting, proper hilling, clean storage'
            }
        ],
        'tomato': [
            {
                'name': 'Tomato Leaf Miner (Tuta absoluta)',
                'type': 'pest',
                'severity': 'critical',
                'symptoms': 'Irregular mines in leaves, damaged fruits',
                'treatment': 'Use pheromone traps, apply approved insecticides',
                'prevention': 'Screen greenhouses, destroy crop residues, rotate crops'
            },
            {
                'name': 'Early Blight',
                'type': 'disease',
                'severity': 'medium',
                'symptoms': 'Concentric rings on older leaves',
                'treatment': 'Apply chlorothalonil or mancozeb',
                'prevention': 'Crop rotation, mulching, avoid overhead watering'
            },
            {
                'name': 'Bacterial Wilt',
                'type': 'disease',
                'severity': 'high',
                'symptoms': 'Sudden wilting, no leaf yellowing',
                'treatment': 'No cure - remove and destroy infected plants',
                'prevention': 'Use resistant varieties, crop rotation, soil solarization'
            }
        ],
        'wheat': [
            {
                'name': 'Wheat Rust',
                'type': 'disease',
                'severity': 'high',
                'symptoms': 'Orange-red pustules on leaves and stems',
                'treatment': 'Apply triazole fungicides',
                'prevention': 'Use resistant varieties, timely planting'
            },
            {
                'name': 'Aphids',
                'type': 'pest',
                'severity': 'medium',
                'symptoms': 'Sticky honeydew, yellowing leaves',
                'treatment': 'Apply systemic insecticides',
                'prevention': 'Encourage natural predators, avoid over-fertilization'
            }
        ]
    }
    
    @staticmethod
    def get_pests_for_crop(crop_type):
        """Get all pests and diseases for a specific crop"""
        return PestDiseaseDatabase.PESTS_DISEASES.get(crop_type, [])
    
    @staticmethod
    def search_by_symptom(symptom_keyword):
        """Search pests/diseases by symptom"""
        results = []
        for crop_type, pests in PestDiseaseDatabase.PESTS_DISEASES.items():
            for pest in pests:
                if symptom_keyword.lower() in pest['symptoms'].lower():
                    results.append({
                        'crop': crop_type,
                        **pest
                    })
        return results
    
    @staticmethod
    def get_critical_threats():
        """Get all critical severity threats"""
        threats = []
        for crop_type, pests in PestDiseaseDatabase.PESTS_DISEASES.items():
            for pest in pests:
                if pest['severity'] == 'critical':
                    threats.append({
                        'crop': crop_type,
                        **pest
                    })
        return threats
    
    @staticmethod
    def get_prevention_tips(crop_type):
        """Get all prevention tips for a crop"""
        pests = PestDiseaseDatabase.get_pests_for_crop(crop_type)
        tips = set()
        for pest in pests:
            tips.add(pest['prevention'])
        return list(tips)
