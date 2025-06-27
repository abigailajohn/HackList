"""
Search Tool for Cybersecurity Projects
Uses Serper (Google Search API) to find relevant projects
"""

import re
from typing import List, Dict, Any
import requests
import os


class SearchTool:
    """Tool for searching cybersecurity projects using Serper API"""
    
    def __init__(self, max_results: int = 10, timeout: int = 30):
        self.max_results = max_results
        self.timeout = timeout
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.serper_url = "https://google.serper.dev/search"
    
    def search_projects(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """
        Search for cybersecurity projects based on query and category using Serper
        """
        if not self.serper_api_key:
            print("Serper API key not found. Set SERPER_API_KEY in your environment.")
            return []
        try:
            search_queries = self._format_search_queries(query, category)
            all_results = []
            for search_query in search_queries:
                try:
                    results = self._serper_search(search_query)
                    for result in results:
                        title = result.get('title', '')
                        url = result.get('link', '')
                        description = result.get('snippet', '')
                        project_info = {
                            'name': self._extract_project_name(title, url),
                            'url': url,
                            'description': self._clean_description(description),
                            'source': 'web_search',
                            'category': category or 'Unknown'
                        }
                        all_results.append(project_info)
                except Exception as e:
                    print(f"Error searching with query '{search_query}': {e}")
                    continue
            return all_results
        except Exception as e:
            print(f"Error in search_projects: {e}")
            return []
    
    def _serper_search(self, query: str) -> List[Dict[str, Any]]:
        """Call Serper API and return results"""
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": self.max_results
        }
        response = requests.post(self.serper_url, headers=headers, json=payload, timeout=self.timeout)
        if response.status_code != 200:
            raise Exception(f"Serper API error: {response.status_code} {response.text}")
        data = response.json()
        return data.get('organic', [])
    
    def _format_search_queries(self, query: str, category: str = None) -> List[str]:
        """Format search queries for better results"""
        base_queries = [
            f"{query} intentionally vulnerable site:github.com",
            f"{query} vulnerable application",
            f"{query} ctf challenges",
            f"{query} lab environment",
            f"{query} vulnerable lab site:github.com",
            f"{query} hands-on project",
            f"{query} practice environment",
            f"{query} vulnerable project site:owasp.org",
            f"{query} project site:owasp.org"
        ]
        return base_queries
    
    def _extract_project_name(self, title: str, url: str) -> str:
        """Extract project name from title or URL"""
       
        if 'github.com' in url:
            parts = url.split('/')
            if len(parts) >= 5:
                return parts[-1].replace('-', ' ').replace('_', ' ').title()
        
     
        title = re.sub(r'[-_]', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
       
        title = re.sub(r'^(GitHub - |GitLab - |Bitbucket - )', '', title)
        title = re.sub(r'\s*[-|]\s*.*$', '', title)
        
        return title[:100]  
    
    def _clean_description(self, description: str) -> str:
        """Clean and format description"""
        description = re.sub(r'\s+', ' ', description)
        description = description.strip()
        
        if len(description) > 200:
            description = description[:197] + "..."
        
        return description 