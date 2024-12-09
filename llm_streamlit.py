
import streamlit as st
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from openai import OpenAI
# Prompt the user for their API key
api_key = st.text_input("Enter your NVIDIA API key", type="password")
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  
  api_key=api_key
)

st.title("Agent financier")






if "nvidia_model" not in st.session_state:
    
    st.session_state["nvidia_model"] = "nvidia/nemotron-4-340b-instruct"


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        #stream=client.stream([{"role":"user","content":"Write a limerick about the wonders of GPU computing."}])
        stream = client.chat.completions.create(
            model=st.session_state["nvidia_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
