import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content='メッセージを入力').send()


@cl.on_message
async def on_message(input_message):
    print(input_message)
    await cl.Message(content='Hello').send()
