from telegram import Update
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler, CallbackContext)
from ChatGPT_HKBU import HKBU_ChatGPT

import redis
import configparser
import logging

global redis1
def main():
	config = configparser.ConfigParser()
	config.read('config.ini')
	updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
	dispatcher = updater.dispatcher
	global redis1
	redis1 = redis.Redis(host=(config['REDIS']['HOST']),password=(config['REDIS']['PASSWORD']),port=(config['REDIS']['REDISPORT']))

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

	global chatgpt
	chatgpt = HKBU_ChatGPT(config)
	chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
	dispatcher.add_handler(chatgpt_handler)

	dispatcher.add_handler(CommandHandler("add", add))
	dispatcher.add_handler(CommandHandler("help", help_command))
	dispatcher.add_handler(CommandHandler("hello", hello))	

	updater.start_polling()
	updater.idle()

def echo(update, context):
	reply_message = update.message.text.upper()
	logging.info("Update: " + str(update))
	logging.info("context: " + str(context))
	context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text('Helping you helping you.')

def add(update:Update, context:CallbackContext) -> None:
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0]
		redis1.incr(msg)

		update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')

	except (IndexError, ValueError):
		update.message.reply_text('Usage: /add <keyword>')

def hello(update:Update, context:CallbackContext) -> None:
        try:
                global redis1
                logging.info(context.args[0])
                name = context.args[0]
                redis1.incr(name)

                update.message.reply_text('Good day,  ' + name + ' !')

        except (IndexError, ValueError):
                update.message.reply_text('Usage: /add <keyword>')

def equiped_chatgpt(update, context):
	global chatgpt
	reply_message = chatgpt.submit(update.message.text)
	logging.info("Update: " + str(update))
	logging.info("context: " + str(context))
	context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)



if __name__ == '__main__':
	main()
