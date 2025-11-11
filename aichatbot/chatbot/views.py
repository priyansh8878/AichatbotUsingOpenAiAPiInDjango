from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def home(request):
    return render(request, 'index.html')

def get_response(request):
    user_message = request.GET.get('message', '')  # Safely get message

    if not user_message:
        return JsonResponse({"reply": "Please enter a message."})

    # Get AI response
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4-turbo", "gpt-5" if enabled
            messages=[
                {"role": "system", "content": "You are a friendly AI chatbot that helps with general queries."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply})

    except Exception as e:
        return JsonResponse({"reply": f"Error: {str(e)}"})
