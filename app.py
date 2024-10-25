import telebot
from g4f.client import Client

# Ваш токен Telegram бота
API_TOKEN = '6800*****54:AA**XrjDb6**dKw**LoDE_YHs5g**VLDUkk'

#  экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# экземпляр клиента ChatGPT
client = Client()

# Словарь для хранения истории сообщений
user_context = {}

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_message = message.text

    # Инициализируем контекст для пользователя, если его нет
    if user_id not in user_context:
        user_context[user_id] = []

    # Добавляем сообщение пользователя в контекст
    user_context[user_id].append({"role": "user", "content": user_message})

    # Отправляем сообщение о том, что бот обрабатывает запрос
    typing_message = bot.reply_to(message, "Подождите, я обрабатываю ваш запрос...")

    try:
        # Получаем ответ от ChatGPT
        response = client.chat.completions.create(
            model="gpt-4",
            messages=user_context[user_id]
        )

        # Извлекаем содержимое ответа
        chat_response = response.choices[0].message.content

        # Удаляем сообщение об обработке
        bot.delete_message(message.chat.id, typing_message.message_id)

        # Отправляем ответ пользователю
        bot.reply_to(message, chat_response)

        # Добавляем ответ ChatGPT в контекст
        user_context[user_id].append({"role": "assistant", "content": chat_response})

    except Exception as e:
        # Удаляем сообщение об обработке
        bot.delete_message(message.chat.id, typing_message.message_id)

        # В случае ошибки отправляем сообщение об ошибке
        bot.reply_to(message, "Произошла ошибка при обработке вашего запроса.")
        print(f"Error: {e}")

# Запускаем бота
bot.polling(print('Bot started'))
