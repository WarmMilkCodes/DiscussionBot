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

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Create New Post", "Respond to Post"])

# Move existing main content into first tab
with tab1:
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

# Add new tab for responses
with tab2:
    st.title("💬 Discussion Response Generator")
    
    original_post = st.text_area(
        "Original Discussion Post",
        height=200,
        placeholder="Paste the discussion post you want to respond to..."
    )
    
    response_prompt = st.text_input(
        "Additional Instructions (Optional)",
        placeholder="E.g., 'Include a personal experience' or 'Focus on theoretical aspects'"
    )
    
    if st.button("Generate Response", type="primary"):
        if not original_post:
            st.error("Please enter the original discussion post.")
        else:
            try:
                with st.spinner("Generating response..."):
                    response_prompt_template = f"""
                    Create a thoughtful response to this discussion post. The response should:
                    - Show understanding of the original post
                    - Add meaningful insights
                    - Be engaging and professional
                    - Include relevant examples or evidence
                    {f'Additional instructions: {response_prompt}' if response_prompt else ''}
                    
                    Original post:
                    {original_post}
                    """
                    
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "user", "content": response_prompt_template}
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    generated_response = response.choices[0].message.content
                    
                    st.success("Response generated successfully!")
                    st.markdown("### Generated Response")
                    st.markdown(generated_response)
                    
                    # Add copy button
                    st.button("📋 Copy to clipboard", 
                             on_click=lambda: st.write(generated_response),
                             key="copy_response")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")