import streamlit as st
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from openai import OpenAI

#client = OpenAI(
#  base_url = "https://integrate.api.nvidia.com/v1",
#  api_key = "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"
#)

st.title("Agent financier")

# Set OpenAI API key from Streamlit secrets
#client=ChatNVIDIA(api_key="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",model="meta/llama3-70b-instruct")
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
from langchain_nvidia_ai_endpoints import ChatNVIDIA

#model = ChatNVIDIA(model="nvidia/nemotron-4-340b-instruct")
client = ChatNVIDIA(
  model="nvidia/nemotron-4-340b-instruct",
  api_key="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", 
  temperature=0.9,
  top_p=0.7,
  max_tokens=1024,
)


#if "nvidia_model" not in st.session_state:
    #st.session_state["nvidia_model"] = "meta/llama3-70b-instruct"
 #   st.session_state["nvidia_model"] = "nvidia/nemotron-4-340b-instruct"


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