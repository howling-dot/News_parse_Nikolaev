import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from covid import Covid
#import logging
#import config
from sqlighter import SQLighter
from aiogram import Bot, Dispatcher, executor, types

#bot
bot = telebot.AsyncTeleBot("678908061:AAE-kmyK2_l8vtfg0eO3YiNp94yuzQvqRa0")

# OWM
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('aaa6c5a66b270fe65e5a711ef37e7f63', config_dict)
mgr = owm.weather_manager()

@bot.message_handler(commands=['start'])
def handle_start(message):
	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	markup.row('/wheather','/covid_ua')
	bot.send_message(message.chat.id, "Your choose:", reply_markup=markup)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
	bot.send_message(message.chat.id, "Thanks", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=['covid_ua'])
def handle_stop(message):
	covid = Covid()
	covid.get_data()
	ua_cases = covid.get_status_by_country_name("ukraine")
	answer = ('В '+ ua_cases['country'] + ' всего подтвердженных случаев ' + str(ua_cases['confirmed']) + '. В данный момент болеют ' + str(ua_cases['active']) + '. Всего смертей ' + str(ua_cases['deaths']) + '. Уже выздоровили ' + str(ua_cases['recovered']) + '.')
	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['weather'])
def handle_weather(message):
	bot.send_message(message.chat.id, 'enter the your place')
	bot.register_next_step_handler(message, get_place);

def get_place(message):
	try:
		observation = mgr.weather_at_place(message.text)
		w = observation.weather
		answer = ('В городе ' + message.text + ' ' + w.detailed_status + '. Температура воздуха '+ str(round(w.temperature('celsius')['temp'])) + ' градусов цельсия\n')
		bot.send_message(message.chat.id, answer)
	except:
		bot.send_message(message.chat.id, 'Unable to find your place, to return click /weather and try again')

#инициализируем соединение с БД
db = SQLighter("db.db")

#активация подписки
@bot.message_handler(commands=["subscribe"])
async def subscribe(message: types.Message):
	if (not db.subscriber_exist(message.from_user.id)):
		db.add_subscriber(message.from_user.id)
	else:
		db.update_subscription(message.from_user.id, True)	

	await message.answer("вы успешно активировали подписку")

#отписка
@bot.message_handler(commands=['unsubscribe'])
async def unsubscribe(mesage: types.Message):
	if(db.subscriber_exist(message.from_user.id)):
		db.update_subscription(message.from_user.id, False)
	else:
		db.add_subscriber(message.from_user.id, False)
	await message.answer('вы успешно отписаны от рассылки')
#executor.start_polling(bot, skip_updates=True)
bot.polling(none_stop = True)
