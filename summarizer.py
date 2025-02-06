import google.generativeai as genai
from config import gemini_api_key

# configure Gemini API
genai.configure(api_key=gemini_api_key)

# define parameters
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.7,
        "max_output_tokens": 150,
    },
)

def summarize_messages(messages):
    if not messages:
        return "No new messages to summarize"
    
    # check data
    if isinstance(messages, str):
        import json
        try:
            messages = json.loads(messages)
        except json.JSONDecodeError:
            return "Error processing messages."
    
    if not isinstance(messages, list):
        return "Invalid message format."

    combined_messages = "\n".join(
        f"{m.get('author', 'Unknown')}: {m.get('message', '')}" for m in messages
    )
    prompt = f"Summarize the following YouTube live chat messages in short:\n\n{combined_messages}"
    
    try:
        response = model.start_chat().send_message(prompt)
        return response.text.strip() if response.text else "No summary generated."
    except Exception as e:
        return f"Error generating summary: {e}"