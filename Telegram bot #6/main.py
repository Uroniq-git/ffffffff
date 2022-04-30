from aiohttp import TraceRequestEndParams
import config
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=["new_chat_members"])
async def mute(message: types.Message):
    txt = message.values
    new_member_id = txt["new_chat_member"]["id"]
    try: 
        new_member_username = txt["new_chat_member"]["username"]
    except:
        pass

    if(new_member_username):
        if(new_member_username in config.unmutedable):
            await bot.restrict_chat_member(message.chat.id, new_member_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        else:
            await bot.restrict_chat_member(message.chat.id, new_member_id, can_send_messages=False)
    else:
        await bot.restrict_chat_member(message.chat.id, new_member_id, can_send_messages=False)


@dp.message_handler(commands="unmute")
async def unmute(message: types.Message):
    msgText = message.text
    try:
        username = msgText.split(' ')[1].replace('@', '') 
    except:
        await message.answer("Ошибка, /unmute <username>")
    
    if(username):
        config.unmutedable.append(username)


@dp.message_handler(commands='permUnmute')
async def permunmute(message: types.Message):
    msgText = message.text
    try:
        username = msgText.split(' ')[1]
    except:
        await message.answer("Ошибка, /permUnmute <chatID>")

    if(username): 
        await bot.restrict_chat_member(message.chat.id, username, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True )
    
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)