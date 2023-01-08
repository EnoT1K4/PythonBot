import logging
from random import random, randint
from aiogram import Bot, Dispatcher, executor, types
import config as cfg
from db import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
db = Database('Database.db')


@dp.message_handler(commands=['id'], commands_prefix='/')
async def id(message: types.Message):
    await bot.send_message(message.chat.id,
                           f'Your ID:{message.from_user.id}, {str(db.name(message.from_user.id)[0][0])}')


@dp.message_handler(commands=['about'], commands_prefix='/')
async def about(message: types.Message):
    await bot.send_message(message.chat.id, """Используй /id чтобы узнать свой id \n
Используй /nickname "пробел" твой ник, чтобы добавить никнейм \n
Используй /cube чтобы бросить игральный кубик \n
Используй /admins чтобы узнать кто админы
     """)


@dp.message_handler(content_types=["new_chat_members"])
async def new_member(message: types.Message):
    name = message.new_chat_members[0].first_name
    id = message.new_chat_members[0].id
    db.add_nick(id,name)
    await bot.send_message(message.chat.id, f"Добро пожаловать, @{name}!")
    await bot.send_message(message.chat.id, """Используй /about чтобы узнать возможноcти бота """)
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.first_name)


@dp.message_handler(commands=['mute'], commands_prefix='/')
async def add_mute(message: types.Message):
    if message.from_user.id in cfg.ADMINS_ID:
        if not message.reply_to_message:
            await message.reply('Эта команда является ответом на сообщение')
            return
        if len(message.text) > 6:
            if int(message.text[6:]):
                mute_sec = int(message.text[6:])
                db.add_mute(message.reply_to_message.from_user.id, mute_sec)
                await message.bot.delete_message(cfg.CHAT_ID, message.reply_to_message.message_id)
                await message.bot.send_message(message.chat.id, f'You in mute for {mute_sec} sec. Shut Up, {str(db.name(message.reply_to_message.from_user.id)[0][0])}!')
        else:
            if len(message.text) <= 6:
                mute_sec = 30
                db.add_mute(message.reply_to_message.from_user.id, mute_sec)
                await message.bot.delete_message(cfg.CHAT_ID, message.reply_to_message.message_id)
                await message.bot.send_message(message.chat.id,
                                               f'You in mute for {mute_sec} sec. Shut Up, {str(db.name(message.reply_to_message.from_user.id)[0][0])}!')


# admin_add
@dp.message_handler(commands=['admin'], commands_prefix='/')
async def add_admin(message: types.Message):
    if str(message.from_user.id) == cfg.ADMIN_ID:
        if not message.reply_to_message:
            await message.reply('Nope')
            return
        db.add_admin(message.reply_to_message.from_user.id)
        await message.bot.send_message(message.chat.id, f'You are Admin, {message.reply_to_message.from_user.first_name}')
        await bot.send_message(message.chat.id, """Отправь мне свою ссылку на ВК,  чтобы к тебе могли обращаться""")
    else:
        await message.bot.send_message(message.chat.id, 'You are not Admin')


@dp.message_handler(commands=['nickname'], commands_prefix='/')
async def add_nick(message: types.Message):
    nickname = message.text[10:]
    db.add_nick(message.from_user.id, nickname)
    db.change_name()
    await bot.send_message(message.chat.id, f'Твой ник теперь {str(db.name(message.from_user.id)[0][0])}')


@dp.message_handler(commands=['admins'], commands_prefix='/')
async def who_ad(message: types.Message):
    strok = ''
    for i in range(len(db.get_users())):
        for j in range(len(db.get_link())):
            if db.get_link()[j][0] == db.get_users()[i][0]:
                if db.get_link()[j][1] not in strok:
                    strok += db.get_link()[j][1]
                    strok += '\n'
    await bot.send_message(message.chat.id, f'Your admins are {strok}')


@dp.message_handler()
async def message1(message: types.Message):
    if db.mute(message.from_user.id):
        await message.bot.delete_message(cfg.CHAT_ID, message.message_id)
    elif 'https://' in message.text:
        if 'https://vk.com/' in message.text and message.from_user.id in db.get_admID():
            db.add_link(message.from_user.id, message.text)
    else:
        return


@dp.message_handler(commands=['cube'], commands_prefix='/')
async def cube(message: types.Message):
    await bot.send_message(message.reply_to_message.message_id, f'{randint(1,6)}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
