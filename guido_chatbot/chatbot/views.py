from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

  # Store API key in settings

def chatbot_view(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chatbot_response(request):
    user_input = request.POST.get('message')
    print("User Input:", user_input)  # Debug print

    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}])
        bot_reply = response.choices[0].message.content
        print("Bot Reply:", bot_reply)  # Debug print
    except Exception as e:
        print("Error:", e)  # Debug print
        bot_reply = "Sorry, I'm having trouble processing that right now."

    return JsonResponse({"response": bot_reply})
