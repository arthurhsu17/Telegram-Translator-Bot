import os
import telebot
from TranslatorApp import text_translate
from google.cloud import translate_v2
from json import JSONEncoder
import json

def to_json(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__)

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot("")
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r"google_api_keys.json"
print("Bot booting up...")


def detect_language(text):
    
    translate_client = translate_v2.Client()
    result = translate_client.detect_language(text)
    print("Language: {}".format(result["language"]))

def text_translate(text,target= "en"):
    translator = translate_v2.Client()
    output= translator.translate(text,target_language=target)
    language= detect_language(text)
    rout = 'Translation:\n\n' + output['translatedText']
    return rout

    

    

    
@bot.message_handler(commands=['translate'])
def translate_command(message): 
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('ENGLISH',))

    keyboard.row(telebot.types.InlineKeyboardButton('CHINESE'))

    bot.send_message(message.chat.id, 'Click on the language of choice:', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('ENGLISH', 'CHINESE')

    
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id, text='Answer accepted!')
    
    if call.data == 'CHINESE':
        answer = 'You chose Chinese'
    if call.data == 'ENGLISH':
        answer = 'You chose English'

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)






@bot.message_handler(func=lambda m: True)
def echo_all(message):  
    translated_message = text_translate(message.text)
    bot.reply_to(message, translated_message)
  
    

bot.polling(none_stop=True)
