import streamlit as st
from langchain.llms import OpenAI

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
# llm = OpenAI(openai_api_key)

st.title('Chatbot')
st.write('Type a message and press Enter to send')

with st.form('my_form'):
    text = st.text_area('Enter text:')
    submitted = st.form_submit_button('Send')

if submitted:
    # Call the LLM to generate a response
    response = llm(text)
    st.write(response)
    
from langchain.community.streamlit import StreamlitChatMessageHistory

# Create a message history instance
message_history = StreamlitChatMessageHistory(key="langchain_messages")

# Add the user's message to the history
message_history.add_message(text, role="user")

# Generate a response using the LLM and add it to the history
response = llm(text)
message_history.add_message(response, role="assistant")

