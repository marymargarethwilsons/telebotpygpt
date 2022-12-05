import openai
import telebot
from telebot import types

bot = telebot.TeleBot("5728237905:AAGX5C5lPspLmRG4EGUOc_X0vn2JuyoD3m8")
openai.api_key = "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"

# Create a keyboard with a try_again button and a new_question button
keyboard = types.InlineKeyboardMarkup()
try_again_button = types.InlineKeyboardButton(text="Try again", callback_data="try_again")
new_question_button = types.InlineKeyboardButton(text="Add new question", callback_data="new_question")
keyboard.add(try_again_button)
keyboard.add(new_question_button)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello! I am a bot. What can I do for you?')

@bot.message_handler(content_types=['text'])
def reply(message):
    bot.send_chat_action(message.chat.id, "typing")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.text,
        max_tokens=3900,
        temperature=0.9,
        top_p=1
    )
    reply = response['choices'][0]['text']
    # Add the keyboard to the reply
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "try_again")
def try_again(call):
    bot.send_chat_action(call.message.chat.id, "typing")
    original_text = call.message.text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=original_text,
        max_tokens=4000,
        temperature=0.9,
        top_p=1
    )
    reply = response['choices'][0]['text']
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=reply,
                          reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "new_question")
def new_question(call):
    keyboard_removed = types.ReplyKeyboardRemove()
    bot.send_message(call.message.chat.id, "Input your new question", reply_markup=keyboard_removed)

print("Bot started")
bot.polling()
