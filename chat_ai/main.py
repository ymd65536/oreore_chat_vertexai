import chainlit as cl
import vertexai_chat as ver_chat


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content='メッセージを入力').send()


@cl.on_message
async def on_message(input_message):
    res = ver_chat.chat_model_response(input_message)
    await cl.Message(content=res).send()