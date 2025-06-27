"""
Core AI Agent for Cybersecurity Project Recommendations
Orchestrates search, categorization, and filtering tools
"""

import json
import os
from typing import List, Dict, Any, Tuple
from openai import OpenAI
from .search_tool import SearchTool
from .categorization import CategorizationTool
from .filtering import FilteringTool


class CyberSecProjectAgent:
    """Main AI Agent for recommending cybersecurity projects"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.search_tool = SearchTool()
        self.categorization_tool = CategorizationTool()
        self.filtering_tool = FilteringTool()
        self.preloaded_projects = self._load_preloaded_projects()
    
    def _load_preloaded_projects(self) -> List[Dict[str, Any]]:
        """Load preloaded cybersecurity projects"""
        try:
            projects_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'projects_dataset.json')
            with open(projects_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                projects = data.get('projects', [])
                
                for project in projects:
                    project['source'] = 'preloaded'
                
                return projects
        except Exception as e:
            print(f"Error loading preloaded projects: {e}")
            return []
    
    def recommend_projects(self, user_input: str, max_results: int = 8) -> Dict[str, Any]:
        """
        Main method to recommend cybersecurity projects
        
        Args:
            user_input: User's learning interest
            max_results: Maximum number of projects to return
            
        Returns:
            Dictionary with recommendations and metadata
        """
        try:
            category, confidence = self.categorization_tool.categorize_interest(user_input)
            if confidence < 0.5:
                category = "Unknown"
            
            preloaded_results = self._get_preloaded_projects(category, user_input)
            
            search_results = []
            if os.getenv('ENABLE_WEB_SEARCH', 'true').lower() == 'true':
                raw_search_results = self.search_tool.search_projects(user_input, category)
                search_results = self.filtering_tool.filter_results(raw_search_results, max_results)
            
            all_results = preloaded_results + search_results
            filtered_results = self.filtering_tool.filter_results(all_results, max_results)
            
            response = self._format_response(
                filtered_results, 
                user_input, 
                category, 
                confidence
            )
            return response
            
        except Exception as e:
            print(f"Error in recommend_projects: {e}")
            return {
                'error': str(e),
                'recommendations': [],
                'category': 'Unknown',
                'confidence': 0.0
            }
    
    def _get_preloaded_projects(self, category: str, user_input: str) -> List[Dict[str, Any]]:
        """Get relevant preloaded projects for the category using explicit category tags"""
        if not self.preloaded_projects or not category or category == "Unknown":
            return []
        
        relevant_projects = []
        for project in self.preloaded_projects:
            project_category = project.get('category', '')

            if isinstance(project_category, list):
                if category in project_category:
                    relevant_projects.append(project)

            elif isinstance(project_category, str):
                if category == project_category:
                    relevant_projects.append(project)
        return relevant_projects
    
    def _format_response(self, projects: List[Dict[str, Any]], user_input: str, 
                        category: str, confidence: float) -> Dict[str, Any]:
        """Format the response with recommendations and metadata"""
        
        markdown_recommendations = self._generate_markdown_recommendations(projects, category)
        
        ai_summary = self._generate_ai_summary(projects, user_input, category)
        
        response = {
            'recommendations': projects,
            'markdown': markdown_recommendations,
            'ai_summary': ai_summary,
            'category': category,
            'confidence': confidence,
            'category_description': self.categorization_tool.get_category_description(category),
            'related_categories': self.categorization_tool.get_related_categories(category),
            'search_suggestions': self.categorization_tool.suggest_search_terms(category),
            'total_found': len(projects)
        }
        
        return response
    
    def _generate_markdown_recommendations(self, projects: List[Dict[str, Any]], category: str) -> str:
        """Generate markdown formatted recommendations"""
        if not projects:
            return "No projects found for your interest. Try broadening your search terms."
        
        markdown = f"**Here are some {category} projects you can explore:**\n\n"
        
        for i, project in enumerate(projects, 1):
            name = project.get('name', 'Unknown Project')
            url = project.get('url', '#')
            description = project.get('description', 'No description available')
            difficulty = project.get('difficulty', '')
            
            difficulty_badge = f" ({difficulty})" if difficulty else ""
            
            markdown += f"{i}. **[{name}]({url})**{difficulty_badge}\n"
            markdown += f"   {description}\n\n"
        
        return markdown
    
    def _generate_ai_summary(self, projects: List[Dict[str, Any]], user_input: str, category: str) -> str:
        """Generate AI-powered summary of recommendations"""
        if not projects:
            return "I couldn't find any specific projects matching your interest. Consider trying different search terms or exploring related categories."
        
        try:
            project_summaries = []
            for project in projects[:5]: 
                summary = f"- {project.get('name', 'Unknown')}: {project.get('description', 'No description')}"
                project_summaries.append(summary)
            
            projects_text = "\n".join(project_summaries)
            
            prompt = f"""
            User is interested in learning about: "{user_input}"
            Category: {category}
            
            Here are some recommended projects:
            {projects_text}
            
            Please provide a brief, encouraging summary (2-3 sentences) explaining why these projects are good for learning {category}. 
            Focus on the learning value and practical skills they'll gain.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity education expert helping students find hands-on learning projects."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating AI summary: {e}")
            return f"Here are {len(projects)} {category} projects to help you learn and practice. Each project offers hands-on experience with real-world security concepts."
    
    def get_categories(self) -> List[str]:
        """Get all available security categories"""
        return self.categorization_tool.get_all_categories()
    
    def search_by_category(self, category: str, max_results: int = 8) -> Dict[str, Any]:
        """Search for projects in a specific category"""
        if category not in self.get_categories():
            return {
                'error': f'Unknown category: {category}',
                'recommendations': [],
                'category': category,
                'confidence': 0.0
            }
        
        preloaded_results = [p for p in self.preloaded_projects if p.get('category') == category]
        
        search_results = []
        if os.getenv('ENABLE_WEB_SEARCH', 'true').lower() == 'true':
            search_results = self.search_tool.search_projects(category, category)
        
        all_results = preloaded_results + search_results
        filtered_results = self.filtering_tool.filter_results(all_results, max_results)
        
        return self._format_response(
            filtered_results,
            f"learning {category}",
            category,
            1.0
        ) 