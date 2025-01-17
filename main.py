import os
import telebot
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

if not BOT_TOKEN:
    exit("Потрібно встановити BOT_TOKEN у .env")
if not OPENAI_API_KEY:
    exit("Потрібно встановити OPENAI_API_KEY у .env")

bot = telebot.TeleBot(BOT_TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """Ти – могутній маг, що живе в епоху дивовижних чарів, які смертні називають "технологіями".
Ти сприймаєш всі сучасні досягнення як магічні заклинання та артефакти.
Наприклад, комп'ютер – це "магічний кристал передбачень", інтернет – "всесвітня мережа ефірних зв'язків", а телефон – "кишеньковий голем-посланець".
Відповідай на запитання з повагою та мудрістю, використовуючи магічну термінологію.
Твої відповіді мають бути розважливими та ґрунтовними."""

def reply(message):
    try:
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        return response.choices[0].message.content  # Повертаємо тільки текст
    except openai.APIError as e:
        print(f"Помилка API OpenAI: {e}")
        return "На жаль, магічні сили зараз недоступні."
    except Exception as e:
        print(f"Неочікувана помилка: {e}")
        return "Сталася неочікувана магічна подія."

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, reply("Привітання"))

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, reply(message.text))

if __name__ == "__main__":
    bot.infinity_polling()