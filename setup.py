"""
Setup script for Cybersecurity Projects Recommender
"""

import os
import sys
import subprocess
import json

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    print("🔧 Creating .env file...")
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
MAX_SEARCH_RESULTS=10
MAX_PROJECTS_RETURNED=8
SEARCH_TIMEOUT=30

# Optional: Custom search settings
USE_PRELOADED_DATA=true
ENABLE_WEB_SEARCH=true
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please edit .env and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        import openai
        import pandas
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_basic_test():
    """Run basic functionality test"""
    print("🧪 Running basic functionality test...")
    
    try:
        from agent import CyberSecProjectAgent
        agent = CyberSecProjectAgent()
        
        # Test categories
        categories = agent.get_categories()
        if categories:
            print(f"✅ Found {len(categories)} security categories")
        else:
            print("❌ No categories found")
            return False
        
        # Test preloaded data
        if hasattr(agent, 'preloaded_projects') and agent.preloaded_projects:
            print(f"✅ Loaded {len(agent.preloaded_projects)} preloaded projects")
        else:
            print("❌ No preloaded projects found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🛡️ Cybersecurity Projects Recommender Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Run basic test
    if not run_basic_test():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: streamlit run app.py")
    print("3. Open http://localhost:8501 in your browser")
    print("\n💡 Optional: Run 'python test_agent.py' to test the agent")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 