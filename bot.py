import os
import random
import telebot

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан.")

bot = telebot.TeleBot(TOKEN)

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")


def send_random_image_to(message):
    supported = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    images = [
        f for f in os.listdir(IMAGES_DIR)
        if f.lower().endswith(supported)
    ]

    if not images:
        bot.reply_to(message, "Папка images пустая — добавь картинки!")
        return

    chosen = random.choice(images)
    path = os.path.join(IMAGES_DIR, chosen)

    try:
        with open(path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception:
        with open(path, "rb") as doc:
            bot.send_document(message.chat.id, doc)


@bot.message_handler(regexp=r"^/blyat(\s|$)")
def on_command(message):
    send_random_image_to(message)


@bot.message_handler(regexp=r"(?i)\bblyat\b")
def on_word(message):
    send_random_image_to(message)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling(allowed_updates=["message"])
