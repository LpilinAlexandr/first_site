import telebot

TOKEN = '1339324208:AAHNqGKWzfYYS0WKXA8_BwtJnm4eGsrdEhQ'
bot = telebot.TeleBot(TOKEN)
chat_id = 475997071


def send_message_in_telegram(message):
    bot.send_message(chat_id, message)
