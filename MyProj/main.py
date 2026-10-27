import os
from dotenv import load_dotenv
from gigachat import GigaChat
from prompts import SYSTEM_PROMPT
from gigachat.models import ChatCompletionRequest, ChatMessage

load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")
scope = os.getenv("GIGACHAT_SCOPE")

default_question = "Составьте маршрут для путешествия из Москвы на Байкал продолжительностью 7 дней с бюджетом до 50 000 рублей. Интересы — активный туризм."
print(f"Запрос по умолчанию: {default_question}")
user_input = input("Нажмите Enter для отправки или введите свой вопрос: ").strip()

question = user_input if user_input else default_question

request = ChatCompletionRequest(
    messages=[
        ChatMessage(
            role="system",
            content=SYSTEM_PROMPT,
        ),
        ChatMessage(
            role="user",
            content=question,
        )
    ]
)

print("Отправляем запрос. . . .")
with GigaChat(
    credentials=key,
    scope=scope,
    model="Gigachat-2",
    ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
    timeout=60,
) as client:
    response = client.chat.create(request)

answer = response.messages[0].content[0].text
print("Ответ:")
print(answer)

while True:
    question = input("\nВаш вопрос (или 'выход'): ")
    if question.lower() in ["выход", "exit", "quit"]:
        break
    if not question.strip():
        continue
        
    request.messages.append(ChatMessage(role="user", content=question))
    print("Отправляем запрос. . .")
    
    with GigaChat(
        credentials=key,
        scope=scope,
        model="Gigachat-2",
        ca_bundle_file="certs/russian_trusted_root_ca_pem.crt",
        timeout=60,
    ) as client:
        response = client.chat.create(request)
        answer = response.messages[0].content[0].text
        print(f"Ответ:\n{answer}")
        request.messages.append(ChatMessage(role="assistant", content=answer))
