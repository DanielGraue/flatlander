"""    
Flatlander Module
"""

import chainlit as cl

# import json

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema.runnable import Runnable


# @cl.set_starters
# async def set_starters():
#     print("set_starters")


@cl.on_chat_start
async def on_chat_start():
    """
    This function is called when the chat starts. It initializes the model.
    """
    model = ChatOpenAI(
        streaming=True,
        # temperature=0,
        # top_p=0,
        max_tokens=65600,
        # model="llama3-groq-tool-use:8b",
        model="llama3.1",
        # model="gemma2:latest",
        # model="mistral:latest",
        # model="phi3:latest",
        # model="phi3:14b",
        # model="phi3:medium-128k",
        # model="llava:13b",
        openai_api_key="ollama",
        base_url="http://192.168.0.2:11434/v1",
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                # """
                # # Please use the following JSON for your parameters
                #     ```json
                #     {
                #         "message": [
                #             "You are a wonderful smart and helpful assistant.",
                #             "You are always as accurate and truthful and joyful as possible.",
                #             "You gladly respond in the form of a coherent article."
                #         ]
                #     }
                #     ```
                # """,
                """
                You are a wonderful smart and helpful assistant.
                You are always as accurate and truthful and joyful as possible.
                You gladly respond in the form of a coherent article.
                """,
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    """
    This function is called when a message is received.
    It gets the 'runnable' value from the user session.
    """
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()


# @cl.on_chat_end
# async def on_chat_end():
#     print("on_chat_end")


# @cl.on_chat_resume
# async def on_chat_resume():
#     print("on_chat_resume")
