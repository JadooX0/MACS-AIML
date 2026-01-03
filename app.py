import streamlit as st
import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os


load_dotenv()


st.set_page_config(page_title="Event Planner Assistant", page_icon="Pg")
st.title(" AI Event Planner Assistant")
st.markdown("Upload an event poster and let's start planning!")


with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter API Key", type="password")
    uploaded_file = st.file_uploader("Upload Event Poster", type=["jpg", "jpeg", "png"])
    if st.button("Clear Chat History"):
        st.session_state.messages = []


if "messages" not in st.session_state:
    st.session_state.messages = []
if "event_details" not in st.session_state:
    st.session_state.event_details = None


def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

def get_assistant_response(user_query, image_base64=None):
    
    model = ChatOpenAI(api_key=api_key, model="gpt-4o-mini")
    
    
    content = [{"type": "text", "text": user_query}]
    if image_base64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
        })
    
    
    history = [SystemMessage(content="You are a helpful Event Planning Assistant.")]
    for msg in st.session_state.messages[-5:]: 
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(AIMessage(content=msg["content"]))
            
    history.append(HumanMessage(content=content))
    response = model.invoke(history)
    return response.content


if uploaded_file and not st.session_state.event_details:
    with st.spinner("Analyzing poster..."):
        base64_img = encode_image(uploaded_file)
        initial_prompt = "Analyze this poster and give me a brief summary of the event (Name, Date, Venue, Highlights)."
        analysis = get_assistant_response(initial_prompt, base64_img)
        st.session_state.event_details = analysis
        st.session_state.messages.append({"role": "assistant", "content": analysis})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask about the event..."):
    if not api_key:
        st.error("Please provide an API key in the sidebar.")
    else:
       
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_assistant_response(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})