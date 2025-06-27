"""
Categorization Tool for Cybersecurity Projects
Maps user interests to security domains and categories
"""

import json
import os
from typing import Dict, List, Tuple
from difflib import SequenceMatcher


class CategorizationTool:
    """Tool for categorizing cybersecurity interests and projects"""
    
    def __init__(self):
        self.categories = self._load_categories()
    
    def _load_categories(self) -> Dict:
        """Load categories from JSON file"""
        try:
            categories_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'categories.json')
            with open(categories_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('categories', {})
        except Exception as e:
            print(f"Error loading categories: {e}")
            return {}
    
    def categorize_interest(self, user_input: str) -> Tuple[str, float]:
        """
        Categorize user interest into security domain
        
        Args:
            user_input: User's learning interest (e.g., "I want to learn API security")
            
        Returns:
            Tuple of (category, confidence_score)
        """
        key_terms = self._extract_key_terms(user_input.lower())
        
        best_category = "Unknown"
        best_score = 0.0
        
        for category, category_info in self.categories.items():
            keywords = category_info.get('keywords', [])
            
            score = self._calculate_similarity_score(key_terms, keywords)
            
            if score > best_score:
                best_score = score
                best_category = category
        
        return best_category, best_score
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key security terms from text"""
        stop_words = {
            'i', 'want', 'to', 'learn', 'about', 'the', 'a', 'an', 'and', 'or', 'but',
            'in', 'on', 'at', 'for', 'with', 'by', 'from', 'up', 'down', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'between', 'among', 'within',
            'without', 'against', 'recommend', 'towards', 'upon', 'of', 'off', 'over', 'under',
            'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
            'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
            'can', 'will', 'just', 'should', 'now', 'this', 'that', 'these', 'those'
        }
        
        words = text.split()
        key_terms = [word for word in words if word.lower() not in stop_words and len(word) > 2]
        
        bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        trigrams = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
        
        return key_terms + bigrams + trigrams
    
    def _best_match_score(self, term: str, keywords: List[str]) -> float:
        """Find the best match score for a single term against all keywords."""
        scores = []
        for keyword in keywords:
            if term.lower() == keyword.lower():
                scores.append(1.0)
            elif term.lower() in keyword.lower() or keyword.lower() in term.lower():
                scores.append(0.8)
            else:
                scores.append(SequenceMatcher(None, term.lower(), keyword.lower()).ratio())
        return max(scores) if scores else 0.0
    
    def _calculate_similarity_score(self, key_terms: List[str], keywords: List[str]) -> float:
        """Calculate similarity score between key terms and category keywords"""
        if not key_terms or not keywords:
            return 0.0
        
        total_score = 0.0
        matches = 0
        
        for term in key_terms:
            best_match_score = self._best_match_score(term, keywords)
            if best_match_score > 0.3:
                total_score += best_match_score
                matches += 1
        
        return (total_score / len(key_terms)) if matches > 0 else 0.0
    
    def get_category_description(self, category: str) -> str:
        """Get description for a security category"""
        if category in self.categories:
            return self.categories[category].get('description', '')
        return ''
    
    def get_related_categories(self, category: str) -> List[str]:
        """Get related categories for a given category"""
        if category not in self.categories:
            return []
        
        relationships = {
            "Web Security":["API Security"],
            "API Security": ["Mobile Security"],
            "Mobile Security": ["Reverse Engineering"],
            "Cloud Security": ["Container & Kubernetes Security"],
            "Reverse Engineering": ["Malware Analysis", "Mobile Security"],
            "Malware Analysis": ["Reverse Engineering"],
            "Digital Forensics": ["Incident Response"],
            "Container & Kubernetes Security":[],
            "DevSecOps":["Container & Kubernetes Security"],
            "Incident Response":["Digital Forensics"],
            "Code Review":["API Security"]
        }
        
        return relationships.get(category, [])
    
    def suggest_search_terms(self, category: str) -> List[str]:
        """Suggest additional search terms for a category"""
        if category not in self.categories:
            return []
        
        keywords = self.categories[category].get('keywords', [])
        
        project_terms = [
            "hands-on", "project", "lab", "vulnerable", 
            "learning", "practice", "challenge", "ctf"
        ]
        
        suggestions = []
        for keyword in keywords[:5]: 
            for term in project_terms:
                suggestions.append(f"{keyword} {term}")
        
        return suggestions
    
    def get_all_categories(self) -> List[str]:
        """Get list of all available categories"""
        return list(self.categories.keys()) 