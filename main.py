
import logging
import os

from moviepy.editor import *

from aiogram.dispatcher.filters import state
from pytube import YouTube

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = 'YOUR TOKEN HERE'

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


name = ''

def get_audio(url):
	YouTube(url).streams.first().download(filename=f'{YouTube(url).title}.mp4')
	mvideo = VideoFileClip(f'{YouTube(url).title}.mp4')
	audio = mvideo.audio
	audio.write_audiofile(f'{YouTube(url).title}.mp3')


class YTFSM(StatesGroup):
	url = State()
	process = State()

@dp.message_handler(commands=['podcast'])
async def cmd_start(message: types.Message):
	await YTFSM.url.set()

	await message.reply("Give me url to get audio from.")

@dp.message_handler(state=YTFSM.url)
async def get_url(message: types.Message):


	data = message.text
	name = message.text
	get_audio(data)
	print(data)


	await bot.send_audio(message.from_user.id, audio=open(f'{YouTube(data).title}.mp3', 'rb'))

@dp.message_handler(state=YTFSM.process)
async def processing(message: types.Message):

	await bot.send_audio(message.from_user.id, audio=open(f'{YouTube(name).title}.mp3', 'rb'))




if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
