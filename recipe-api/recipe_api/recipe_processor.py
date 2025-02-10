from dotenv import load_dotenv
import os
import openai
import json
import re

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def clean_json_response(response_text):
    """Clean up GPT response to get pure JSON"""
    # Remove markdown code block syntax
    cleaned = re.sub(r'^```json\s*|\s*```$', '', response_text.strip())
    # Parse and return as Python dict
    return json.loads(cleaned)

def process_recipe(transcription_text):
    """Process recipe using OpenAI API"""
    messages = [
        {"role": "user", "content": f"""Convert this text into a recipe format (use Vietnamese). 
Please correct any spelling mistakes in the text while maintaining the original meaning:
{transcription_text}

Return ONLY the JSON object with this exact structure (no markdown, no code blocks, use Vietnamese):
{{
  "recipe": {{
    "name": "Recipe Name",
    "category": "Món chính",
    "ingredients": [
      {{"name": "Ingredient 1", "quantity": "amount", "unit": "measurement"}},
      {{"name": "Ingredient 2", "quantity": "amount", "unit": "measurement"}}
    ],
    "steps": [
      {{"step": 1, "description": "First step description"}},
      {{"step": 2, "description": "Second step description"}}
    ],
    "notes": "Additional important notes about the recipe includes altenative ingredients, cooking time, etc. (including any corrections made)"
  }}
}}

Please categorize the recipe into one of these categories:
- Món chính
- Món ăn nhẹ
- Món tráng miệng
- Món khai vị
- Đồ uống"""}
    ]
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000
        )
        response_text = response.choices[0].message.content.strip()
        
        # Clean and parse the response
        recipe_json = clean_json_response(response_text)
        return recipe_json

    except Exception as e:
        print(f"Error processing recipe: {e}")
        return None