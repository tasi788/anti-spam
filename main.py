__author__ = '@DingChen-Tsai'

import time
import telepot
from pprint import pprint as pp
from configparser import SafeConfigParser


# 定義telegram各項參數
def handle(msg):
	#pp(msg)
	content_type, chat_type, chat_id, msg_date, message_id = telepot.glance(
		msg, long=True)
	user_id = msg['from']['id']
	botId = bot_apitoken.split(':')[0]
	fuckchannel = -1001229303409
	username = msg['from']['first_name']
	if 'last_name' in msg['from'].keys():
		username += ' ' + msg['from']['last_name']
	if content_type == 'new_chat_member':
		gId = msg['chat']['id']
		gName = msg['chat']['title']
		if msg['new_chat_member']['id'] == botId:
			tmp = 'Invited\n' \
				'group name: {gName}\n' \
				'group id: {gId}\n' \
				'Invited by\n' \
				'username: {username}\n' \
				'uid: {user_id}'.format(
					gName=gName,
					gId=gId,
					username=username,
					user_id=user_id
				)
			print(tmp)
			bot.sendMessage(fuckchannel, tmp)

		with open('fuckdict.txt') as f:
			fuckname = f.read().replace('\n', '').split(',')
		for x in fuckname:
			if x in username:
				tmp = 'Banned\n' \
					'group id: {gId}\n' \
					'group name: {gName}\n' \
					'name: {username}\n' \
					'uid: {user_id}\n'.format(
						gId=gId,
						gName=gName,
						username=username,
						user_id=user_id
					)
				bot.sendMessage(fuckchannel, tmp)
				try:
					bot.kickChatMember(
						chat_id, user_id)
					bot.deleteMessage((chat_id, message_id))
					print(tmp)
					break
				except telepot.exception.TelegramError as e:
					tmp = '失敗惹 QQ\n' \
						'group id: {gId}\n' \
						'group name: {gName}\n' \
						'name: {username}\n' \
						'uid: {user_id}\n'.format(
							gId=gId,
							gName=gName,
							username=username,
							user_id=user_id
						)
					bot.sendMessage(fuckchannel, tmp)
					print(tmp)
	elif content_type == 'text':
		say = msg['text'].lower()
		if 'reply_to_message' in msg.keys() and user_id == int(owner) and say == '@admin':
			reply_msgId = msg['reply_to_message']['message_id']
			for x in [reply_msgId, message_id]:
				bot.deleteMessage((chat_id, x))



# 登入資訊
parser = SafeConfigParser()
parser.read('apitoken.txt')
owner = parser.get('apitoken', 'owner')
bot_apitoken = parser.get('apitoken', 'token')
bot = telepot.Bot(bot_apitoken)
bot.sendMessage(int(owner), '運轉中!')
bot.message_loop(handle)
print ('監聽中 ...')

while 1:
	time.sleep(10)
