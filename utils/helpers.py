"""
Helper utility functions for HackList
"""

import re
from urllib.parse import urlparse
from typing import Optional


def validate_url(url: str) -> bool:
    """Validate if a URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL"""
    try:
        return urlparse(url).netloc
    except:
        return None


def get_domain_icon(domain: str) -> str:
    """Get appropriate icon for domain"""
    domain_lower = domain.lower()
    
    if 'github.com' in domain_lower:
        return "🐙"
    elif 'owasp.org' in domain_lower:
        return "🛡️"
    elif 'hackthebox.com' in domain_lower:
        return "📦"
    elif 'tryhackme.com' in domain_lower:
        return "🎯"
    else:
        return "🔗"


def get_difficulty_color(difficulty: str) -> str:
    """Get color for difficulty level"""
    difficulty_lower = difficulty.lower()
    
    if 'beginner' in difficulty_lower:
        return "green"
    elif 'intermediate' in difficulty_lower:
        return "orange"
    elif 'advanced' in difficulty_lower:
        return "red"
    else:
        return "blue"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def clean_project_name(name: str) -> str:
    """Clean project name for display"""

    name = re.sub(r'^(GitHub -)', '', name)
    
    name = re.sub(r'[-_]', ' ', name)
    
    name = name.title()
    
    return name.strip()


def format_category_name(category: str) -> str:
    """Format category name for display"""

    category = category.replace('/', ' / ')
    
    words = category.split()
    formatted_words = []
    
    for word in words:
        if word.lower() in ['api', 'iot', 'ctf', 'owasp']:
            formatted_words.append(word.upper())
        else:
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words) 