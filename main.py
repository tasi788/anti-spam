__author__      = '@DingChen-Tsai'

import time
import telepot
from configparser import SafeConfigParser

#定義telegram各項參數
def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	chat_id = msg['chat']['id']
	message_id = msg['message_id']
	user_id = msg['from']['id']
	try:
		username = msg['from']['first_name'] +' '+ msg['from']['last_name']
	except:
		username = msg['from']['first_name']
	if content_type == 'new_chat_member':
		with open('fuckdict.txt') as f:
			fuckname = f.read().replace('\n', '').split(',')
		for x in fuckname:
			if x in username:
				tmp = f'Banned\n' \
				f'name: {username}\n' \
				f'uid: {user_id}'

				bot.sendMessage(-1001229303409, tmp)
				bot.kickChatMember(chat_id, user_id, until_date=int(time.time()))
				bot.deleteMessage((chat_id, message_id))
				print(tmp)
				break

#登入資訊
parser = SafeConfigParser()
parser.read('apitoken.txt')
owner = parser.get('apitoken','owner')
bot_apitoken = parser.get('apitoken', 'token')
bot = telepot.Bot(bot_apitoken)
bot.sendMessage(int(owner),'運轉中!')
bot.message_loop(handle)
print ('監聽中 ...')

while 1:
	time.sleep(10)
