from aiogram.types import Message
from dispatcher import dis


@dis.message_handler(commands=['start'])
async def send_welcome(msg: Message):
    user_id = str(msg.from_user.id)
    await msg.answer('Hi')
