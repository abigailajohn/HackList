# 🛡️ HackList

![HackList Banner](images/HackList.png)

> **Your AI-powered guide to hands-on cybersecurity learning!**

---

## 🚀 Features

- 🤖 **AI-Powered Recommendations**: Understands your interests and finds relevant projects.
- 🔍 **Multi-Source Search**: Searches GitHub, OWASP, blogs, and more.
- 📚 **Preloaded Dataset**: Curated cybersecurity projects for instant results.
- 🏷️ **Smart Categorization**: Automatically sorts projects by security domain.
- 🧹 **Duplicate Filtering**: Removes duplicates and irrelevant results.
- 🖥️ **User-Friendly Interface**: Streamlit web app for easy use.

---

## ⚡ Quickstart

### 🖥️ Local Installation

```bash
git clone <repository-url>
cd HackList
pip install -r requirements.txt
cp .env_example.txt .env
# Edit .env and add your OpenAI API key
streamlit run app.py
```

### 🐳 Docker

```bash
docker build -t hacklist .
docker run -p 8501:8501 --env OPENAI_API_KEY=<your_openai_api_key> hacklist
# Or with a .env file:
docker run -p 8501:8501 --env-file .env hacklist
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🖼️ Gallery

| ![Input Example](images/image1.png) | ![Output Example 1](images/image2.png) | ![Output Example 2](images/image3.png) |
|:---:|:---:|:---:|
| _Describe your interest_ | _Get project recommendations_ | _Explore project details_ |

---

## 🗂️ Project Structure

```
cybersec_projects_recommender/
├── app.py                 # Streamlit web interface
├── agent/
│   ├── __init__.py
│   ├── core_agent.py      # Main AI agent logic
│   ├── search_tool.py     # DuckDuckGo search integration
│   ├── categorization.py  # Project categorization tools
│   └── filtering.py       # Result filtering and deduplication
├── data/
│   ├── projects_dataset.json  # Preloaded cybersecurity projects
│   └── categories.json        # Security domain categories
├── utils/
│   ├── __init__.py
│   └── helpers.py         # Utility functions
├── requirements.txt
└── README.md
```


## 🛡️ Supported Security Domains

- 🌐 Web/API Security
- 🔗 Web3 Security
- 📱 Mobile Security
- 📡 IoT Security
- ☁️ Cloud Security
- 🤖 AI Security
- 🕵️‍♂️ Reverse Engineering
- 🦠 Malware Analysis
- 🕵️ Digital Forensics
- 🎭 Social Engineering
- 🐳 Container & Kubernetes Security
- 🔄 DevSecOps
- 🚨 Incident Response
- 🧩 Threat Modeling
- And more!

## 🤝 Contributing

Feel free to contribute by:
- Adding new projects to the dataset
- Improving categorization logic
- Enhancing the search functionality
- Adding new security domains

## 📄 License

MIT License 