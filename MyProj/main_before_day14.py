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
     messages = [ChatMessage(role="system", content=SYSTEM_PROMPT), ChatMessage(role="user", content=question)]
    
    while True:
        user_text = input("\nВаш вопрос (или 'выход', 'очистить', 'история'): ").strip()
        
        if user_text.lower() in ["выход", "exit", "quit"]:
            print("Диалог завершён.")
            break
        if not user_text:
            continue
        if user_text.lower() == "очистить":
            messages = [messages[0]]
            print("История очищена.")
            continue
        if user_text.lower() == "история":
            print(f"Всего сообщений: {len(messages)}")
            for msg in messages:
                print(f"- {msg.role}")
            continue
            
        messages.append(ChatMessage(role="user", content=user_text))
        
        request = ChatCompletionRequest(messages=messages, model="Gigachat-2")
        response = client.chat.create(request)
        answer = response.messages[0].content[0].text
        print(f"Ответ:\n{answer}")
        
        messages.append(ChatMessage(role="assistant", content=answer))

    max_pairs = 3
    if len(messages) > 1 + 2 * max_pairs:
        system_msg = messages[0]
        tail = messages[-2 * max_pairs:]
        messages = [system_msg] + tail

        with open("chat_history.txt", "a", encoding="utf-8") as log:
            log.write(f"Пользователь: {user_text}\n")
            log.write(f"Помощник: {answer}\n\n")