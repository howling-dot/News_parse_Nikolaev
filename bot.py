from pyowm import OWM
from pyowm.utils.config import get_default_config
from covid import Covid
import settings
from parse import ParsePN
from sqlighter import SQLighter
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio


#bot
bots = Bot(settings.bot_token)
loop = asyncio.get_event_loop()
bot = Dispatcher(bots, loop=loop)

# OWM
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(settings.owm_key, config_dict)
mgr = owm.weather_manager()

parse_pn = ParsePN()
# States
class Form(StatesGroup):
    place = State()  # Will be represented in storage as 'Form:name'
#    age = State()  # Will be represented in storage as 'Form:age'
#    gender = State()  # Will be represented in storage as 'Form:gender'

@bot.message_handler(commands=['start'])
async def handle_start(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	markup.row('/weather','/covid_ua')
	markup.row('/subscribe','/unsubscribe')
	markup.row('/stop')
	await message.answer("Your choose:", reply_markup=markup)

@bot.message_handler(commands=['stop'])
async def handle_stop(message):
	await message.answer("Thanks", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['covid_ua'])
async def handle_stop(message: types.Message):
	covid = Covid()
	covid.get_data()
	ua_cases = covid.get_status_by_country_name("ukraine")
	answer = ('В '+ ua_cases['country'] + ' всего подтвердженных случаев ' + str(ua_cases['confirmed']) + '. В данный момент болеют ' + str(ua_cases['active']) + '. Всего смертей ' + str(ua_cases['deaths']) + '. Уже выздоровили ' + str(ua_cases['recovered']) + '.')
	#bot.send_message(message.chat.id, answer)
	await message.answer(answer)

@bot.message_handler(commands=['weather'])
async def handle_weather(message: types.Message):
#	await message.answer('enter the your place')
	place = 'Николаев'
	try:
		observation = mgr.weather_at_place(place)
		w = observation.weather
		answer = ('В городе ' + place + ' ' + w.detailed_status + '. Температура воздуха '+ str(round(w.temperature('celsius')['temp'])) + ' градусов цельсия\n')
		await message.answer(answer)
	except:
		await message.answer('Unable to find your place, to return click /weather and try again')

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
async def unsubscribe(message: types.Message):
	if(db.subscriber_exist(message.from_user.id)):
		db.update_subscription(message.from_user.id, False)
	else:
		db.add_subscriber(message.from_user.id, False)
	await message.answer('вы успешно отписаны от рассылки')


async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		print('start')
		new_news = parse_pn.parse_news()
		if new_news:
			subscriptions = db.get_subscription()
			for i in subscriptions:
				await bots.send_message(i[1], new_news, disable_notification=True)
		print('stop')


if __name__ == '__main__':
	bot.loop.create_task(scheduled(1800)) # пока что оставим 10 секунд (в качестве теста)
	executor.start_polling(bot, skip_updates=True)
