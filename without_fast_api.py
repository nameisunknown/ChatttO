from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

chat_log = []

while True:
    data_collected = input()
    if data_collected.lower() == 'stop':
        break

    translating_data_collected = {
        "role": "user",
        "content": data_collected
    }

    chat_log.append(translating_data_collected)

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=chat_log,
        temperature=0.6
    )
    bot_response = response.choices[0].message.content
    pass_response_collected = {
        "role": "assistant",
        "content": bot_response
    }
    chat_log.append(pass_response_collected)
    print(bot_response)
