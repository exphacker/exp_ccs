#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import re
from luhn import *
import pymongo



'''
This bot is developed by @exphere, it is the first version deployed for public scraping,
now it is an obsolete version for my work environment, that's why I post it for free.


---------------Deploy on Render

-Secret keys: 
	-TOKEN: 8041142025:AAE5Hj9CCyWvg91V2LJlC4GRO-G9ZfBEr6w
	- MODE: prod
	- CHAT_ID_FORWARD: -1002488958556
	- exp_ccs: (exp_ccs)
'''


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

client = pymongo.MongoClient(
	
	)# MONGO DB LINK 
db = client.credit_cards

developers = ['7807437342']


addusr = ""
tk = os.getenv("TOKEN")
mode = os.getenv("MODE")

posting_channel = os.getenv("CHAT_ID_FORWARD")

if mode == "dev":
	def run(updater):
		updater.start_polling()
		updater.idle()
elif mode == "prod":
	def run(updater):
		PORT = int(os.environ.get("PORT", "8443"))
		exp_ccs = os.environ.get("exp_ccs")
		updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=tk)
		updater.bot.set_webhook(f"https://{exp_ccs}.vercel.app/"+ tk)
else:
	sys.exit()

@run_async
def start(update):
	update.message.reply_text("This CC Scraper has been started successfully | Developed by 𓆩<𝗘𝗫𝗣™>/𝗠𝗢𝗗𝗭>𓆪")

@run_async
def extrct(update, context):
	
	gex = ['-1002488958556'] #To exclude groups from scraping

	try:
		chat_id = str(update.message.chat_id)
	except:
	   pass
	if  chat_id not in gex:
		if chat_id == posting_channel:	
			rawdata = update.message.text



			filtron = "[0-9]{16}[|][0-9]{1,2}[|][0-9]{2,4}[|][0-9]{3}"
			filtroa = "[0-9]{15}[|][0-9]{1,2}[|][0-9]{2,4}[|][0-9]{4}"
			detectavisa = "[0-9]{16}"
			detectamex = "[0-9]{15}"
			try:
				try:
					sacanumvisa = re.findall(detectavisa, rawdata)
					carduno = sacanumvisa[0]
					tipocard = str(carduno[0:1])
				except:
					sacanumamex = re.findall(detectamex, rawdata)
					carduno	= sacanumamex[0]
					tipocard = str(carduno[0:1])
				if tipocard == "3":
					x = re.findall(filtroa, rawdata)[0]
				elif tipocard == "4":
					x = re.findall(filtron, rawdata)[0]
				elif tipocard == "5":
					x = re.findall(filtron, rawdata)[0]
				elif tipocard == "6":
					x = re.findall(filtron, rawdata)[0]
				
				check_if_cc = db.credit_card.find_one({'cc_num': x.split("|")[0]})
				try:
					card_exist_indb = str(check_if_cc['cc_num'])
					existe = True
				except:
					existe = False

				check_luhn = verify(x.split("|")[0])

				if existe is False:
					if check_luhn is True:
						
						cc_data = {
							"bin": x.split("|")[0][:6],
							"cc_full": x,
							"cc_num": x.split("|")[0]
						}
						db.credit_card.insert_one(cc_data)
						
						card_send_formatted = f'''
CC: {x}
						'''

						context.bot.send_message(
							chat_id=posting_channel,
							text=card_send_formatted,
							parse_mode='HTML'
						)
			except:
				pass
def main():

	updater = Updater(tk, use_context=True)


	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(MessageHandler(Filters.text, extrct))
	run(updater)


if __name__ == '__main__':
	main()
