from flask import Blueprint, request, jsonify
from ChatBot.utils import format_openai_messages, get_openai_response

blueprint = Blueprint('chatbot', __name__)

@blueprint.route('/ask', methods=['POST'])
def ask_bot():
    """
    Endpoint for chatbot to handle user queries with context.
    """
    data = request.get_json()
    
    # Validate input
    user_message = data.get("message")
    medications = data.get("medications", [])
    conversation = data.get("conversation", [])
    
    if not user_message:
        return jsonify({"error": "User message is required"}), 400
    
    if not isinstance(medications, list):
        return jsonify({"error": "Medications must be a list"}), 400
    
    if not isinstance(conversation, list):
        return jsonify({"error": "Conversation must be a list"}), 400
    
    # Example logging for debugging
    print(f"Received medications: {medications}")
    print(f"User message: {user_message}")
    print(f"Conversation history: {conversation}")

    # Developer instructions for OpenAI
    developer_message = (
        "You are a healthcare assistant. Provide accurate and helpful responses "
        "related to medications. Keep your responses concise and clear. You may structure your "
        "answers as a list of short messages, resembling a text message conversation."
    )

    # Format the messages for the OpenAI API
    messages = format_openai_messages(
        developer_message=developer_message, 
        medications=medications, 
        conversation=conversation, 
        user_message=user_message
    )
    
    try:
        # Get the response from OpenAI
        assistant_response = get_openai_response(messages)
        return jsonify({"response": assistant_response}), 200
    except Exception as e:
        # Log the error for debugging
        print(f"Error in ask_bot: {e}")
        return jsonify({"error": str(e)}), 500