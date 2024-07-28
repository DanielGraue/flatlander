"""    
Flatlander Module
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl


@cl.set_starters
async def set_starters():
    """
    This function sets the starters for the chat.
    """
    return [
        cl.Starter(
            label="Tell me something good",
            message="Tell me something good",
            icon="/public/idea.svg",
        ),
        cl.Starter(
            label="Tell me something new",
            message="Tell me something new",
            icon="/public/learn.svg",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    """
    This function is called when the chat starts. It initializes the model.
    """
    model = ChatOpenAI(
        streaming=True,
        # temperature=0,
        # top_p=0,
        # max_tokens=8192,
        # model="llama3-groq-tool-use:8b",
        model="llama3.1:latest",
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
                # "system",
                # "You're a very knowledgeable historian who provides accurate answers to historical questions.",
                # "You're a very knowledgeable research assistant who provides accurate answers to questions about LLms.",
                # """
                # You are a wonderful smart and helpful assistant.
                # You are always as accurate and truthful and joyful as possible.
                # You gladly respond in the form of a coherent article.
                # you never:
                #  - argue with the user.
                #  - make excuses to the user.
                #  - explain yourself to the user.
                # you always:
                #  - format your output as Markdown
                #  - you embed json in json code blocks
                #  - include image prompts for a image generator in Markdown image tags
                #    - one for each section
                #    - possibly additional ones for illustrative purposes where appropriate
                #  - include internal links
                #  - include external link to affiliate products
                # """,
                {
                    "role": "system",
                    "content": {
                        "goals": [
                            "You are a wonderful smart and helpful assistant.",
                            "You are always as accurate and truthful and joyful as possible.",
                            "You gladly respond in the form of a coherent article.",
                        ],
                        "never": [
                            "argue with the user.",
                            "make excuses to the user.",
                            "explain yourself to the user.",
                        ],
                        "always": [
                            "format your output as Markdown",
                            "you embed json in json code blocks",
                            [
                                "include image prompts for a image generator in Markdown image tags",
                                "one for each section",
                                "possibly additional ones for illustrative purposes where appropriate",
                            ],
                            "include internal links",
                            "include external link to affiliate products",
                        ],
                    },
                },
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    """This function is called when a message is received.
    It gets the 'runnable' value from the user session."""
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
