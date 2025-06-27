"""
HackList - Streamlit Web Application
"""

import streamlit as st
import os
import json
from dotenv import load_dotenv
from agent import CyberSecProjectAgent
from utils.helpers import (
    validate_url, extract_domain, get_domain_icon,
    get_difficulty_color, truncate_text, clean_project_name, format_category_name
)

load_dotenv()

st.set_page_config(
    page_title="HackList",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .project-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .category-badge {
        background-color: #007bff;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.25rem;
    }
    .difficulty-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.25rem;
    }
    .confidence-meter {
        background-color: #e9ecef;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #0084ff; 
        color: white;
    }
    .stButton > button:hover {
        background-color: #006fd6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    """Initialize the AI agent with caching"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return None
    
    try:
        return CyberSecProjectAgent(api_key)
    except Exception as e:
        st.error(f"Error initializing agent: {e}")
        return None

def main():
    """Main application function"""
    
    st.markdown('<h1 class="main-header">🛡️HackList</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered recommendations for hands-on cybersecurity learning</p>', unsafe_allow_html=True)
    
    agent = initialize_agent()
    if not agent:
        st.stop()
    
    with st.sidebar:
        st.header("🔧 Settings")
        
        st.subheader("Browse by Category")
        categories = agent.get_categories()
        selected_category = st.selectbox(
            "Choose a security domain:",
            ["All Categories"] + categories,
            index=0
        )
        
        if selected_category != "All Categories":
            if st.button(f"Browse {selected_category} Projects"):
                st.session_state.browse_category = selected_category
        
        st.divider()
        
        st.subheader("Search Settings")
        max_results = st.slider("Max Results", 3, 15, 8)
        enable_web_search = st.checkbox("Enable Web Search", value=True)
        
        os.environ['ENABLE_WEB_SEARCH'] = str(enable_web_search).lower()
        
        st.divider()
        
        st.subheader("ℹ️ About")
        st.markdown("""
        This AI agent helps you find hands-on cybersecurity projects based on your learning interests.
        
        **Features:**
        - 🤖 AI-powered recommendations
        - 🔍 Multi-source search
        - 📚 Preloaded curated projects
        - 🏷️ Smart categorization
        - 🎯 Personalized results
        """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if 'browse_category' in st.session_state:
            st.subheader(f"📂 {format_category_name(st.session_state.browse_category)} Projects")
            
            with st.spinner("Searching for projects..."):
                result = agent.search_by_category(st.session_state.browse_category, max_results)
            
            if 'error' in result:
                st.error(result['error'])
            else:
                display_results(result)
            
            if st.button("← Back to Search"):
                del st.session_state.browse_category
                st.rerun()
        
        else:
            st.subheader("🔍 What do you want to learn?")
            
            st.markdown("Try these examples:")

            example_queries = [
                "Show me web security projects",
                "I'm interested in mobile security"
            ]

            for i, query in enumerate(example_queries):
                if st.button(query, key=f"example_{i}"):
                    st.session_state.user_input = query

           
            user_input = st.text_input(
                "Describe your learning interest:",
                value=st.session_state.get('user_input', ''),
                placeholder="e.g., I want to learn API security"
            )

          
            if st.button("🚀 Get Recommendations"):
                if user_input.strip():
                    with st.spinner("🤖 AI is finding the perfect projects for you..."):
                        result = agent.recommend_projects(user_input, max_results)
                    if 'error' in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        display_results(result)
                else:
                    st.warning("Please enter your learning interest.")

def display_results(result):
    """Display search results"""
    
    category = result.get('category', 'Unknown')
    confidence = result.get('confidence', 0.0)
    
    st.markdown(f"### Detected Category: {format_category_name(category)}")
    
    if confidence > 0:
        st.markdown(f"**Confidence:** {confidence:.1%}")
        st.progress(confidence)
    
    category_desc = result.get('category_description', '')
    if category_desc:
        st.info(f"💡 {category_desc}")
    
    ai_summary = result.get('ai_summary', '')
    if ai_summary:
        st.markdown("### 🤖 AI Summary")
        st.markdown(ai_summary)
    
    projects = result.get('recommendations', [])
    if projects:
        st.markdown(f"### 📚 Found {len(projects)} Projects")
        
        for i, project in enumerate(projects, 1):
            with st.container():
                st.markdown(f"#### {i}. {clean_project_name(project.get('name', 'Unknown Project'))}")
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    url = project.get('url', '')
                    if url and validate_url(url):
                        domain = extract_domain(url)
                        icon = get_domain_icon(domain) if domain else "🔗"
                        st.markdown(f"{icon} [View Project]({url})")
                
                with col2:
                    project_category = project.get('category', 'Unknown')
                    st.markdown(f'<span class="category-badge">{project_category}</span>', unsafe_allow_html=True)
                
                with col3:
                    difficulty = project.get('difficulty', '')
                    if difficulty:
                        color = get_difficulty_color(difficulty)
                        st.markdown(f'<span class="difficulty-badge" style="background-color: {color}; color: white;">{difficulty}</span>', unsafe_allow_html=True)
                
                description = project.get('description', 'No description available')
                st.markdown(f"**Description:** {description}")
                
                tags = project.get('tags', [])
                if tags:
                    tag_text = " ".join([f"`{tag}`" for tag in tags[:5]])  # Limit to 5 tags
                    st.markdown(f"**Tags:** {tag_text}")
                
                st.divider()
    
    else:
        st.warning("No projects found. Try broadening your search terms or check the related categories below.")
    
    related_categories = result.get('related_categories', [])
    if related_categories:
        st.markdown("### 🔗 Related Categories")
        for related_cat in related_categories:
            if st.button(f"Browse {format_category_name(related_cat)}", key=f"related_{related_cat}"):
                st.session_state.browse_category = related_cat
                st.rerun()
    
    suggestions = result.get('search_suggestions', [])
    if suggestions:
        st.markdown("### 💡 Try These Search Terms")
        for suggestion in suggestions[:2]: 
            if st.button(suggestion, key=f"suggestion_{suggestion}"):
                st.session_state.user_input = suggestion
                st.rerun()

if __name__ == "__main__":
    main() 