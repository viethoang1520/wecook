# WeCook 🍽️  
A smart cooking assistant that suggests recipes based on video input.

## 🚀 Features
- Ingredient-based recipe suggestions
- AI-powered recipe generator
- Step-by-step cooking guidance

## 🛠️ Tech Stack
- **Backend**: Django, MongoDB, HuggingFace AI, OpenAI API, JavaScript, Python
- **Frontend**: ReactJS, Ant Design, JavaScript

## 📦 Installation
```bash
# Clone the repo
git clone https://github.com/viethoang1520/wecook.git
cd wecook

# Install dependencies
cd recipe-api && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
cd recipe-admin && npm install

# Run the application
python manage.py runserver