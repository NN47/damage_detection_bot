import os
from dotenv import load_dotenv
import telebot  

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Функция, обрабатывающая команду /start

@bot.message_handler(commands=["start"])

def start(m, res=False):

    bot.send_message(m.chat.id, 'Бот запущен. Начните общение с ним.')

# Получение сообщений от пользователя

@bot.message_handler(content_types=["text"])

def handle_text(message):

    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.send_message(message.chat.id, 'Фото получено')
    photo = message.photo
    print(photo)
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
      new_file.write(downloaded_file)
    CLIENT = InferenceHTTPClient(
          api_url="https://detect.roboflow.com",
          api_key="bpBEGQKQ0Xzm4n4L3VPs"
      )
    result = CLIENT.infer("image.jpg", model_id="etiquetado-de-danos/1")
    if result['predictions']:
        answer = "найден тип повреждения " + result['predictions'][0]['class'] + " с точностью: " + str(round((result['predictions'][0]['confidence']),2))
    else:
        answer = "повреждения не найдены"
    bot.send_message(message.chat.id, 'Результат: ' + answer)
# Запускаем бота


bot.polling(none_stop=True, interval=0)
