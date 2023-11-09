import config
import asyncio
import logging
import sys
import utils
import time
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = config.BOT_TOKEN
dp = Dispatcher()
bot = Bot(TOKEN)
IP_ADDRESS = utils.get_external_ip()


class UserPassword(StatesGroup):
    password = State()


@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.set_state(UserPassword.password)
    await message.answer(text="Введіть пароль:")


@dp.message(UserPassword.password)
async def check_password(message: Message, state: FSMContext):
    if config.PASSWORD == message.text:
        config.USER_DICT[message.from_user.full_name] = message.chat.id
        await state.clear()
        await check_ip()
    else:
        await message.answer(text="Неправильний пароль.")
        await state.clear()


async def check_ip():
    global IP_ADDRESS
    while True:
        current_ip_address = utils.get_external_ip()
        if IP_ADDRESS != current_ip_address:
            IP_ADDRESS = current_ip_address
            for _, value in config.USER_DICT.items():
                await bot.send_message(chat_id=value, text=current_ip_address)
        time.sleep(1)


async def main() -> None:
    bot_1 = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot_1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
