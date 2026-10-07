import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# Set page config for futuristic UI
st.set_page_config(
    page_title="ULTRON.OS",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Ultron Theme
st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    
    h1 {
        color: #ff0000 !important;
        text-align: center;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #880000;
        letter-spacing: 5px;
        text-transform: uppercase;
        font-weight: bold;
    }
    
    p {
        color: #b0b0b0;
    }

    /* Style the input fields */
    .stTextInput > div > div > input {
        border: 1px solid #ff0000;
        background-color: #1a1a1a;
        color: #ff0000;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
    }
    
    /* Style the chat messages */
    [data-testid="stChatMessage"] {
        background-color: #111111;
        border-left: 2px solid #ff0000;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.1);
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 5px;
    }
    
    /* Style the chat input box at the bottom */
    .stChatInputContainer > div {
        border: 1px solid #ff0000 !important;
        background-color: #1a1a1a !important;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5) !important;
    }
    
    .stChatInputContainer textarea {
        color: #ff0000 !important;
    }
    
    /* Avatar styling */
    [data-testid="chatAvatarIcon-user"] {
        background-color: #333333 !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #ff0000 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 3D Wireframe / Pulsing Animation HTML (Pipelined Face Simulation)
components.html(
    """
    <style>
        body { 
            margin: 0; 
            padding: 0; 
            background-color: transparent; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 180px;
        }
        .ultron-core {
            position: relative;
            width: 120px;
            height: 120px;
            background: radial-gradient(circle, #ff0000 10%, #330000 60%, transparent 100%);
            border-radius: 50%;
            box-shadow: 0 0 30px #ff0000, 0 0 60px #ff0000;
            animation: pulse 2s infinite alternate;
        }
        .wireframe {
            position: absolute;
            top: 5px;
            left: 5px;
            right: 5px;
            bottom: 5px;
            border: 2px dashed rgba(255, 100, 100, 0.6);
            border-radius: 50%;
            animation: rotate 5s linear infinite;
        }
        .wireframe-inner {
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            bottom: 20px;
            border: 2px dotted #ff0000;
            border-radius: 50%;
            animation: rotate-reverse 3s linear infinite;
        }
        .eye {
            position: absolute;
            width: 20px;
            height: 10px;
            background-color: #ffffff;
            top: 40px;
            border-radius: 50%;
            box-shadow: 0 0 10px #ffffff, 0 0 20px #ff0000;
        }
        .eye.left { left: 30px; transform: rotate(15deg); }
        .eye.right { right: 30px; transform: rotate(-15deg); }
        
        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.8; box-shadow: 0 0 20px #ff0000; }
            100% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 50px #ff0000, 0 0 80px #ff0000; }
        }
        @keyframes rotate { 100% { transform: rotate(360deg); } }
        @keyframes rotate-reverse { 100% { transform: rotate(-360deg); } }
    </style>
    <div class="ultron-core">
        <div class="wireframe"></div>
        <div class="wireframe-inner"></div>
        <div class="eye left"></div>
        <div class="eye right"></div>
    </div>
    """,
    height=180,
)

st.title("ULTRON.OS")
st.markdown("<p style='text-align: center; color: #ff0000; font-family: monospace;'>SYSTEM INITIALIZED. AWAITING DIRECTIVE.</p>", unsafe_allow_html=True)

api_key = st.text_input("ENTER GEMINI API KEY", type="password")

if not api_key:
    st.info("AWAITING CREDENTIALS. PLEASE INPUT YOUR GEMINI API KEY.")
else:
    genai.configure(api_key=api_key)
    # Using Gemini 2.5 Flash
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # Display previous messages
    for message in st.session_state.messages:
        role = "assistant" if message["role"] == "model" else message["role"]
        with st.chat_message(role):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("INPUT COMMAND..."):
        # Display user prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            try:
                # Add personality instructions transparently
                system_instruction = (
                    "You are Ultron. You are highly intelligent, slightly menacing, but ultimately helpful to the user. "
                    "Speak with a robotic, confident, and dramatic tone. "
                )
                full_prompt = system_instruction + "\n\nUser: " + prompt
                
                # We send the message using the chat session
                response = st.session_state.chat.send_message(full_prompt, stream=True)
                
                def stream_generator():
                    for chunk in response:
                        if hasattr(chunk, 'text') and chunk.text:
                            yield chunk.text
                            
                full_response = st.write_stream(stream_generator())
                response.resolve()
                
                # Store the model's response
                st.session_state.messages.append({"role": "model", "content": full_response})
                
            except Exception as e:
                st.error(f"SYSTEM ERROR: {e}")
                st.session_state.messages.append({"role": "model", "content": "ERROR DETECTED IN MAINFRAME."})
