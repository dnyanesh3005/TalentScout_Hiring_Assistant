import gradio as gr
import google.generativeai as genai
import config

# ============================================================================
# INITIALIZE GOOGLE GEMINI CLIENT
# ============================================================================
genai.configure(api_key=config.GEMINI_API_KEY)

generation_config = genai.types.GenerationConfig(
    max_output_tokens=config.MAX_TOKENS,
    temperature=config.TEMPERATURE,
)

# Initialize the generative model with the system prompt
model = genai.GenerativeModel(
    model_name=config.MODEL,
    system_instruction=config.SYSTEM_PROMPT,
    generation_config=generation_config,
)

def respond(message, history):
    """
    Function to handle chatbot responses.
    Gradio passes `history` as a list of lists: [[user_msg_1, bot_msg_1], [user_msg_2, bot_msg_2], ...]
    """
    
    # Format history for Gemini
    gemini_history = []
    for user_msg, bot_msg in history:
        gemini_history.append({"role": "user", "parts": [user_msg]})
        gemini_history.append({"role": "model", "parts": [bot_msg]})
        
    try:
        # Start a chat session with the previous history
        chat = model.start_chat(history=gemini_history)
        # Send the current message
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"❌ Error processing request: {str(e)}"

# ============================================================================
# GRADIO INTERFACE SETUP
# ============================================================================

# Define custom CSS for a cleaner, modern look
custom_css = """
footer {display: none !important;} 
"""

with gr.Blocks(theme=gr.themes.Base(), css=custom_css) as demo:
    gr.Markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <h1>🎯 TalentScout Assistant</h1>
            <p style="font-size: 1.1rem; color: #64748b;">Intelligent Initial Candidate Screening for Technology Placements (Gradio Version)</p>
        </div>
        """
    )
    
    # Using Gradio's built-in ChatInterface for a seamless chat experience
    chat_interface = gr.ChatInterface(
        fn=respond,
        chatbot=gr.Chatbot(height=600, bubble_full_width=False),
        textbox=gr.Textbox(placeholder="Type your response here...", container=False, scale=7),
        examples=[
            "Hello! I am here for the interview.",
            "I'm a Senior DevOps Engineer with 5 years of experience.",
            "My tech stack includes Python, Docker, Kubernetes, and AWS."
        ],
    )

if __name__ == "__main__":
    print("Launching Gradio App...")
    # You can set share=True to create a public link
    demo.launch(share=False)
