from pyowm import OWM
from pyowm.utils.config import get_default_config
from covid import Covid
import settings
from parse import ParsePN, ParseUkrNetMk
from sqlighter import SQLighter
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

# bot
bots = Bot(settings.bot_token)
loop = asyncio.get_event_loop()
bot = Dispatcher(bots, loop=loop)

# OWM
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(settings.owm_key, config_dict)
mgr = owm.weather_manager()

# Создаем классы
parse_pn = ParsePN()
parse_ukrnet = ParseUkrNetMk()

# инициализируем соединение с БД
db = SQLighter("db.db")


# States
class Form(StatesGroup):
    place = State()  # Will be represented in storage as 'Form:name'


#    age = State()  # Will be represented in storage as 'Form:age'
#    gender = State()  # Will be represented in storage as 'Form:gender'


# Обработка кнопки старт
@bot.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('/weather', '/weather2', '/covid_ua')
    markup.row('/subscribe', '/unsubscribe')
    markup.row('/stop')
    await message.answer("Your choose:", reply_markup=markup)


# Обработка кнопки стоп
@bot.message_handler(commands=['stop'])
async def handle_stop(message):
    await message.answer("Thanks", reply_markup=types.ReplyKeyboardRemove())


# Обработка кнопки covid_ua
@bot.message_handler(commands=['covid_ua'])
async def handle_stop(message: types.Message):
    covid = Covid()
    covid.get_data()
    ua_cases = covid.get_status_by_country_name("ukraine")
    answer = ('В ' + ua_cases['country'] + ' всего подтвердженных случаев ' + str(
        ua_cases['confirmed']) + '. В данный момент болеют ' + str(ua_cases['active']) + '. Всего смертей ' + str(
        ua_cases['deaths']) + '. Уже выздоровили ' + str(ua_cases['recovered']) + '.')
    await message.answer(answer)


# Обработка кнопки weather
@bot.message_handler(commands=['weather'])
async def handle_weather(message: types.Message):
    place = 'Николаев'
    try:
        observation = mgr.weather_at_place(place)
        w = observation.weather
        answer = ('В городе ' + place + ' ' + w.detailed_status + '. Температура воздуха ' + str(
            round(w.temperature('celsius')['temp'])) + ' градусов цельсия\n')
        await message.answer(answer)
    except:
        await message.answer('Unable to find your place, to return click /weather and try again')


@bot.message_handler(commands=['weather2'])
async def handle_weather2(message: types.Message):
    place = 'Николаев'
    print(place)
    if db.get_sity(message.from_user.id):
        place = db.get_sity(message.from_user.id)
    else:
        bots.send_message(message.from_user.id, 'Введите свой город:')
        plase = message.text
        if not db.subscriber_exist(message.from_user.id):
            db.add_subscriber(message.from_user.id)
        else:
            db.update_subscription(message.from_user.id, True)
        if db.add_sity(message.from_user.id, place)
    print(place)
    try:
        observation = mgr.weather_at_place(place)
        w = observation.weather
        answer = ('В городе ' + place + ' ' + w.detailed_status + '. Температура воздуха ' + str(
            round(w.temperature('celsius')['temp'])) + ' градусов цельсия\n')
        await message.answer(answer)
    except:
        await message.answer('Unable to find your place, to return click /weather and try again')


# активация подписки
@bot.message_handler(commands=["subscribe"])
async def subscribe(message: types.Message):
    if not db.subscriber_exist(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)

    await message.answer("вы успешно активировали подписку")


# отписка
@bot.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if db.subscriber_exist(message.from_user.id):
        db.update_subscription(message.from_user.id, False)
    else:
        db.add_subscriber(message.from_user.id, False)
    await message.answer('вы успешно отписаны от рассылки')


@bot.message_handler(commands=["geo"])
async def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.row(types.KeyboardButton(text="Отправить местоположение", request_location=True))
    await bots.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение",
                     reply_markup=keyboard)

import geocoder
@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        latlng = (message.location.latitude, message.location.longitude)
        g = geocoder.reverse(latlng)
        print(g)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        new_newspn = parse_pn.parse_news()
        new_newsukrnet = parse_ukrnet.parse_news()
        if new_newspn:
            subscriptions = db.get_subscription()
            for i in subscriptions:
                await bots.send_message(i[1], new_newspn, disable_notification=True)
        if new_newsukrnet:
            subscriptions = db.get_subscription()
            for i in subscriptions:
                await bots.send_message(i[1], new_newsukrnet, disable_notification=True)


if __name__ == '__main__':
    bot.loop.create_task(scheduled(10))  # пока что оставим 10 секунд (в качестве теста)
    executor.start_polling(bot, skip_updates=True)
