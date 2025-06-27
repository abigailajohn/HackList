"""
Filtering Tool for Cybersecurity Projects
Removes duplicates and filters irrelevant results
"""

import re
from typing import List, Dict, Any
from urllib.parse import urlparse, unquote


class FilteringTool:
    """Tool for filtering and cleaning project results"""
    
    def __init__(self):
        self.seen_urls = set()
        self.seen_names = set()
        
    def filter_results(self, results: List[Dict[str, Any]], max_results: int = 8) -> List[Dict[str, Any]]:
        """
        Filter and clean project results
        
        Args:
            results: List of project dictionaries
            max_results: Maximum number of results to return
            
        Returns:
            Filtered list of projects
        """
        if not results:
            return []
        
        unique_results = self._remove_duplicates(results)
        
        relevant_results = self._filter_by_relevance(unique_results)
        
        sorted_results = self._sort_by_quality(relevant_results)
        
        return sorted_results[:max_results]
    
    def _remove_duplicates(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate projects based on URL and name"""
        unique_results = []
        
        for result in results:
            url = result.get('url', '').strip()
            name = result.get('name', '').strip()
            
            if not url or not name:
                continue
            
            normalized_url = self._normalize_url(url)
            
            if self._is_duplicate(normalized_url, name):
                continue
            
            self.seen_urls.add(normalized_url)
            self.seen_names.add(name.lower())
            
            result['url'] = normalized_url
            unique_results.append(result)
        
        return unique_results
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for comparison"""
        try:
            parsed = urlparse(url)
            
            clean_path = parsed.path.rstrip('/')
            if parsed.fragment:
                clean_path = clean_path.split('#')[0]
            
            normalized = f"{parsed.scheme}://{parsed.netloc}{clean_path}"
            
            normalized = unquote(normalized)
            
            return normalized.lower()
        except:
            return url.lower()
    
    def _is_duplicate(self, url: str, name: str) -> bool:
        """Check if project is a duplicate"""
        if url in self.seen_urls:
            return True
        
        name_lower = name.lower()
        for seen_name in self.seen_names:
            if self._calculate_name_similarity(name_lower, seen_name) > 0.8:
                return True
        
        return False
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity between two project names"""
        if name1 == name2:
            return 1.0
        
        if name1 in name2 or name2 in name1:
            return 0.9
        
        from difflib import SequenceMatcher
        return SequenceMatcher(None, name1, name2).ratio()
    
    def _filter_by_relevance(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter results by relevance criteria"""
        relevant_results = []
        
        for result in results:
            if self._is_relevant_project(result):
                relevant_results.append(result)
        
        return relevant_results
    
    def _is_relevant_project(self, result: Dict[str, Any]) -> bool:
        """Check if project is relevant for learning"""
        name = result.get('name', '').lower()
        description = result.get('description', '').lower()
        url = result.get('url', '').lower()
        
        if len(name) < 3 or len(description) < 10:
            return False
        
        security_indicators = [
            'vulnerable', 'security project', 'hack', 'pentesting', 'insecure',
            'practice lab', 'deliberately', 'learning', 'training', 'ctf', 'challenge',
            'damn vulnerable', 'owasp', 'security testing', 'exploit', 'tool', 'forensics', 
            'web3', 'threat model', 'cloud', 'reverse engineering', 'code review', 'appsec', 
            'cloud', 'kubernetes', 'container', 'misconfiguration', 'cloud-native', 'devsecops', 
            'ai vulnerable lab', 'goat', 'hands-on', 'intentionally vulnerable'
        ]    

        text_to_check = f"{name} {description}"
        has_security_indicator = any(indicator in text_to_check for indicator in security_indicators)
        
        return has_security_indicator
    
    def _sort_by_quality(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort results by quality score"""
        for result in results:
            result['quality_score'] = self._calculate_quality_score(result)
        
        return sorted(results, key=lambda x: x.get('quality_score', 0), reverse=True)
    
    def _calculate_quality_score(self, result: Dict[str, Any]) -> float:
        """Calculate quality score for a project"""
        score = 0.0
        
        score += 1.0
        
        url = result.get('url', '').lower()
        if 'github.com' in url:
            score += 2.0
        elif 'owasp' in url:
            score += 1.5
        
        name = result.get('name', '')
        if len(name) > 5 and len(name) < 50:
            score += 0.5
        
        description = result.get('description', '')
        if len(description) > 20:
            score += 0.5
        if len(description) > 50:
            score += 0.5
        
        source = result.get('source', '')
        if source == 'preloaded':
            score += 1.0 
        
        return score
    
    def reset_filters(self):
        """Reset filter state (clear seen URLs and names)"""
        self.seen_urls.clear()
        self.seen_names.clear() 