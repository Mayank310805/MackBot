# if you don't use pipenv, uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import streamlit as st
import requests

# ----- UI Configuration -----
st.set_page_config(page_title="LangGraph AI Chatbot", layout="centered")

# ----- App Header -----
st.markdown("""
    <h1 style="text-align: center; color: #4CAF50;">🤖 LangGraph AI Chatbot</h1>
    <p style="text-align: center;">Create and interact with AI agents powered by Groq & OpenAI</p>
    <hr>
""", unsafe_allow_html=True)

# ----- System Prompt -----
st.subheader("🧠 Define your Agent's Behavior")
system_prompt = st.text_area("Enter System Prompt", height=100, placeholder="E.g. Act as a smart, friendly assistant...")

# ----- Model Selection -----
st.subheader("🧪 Model Settings")

col1, col2 = st.columns(2)
with col1:
    provider = st.radio("Model Provider", ("Groq", "OpenAI"))

with col2:
    if provider == "Groq":
        selected_model = st.selectbox("Groq Models", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    else:
        selected_model = st.selectbox("OpenAI Models", ["gpt-4o-mini"])

# ----- Web Search Toggle -----
st.subheader("🌐 Tools")
allow_web_search = st.checkbox("Allow Web Search", value=True)

# ----- Query Input -----
st.subheader("💬 Ask your Agent")
user_query = st.text_area("Your Message", height=150, placeholder="Ask anything...")

# ----- Send Button -----
API_URL = "http://127.0.0.1:9999/chat"
send_btn = st.button("🚀 Ask Agent")

# ----- Result Display -----
if send_btn:
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Thinking..."):
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }

            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    if isinstance(response_data, dict) and "error" in response_data:
                        st.error(response_data["error"])
                    else:
                        st.success("✅ Agent Response")
                        st.markdown(f"""<div style='background-color:#111827;padding:20px;border-radius:10px;color:white;'>
                        {response_data}
                        </div>""", unsafe_allow_html=True)
                else:
                    st.error("Something went wrong with the request.")
            except Exception as e:
                st.error(f"Error contacting the backend: {e}")

# ----- Footer -----
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Powered by LangGraph · Developed by Mayank</p>", unsafe_allow_html=True)
