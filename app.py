import streamlit as st
import os
from main import load_config, analyze_and_generate_post, read_posts_from_file
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Discussion Post Generator",
    page_icon="💭",
    layout="wide"
)

# Load configuration
config = load_config()

def initialize_session_state():
    if 'model' not in st.session_state:
        st.session_state.model = config["ai_settings"]["model"]
    if 'temperature' not in st.session_state:
        st.session_state.temperature = config["ai_settings"]["temperature"]
    if 'max_tokens' not in st.session_state:
        st.session_state.max_tokens = config["ai_settings"]["max_tokens"]

initialize_session_state()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("openapi_key"))

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Model selection with friendly names and version values
    model_options = {
        "GPT-4O": "gpt-4o-2024-08-06",
        "GPT-4O Mini": "gpt-4o-mini-2024-07-18",
        "O1": "o1-2024-12-17",
        "O1 Mini": "o1-mini-2024-09-12",
        "O3 Mini": "o3-mini-2025-01-31",
        "GPT-4": "gpt-4",
        "GPT-4 Turbo": "gpt-4-turbo",
    }
    
    model_name = st.selectbox("Model", 
                             options=list(model_options.keys()),
                             index=0)
    model = model_options[model_name]
    
    # Temperature slider
    temperature = st.slider("Temperature", 
                          min_value=0.0,
                          max_value=2.0,
                          value=st.session_state.temperature,
                          step=0.1)
    
    # Max tokens slider
    max_tokens = st.slider("Max Tokens",
                          min_value=50,
                          max_value=4000,
                          value=st.session_state.max_tokens,
                          step=50)

# Main content
st.title("💭 AI Discussion Post Generator")

# Input area for discussion prompt
prompt = st.text_area("Discussion Theme/Question", 
                     height=100,
                     placeholder="Enter the discussion theme or question here...")

# Input area for existing posts
posts = st.text_area("Existing Discussion Posts",
                    height=200,
                    placeholder="Enter existing discussion posts here, one per line...")

if st.button("Generate Post", type="primary"):
    if not prompt:
        st.error("Please enter a discussion theme or question.")
    elif not posts:
        st.error("Please enter some existing discussion posts.")
    else:
        try:
            # Update config with current settings
            config["ai_settings"]["model"] = model
            config["ai_settings"]["temperature"] = temperature
            config["ai_settings"]["max_tokens"] = max_tokens
            
            with st.spinner("Generating post..."):
                posts_list = posts.split('\n')
                generated_post = analyze_and_generate_post(posts_list, prompt)
                
                st.success("Post generated successfully!")
                st.markdown("### Generated Post")
                st.markdown(generated_post)
                
                # Add copy button
                st.button("📋 Copy to clipboard", 
                         on_click=lambda: st.write(generated_post))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}") 