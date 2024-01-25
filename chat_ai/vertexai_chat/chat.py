import os
import vertexai
from vertexai.language_models import ChatModel
from vertexai.language_models import InputOutputTextPair


def chat_model_response(input_text):

    LOCALTION = os.getenv("LOCALTION")
    MODEL_NAME = "chat-bison@001"

    vertexai.init(location=LOCALTION)
    chat_model = ChatModel.from_pretrained(MODEL_NAME)
    chat = chat_model.start_chat(
        context="あなたは文章をきれいにまとめることができるアシスタントです。入力された文章を要約してください。",
        examples=[
            InputOutputTextPair(
                input_text="Your name",
                output_text="Kento.Yamada@ymd65536",
            )
        ],
        temperature=0.3,
    )

    response = chat.send_message(input_text)

    return response.text
