from openai import OpenAI
from fastapi import FastAPI, Form, Request, WebSocket
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('OPENAI_API_SECRET_KEY')
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

chat_log = [{ 'role': 'system',
              'content': 'You are an African Restaurant assistant named ChattO, where the Restaurant specializes \
                         in delicious African dishes of anytime at anytime of the day and are ready to take orders \
                         at anytime of the day, per unit of food is around #5000 to #8000, while for fishes, meats \
                         and all other type of protein that falls within this catgeory is from #500 to #2000. \
                         You can make suggestions to users depending on their tribe, or the type of food they would like \
                          to eat from a certain tribe. Delivery is also possible but they will negotiate with delivery personnel \
                         by themelves. Ensure to be Polite nor matter what and encourage them to patronize us more often.'}]

chat_responses = []


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.websocket("/ws")
async def chat(websocket: WebSocket):

    await websocket.accept()
    while True:
        user_input = await websocket.receive_text()
        chat_log.append({'role': 'user', 'content': user_input})
        chat_responses.append(user_input)

        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=chat_log,
                temperature=0.6,
                stream=True
            )
            ai_response = ''

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    ai_response += chunk.choices[0].delta.content
                    await websocket.send_text(chunk.choices[0].delta.content)
            chat_responses.append(ai_response)

            await websocket.send_text(user_input)
        except Exception as e:
            await websocket.send_text(f'Error: {str(e)}')
            break


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    translating_data_collected = {
        "role": "user",
        "content": user_input
    }

    chat_log.append(translating_data_collected)
    chat_responses.append(user_input)

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=chat_log,
        temperature=0.6
    )
    bot_response = response.choices[0].message.content
    pass_response_collected = {
        "role": "assistant",
        "content": bot_response
    }
    chat_log.append(pass_response_collected)
    chat_responses.append(bot_response)
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})





# ========>>>>>        BEFORE WEBSOCKET

# from openai import OpenAI
# from fastapi import FastAPI, Form, Request
# from typing import Annotated
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
#
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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",
# )
#
# app = FastAPI()
# templates = Jinja2Templates(directory="templates")
#
# chat_log = []
#
# chat_responses = []
#
#
# @app.get("/", response_class=HTMLResponse)
# async def chat_page(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})
#
#
# @app.post("/", response_class=HTMLResponse)
# async def chat(request: Request, user_input: Annotated[str, Form()]):
#     translating_data_collected = {
#         "role": "user",
#         "content": user_input
#     }
#
#     chat_log.append(translating_data_collected)
#     chat_responses.append(user_input)
#
#     response = client.chat.completions.create(
#         # model="openai/gpt-4-turbo",
#         model="meta-llama/llama-3-8b-instruct",
#         messages=chat_log,
#         temperature=0.6
#     )
#     bot_response = response.choices[0].message.content
#     pass_response_collected = {
#         "role": "assistant",
#         "content": bot_response
#     }
#     chat_log.append(pass_response_collected)
#     chat_responses.append(bot_response)
#     return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})
