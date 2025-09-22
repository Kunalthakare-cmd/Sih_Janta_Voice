# utils/nlp_analysis.py

import re
import json
from datetime import datetime, timedelta
from collections import Counter

class ComplaintAnalyzer:
    """
    Advanced NLP analyzer for complaint classification and routing
    """
    
    def __init__(self):
        self.department_keywords = {
            'roads': {
                'primary': ['road', 'street', 'highway', 'sadak', 'rasta'],
                'secondary': ['pothole', 'traffic', 'signal', 'zebra crossing', 'gaddha', 
                           'traffic light', 'divider', 'footpath', 'bridge', 'construction',
                           'repair', 'barricade', 'speed breaker', 'manhole', 'accident']
            },
            'water': {
                'primary': ['water', 'pani', 'pipe', 'tap'],
                'secondary': ['leak', 'drainage', 'sewer', 'nali', 'pipeline', 'supply',
                           'shortage', 'contamination', 'quality', 'bore well', 'tank',
                           'overflow', 'blockage', 'meter', 'pressure', 'dirty water']
            },
            'electricity': {
                'primary': ['light', 'power', 'electricity', 'bijli', 'current'],
                'secondary': ['pole', 'wire', 'transformer', 'outage', 'cable', 'meter',
                           'bill', 'connection', 'voltage', 'streetlight', 'bulb', 
                           'short circuit', 'power cut', 'load shedding']
            },
            'sanitation': {
                'primary': ['garbage', 'waste', 'toilet', 'kachra', 'safai'],
                'secondary': ['cleanliness', 'dustbin', 'sweeping', 'collection', 'disposal',
                           'sewage', 'smell', 'dirty', 'hygiene', 'public toilet', 
                           'drain cleaning', 'litter', 'stray animals']
            },
            'health': {
                'primary': ['hospital', 'doctor', 'health', 'aspatal', 'dawai'],
                'secondary': ['medicine', 'clinic', 'medical', 'emergency', 'ambulance',
                           'treatment', 'vaccination', 'disease', 'infection', 'pharmacy',
                           'patient', 'nurse', 'covid', 'fever', 'dengue']
            },
            'police': {
                'primary': ['police', 'crime', 'theft', 'chori', 'security'],
                'secondary': ['robbery', 'harassment', 'violence', 'accident', 
                           'traffic violation', 'noise', 'disturbance', 'illegal',
                           'drugs', 'fight', 'ladai', 'dispute', 'complaint']
            },
            'education': {
                'primary': ['school', 'education', 'vidyalaya', 'shiksha'],
                'secondary': ['teacher', 'student', 'college', 'classroom', 'books',
                           'fees', 'admission', 'exam', 'playground', 'uniform',
                           'transportation', 'bus', 'infrastructure', 'library']
            },
            'women-child': {
                'primary': ['women', 'child', 'harassment', 'safety', 'abuse'],
                'secondary': ['molestation', 'eve teasing', 'domestic violence', 'dowry',
                           'child labor', 'missing person', 'kidnapping', 'stalking',
                           'women safety', 'child safety', 'gender', 'female']
            }
        }
        
        self.urgency_patterns = {
            'high': {
                'keywords': ['emergency', 'urgent', 'immediately', 'danger', 'accident', 
                           'fire', 'flood', 'turant', 'khatre', 'jaldi', 'abhi', 'serious', 
                           'critical', 'life threatening', 'help', 'rescue', 'ambulance',
                           'police', 'died', 'injured', 'bleeding', 'unconscious'],
                'patterns': [r'\b(urgent|emergency|immediate|critical)\b', 
                           r'\b(help|rescue|save)\b', r'\b(died|death|injured)\b']
            },
            'medium': {
                'keywords': ['soon', 'quickly', 'problem', 'issue', 'samasya', 
                           'inconvenience', 'difficulty', 'concern', 'repair needed',
                           'broken', 'not working', 'damaged', 'complaint'],
                'patterns': [r'\b(problem|issue|broken|not working)\b',
                           r'\b(repair|fix|solve)\b']
            },
            'low': {
                'keywords': ['when possible', 'convenience', 'eventually', 'jab samay mile',
                           'suggestion', 'improvement', 'request', 'minor', 'small',
                           'sometime', 'later', 'future'],
                'patterns': [r'\b(suggestion|improvement|minor|small)\b',
                           r'\b(when possible|eventually|sometime)\b']
            }
        }
        
        self.location_priorities = {
            'critical': ['hospital', 'school', 'police station', 'fire station', 
                        'aspatal', 'vidyalaya'],
            'high': ['market', 'main road', 'station', 'mall', 'office', 
                    'government building', 'bank'],
            'medium': ['residential', 'colony', 'society', 'apartment', 'building'],
            'low': ['rural', 'outskirts', 'village', 'gaon']
        }
    
    def preprocess_text(self, text):
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Handle common abbreviations and misspellings
        replacements = {
            'rd': 'road', 'st': 'street', 'govt': 'government',
            'phn': 'phone', 'elec': 'electricity', 'hosp': 'hospital'
        }
        
        for abbr, full in replacements.items():
            text = re.sub(rf'\b{abbr}\b', full, text)
        
        return text
    
    def calculate_department_score(self, text, department_data):
        """Calculate department relevance score"""
        score = 0
        matched_keywords = []
        
        # Primary keywords (higher weight)
        for keyword in department_data['primary']:
            if keyword in text:
                score += 3
                matched_keywords.append(keyword)
        
        # Secondary keywords (lower weight)
        for keyword in department_data['secondary']:
            if keyword in text:
                score += 1
                matched_keywords.append(keyword)
        
        return score, matched_keywords
    
    def determine_urgency(self, text):
        """Determine urgency level with confidence score"""
        text = self.preprocess_text(text)
        urgency_scores = {'high': 0, 'medium': 0, 'low': 0}
        matched_patterns = []
        
        for level, data in self.urgency_patterns.items():
            # Keyword matching
            for keyword in data['keywords']:
                if keyword in text:
                    urgency_scores[level] += 1
            
            # Pattern matching
            for pattern in data['patterns']:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    urgency_scores[level] += 2
                    matched_patterns.extend(matches)
        
        # Determine final urgency
        if urgency_scores['high'] > 0:
            urgency = 'high'
        elif urgency_scores['low'] > urgency_scores['medium'] and urgency_scores['low'] > 0:
            urgency = 'low'
        else:
            urgency = 'medium'
        
        confidence = min(urgency_scores[urgency] / 5, 1.0)  # Normalize to 0-1
        
        return urgency, confidence, matched_patterns
    
    def analyze_location_priority(self, location):
        """Analyze location to determine priority level"""
        if not location:
            return 'medium', []
        
        location_lower = location.lower()
        matched_areas = []
        
        for priority, areas in self.location_priorities.items():
            for area in areas:
                if area in location_lower:
                    matched_areas.append(area)
                    return priority, matched_areas
        
        return 'medium', []
    
    def classify_complaint(self, complaint_text, location="", additional_context=None):
        """
        Main function to classify complaint and determine routing
        """
        if not complaint_text:
            return self._default_classification()
        
        text = self.preprocess_text(complaint_text)
        
        # Calculate department scores
        department_scores = {}
        all_matched_keywords = {}
        
        for dept, keywords in self.department_keywords.items():
            score, keywords_matched = self.calculate_department_score(text, keywords)
            if score > 0:
                department_scores[dept] = score
                all_matched_keywords[dept] = keywords_matched
        
        # Determine primary department
        if department_scores:
            primary_dept = max(department_scores, key=department_scores.get)
            confidence = min(department_scores[primary_dept] / 10, 1.0)
        else:
            primary_dept = 'general'
            confidence = 0.3
        
        # Determine urgency
        urgency, urgency_confidence, urgency_patterns = self.determine_urgency(text)
        
        # Analyze location priority
        location_priority, location_areas = self.analyze_location_priority(location)
        
        # Adjust urgency based on location
        if location_priority == 'critical' and urgency == 'medium':
            urgency = 'high'
            urgency_confidence = min(urgency_confidence + 0.3, 1.0)
        
        # Estimate resolution time
        resolution_time = self._get_resolution_time(primary_dept, urgency, location_priority)
        
        # Determine secondary departments if needed
        secondary_depts = []
        if len(department_scores) > 1:
            sorted_depts = sorted(department_scores.items(), key=lambda x: x[1], reverse=True)
            secondary_depts = [dept for dept, score in sorted_depts[1:3]]  # Top 2 alternatives
        
        return {
            'department': primary_dept,
            'secondary_departments': secondary_depts,
            'urgency': urgency,
            'confidence': confidence,
            'urgency_confidence': urgency_confidence,
            'keywords': all_matched_keywords.get(primary_dept, []),
            'urgency_indicators': urgency_patterns,
            'location_priority': location_priority,
            'location_areas': location_areas,
            'estimated_resolution': resolution_time,
            'analysis_metadata': {
                'text_length': len(complaint_text),
                'has_location': bool(location),
                'department_scores': department_scores,
                'processed_text_length': len(text),
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
    
    def _get_resolution_time(self, department, urgency, location_priority):
        """Calculate estimated resolution time"""
        base_times = {
            'high': {'min': 2, 'max': 4, 'unit': 'hours'},
            'medium': {'min': 1, 'max': 3, 'unit': 'days'},
            'low': {'min': 3, 'max': 7, 'unit': 'days'}
        }
        
        # Adjust based on department
        dept_multipliers = {
            'police': 0.5,  # Faster response
            'health': 0.6,  # Medical emergencies
            'women-child': 0.3,  # Highest priority
            'electricity': 1.2,  # Slightly longer
            'water': 1.1,
            'roads': 1.5,  # Infrastructure takes longer
            'sanitation': 1.3,
            'education': 2.0,  # Non-urgent typically
            'general': 1.4
        }
        
        base = base_times[urgency]
        multiplier = dept_multipliers.get(department, 1.0)
        
        # Adjust for location priority
        if location_priority == 'critical':
            multiplier *= 0.7
        elif location_priority == 'high':
            multiplier *= 0.8
        
        min_time = max(1, int(base['min'] * multiplier))
        max_time = int(base['max'] * multiplier)
        
        if base['unit'] == 'hours':
            return f"{min_time}-{max_time} hours"
        else:
            return f"{min_time}-{max_time} days"
    
    def _default_classification(self):
        """Return default classification for empty/invalid input"""
        return {
            'department': 'general',
            'secondary_departments': [],
            'urgency': 'medium',
            'confidence': 0.3,
            'urgency_confidence': 0.3,
            'keywords': [],
            'urgency_indicators': [],
            'location_priority': 'medium',
            'location_areas': [],
            'estimated_resolution': '2-5 days',
            'analysis_metadata': {
                'text_length': 0,
                'has_location': False,
                'department_scores': {},
                'processed_text_length': 0,
                'analysis_timestamp': datetime.now().isoformat(),
                'error': 'No complaint text provided'
            }
        }

# Global analyzer instance
complaint_analyzer = ComplaintAnalyzer()

def analyze_complaint_text(complaint_text, location="", additional_context=None):
    """
    Wrapper function for easy import and use
    """
    return complaint_analyzer.classify_complaint(complaint_text, location, additional_context)

def get_department_statistics(complaints_list):
    """
    Generate statistics from a list of analyzed complaints
    """
    if not complaints_list:
        return {}
    
    departments = [c.get('department', 'general') for c in complaints_list]
    urgencies = [c.get('urgency', 'medium') for c in complaints_list]
    
    stats = {
        'total_complaints': len(complaints_list),
        'department_distribution': dict(Counter(departments)),
        'urgency_distribution': dict(Counter(urgencies)),
        'average_confidence': sum(c.get('confidence', 0) for c in complaints_list) / len(complaints_list),
        'high_priority_count': sum(1 for c in complaints_list if c.get('urgency') == 'high'),
        'location_based_priority': sum(1 for c in complaints_list if c.get('location_priority') in ['critical', 'high'])
    }
    
    return stats