import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.messages import HumanMessage, AIMessage

# Set up the OpenAI model
llm = ChatOpenAI(
    streaming=True,
    temperature=0,
    # model="phi3",
    # model="gemma2",
    model="llama3",
    openai_api_key="ollama",
    base_url="http://192.168.0.2:11434/v1",
)

# Set up memory
memory = ConversationBufferMemory(return_messages=True, output_key="output")

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant."),
        ("human", "{input}"),
        ("human", "Previous conversation:\n{history}\nHuman: {input}\nAI:"),
    ]
)

# Define the runnable chain
chain = (
    RunnablePassthrough.assign(
        history=memory.load_memory_variables | (lambda x: x["history"])
    )
    | prompt
    | llm
    | StrOutputParser()
)

# Streamlit UI
st.title("ChatGPT-like Interface with LangChain Runnables")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("human"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chain.invoke({"input": prompt})
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Update memory
    memory.save_context({"input": prompt}, {"output": response})

# Display memory contents (optional, for debugging)
with st.expander("Conversation Memory"):
    st.write(memory.load_memory_variables({}))
