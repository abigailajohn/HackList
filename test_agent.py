"""
Test script for the Cybersecurity Projects Recommender AI Agent
"""

import os
from dotenv import load_dotenv
from agent import CyberSecProjectAgent

def test_agent():
    """Test the AI agent functionality"""
    
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        print("   You can still test with preloaded data only.")
        api_key = None
    
    # Initialize agent
    print("🤖 Initializing AI Agent...")
    agent = CyberSecProjectAgent(api_key)
    
    # Test categories
    print("\n📂 Available Categories:")
    categories = agent.get_categories()
    for i, category in enumerate(categories, 1):
        print(f"   {i}. {category}")
    
    # Test queries
    test_queries = [
        "I want to learn API security",
        "Show me web application security projects",
        "Help me practice network penetration testing",
        "I'm interested in mobile security",
        "Recommend cryptography learning projects"
    ]
    
    print(f"\n🧪 Testing {len(test_queries)} queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: {query} ---")
        
        try:
            result = agent.recommend_projects(query, max_results=3)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                category = result.get('category', 'Unknown')
                confidence = result.get('confidence', 0.0)
                projects_count = len(result.get('recommendations', []))
                
                print(f"✅ Category: {category} (Confidence: {confidence:.1%})")
                print(f"📚 Found {projects_count} projects")
                
                # Show first project
                projects = result.get('recommendations', [])
                if projects:
                    first_project = projects[0]
                    print(f"   🥇 {first_project.get('name', 'Unknown')}")
                    print(f"      {first_project.get('description', 'No description')[:100]}...")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    test_agent() 