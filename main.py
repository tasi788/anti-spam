__author__ = '@DingChen-Tsai'

import time
import logging
import telepot
from pprint import pprint as pp
from configparser import SafeConfigParser

'''
log頻道：https://t.me/joinchat/AAAAAElFrnF0_YOo2a7jNQ
作者在上面自己看。

未來會不會加更多功能？
可能會吧 我盡量 (´･_･`)

如果有新的字詞要新增怎麼辦？
到github丟issue, 沒問題的話看到會馬上merge。
之後會新增即時新增吧
'''

# 定義telegram各項參數


def handle(msg):
	#pp(msg)
	content_type, chat_type, chat_id, msg_date, message_id = telepot.glance(
		msg, long=True)
	user_id = msg['from']['id']
	botId = int(bot_apitoken.split(':')[0])
	fuckchannel = -1001229303409
	username = msg['from']['first_name']
	if 'last_name' in msg['from'].keys():
		username += ' ' + msg['from']['last_name']

	if content_type == 'new_chat_member':
		gId = msg['chat']['id']
		gName = msg['chat']['title']
		if msg['new_chat_member']['id'] == botId:
			tmp = 'Invited\n' \
				'group name: `{gName}` \n' \
				'group id: `{gId}` \n' \
				'Invited by\n' \
				'username: {username}\n' \
				'uid: `{user_id}` '.format(
					gName=gName,
					gId=gId,
					username=username,
					user_id=user_id
				)
			greeting = '咕嚕靈波（●´∀｀）ノ♡\n' \
				'我沒有濫權就會自己離家出走唷'
			bot.sendMessage(chat_id, greeting)
			bot.sendMessage(fuckchannel, tmp, parse_mode='markdown')

		with open('fuckdict.txt') as f:
			fuckname = f.read().replace('\n', '').split(',')
		for x in fuckname:
			if x in username:
				tmp = 'Banned\n' \
					'group id: `{gId}`\n' \
					'group name: `{gName}`\n' \
					'name: {username}\n' \
					'uid: `{user_id}`\n'.format(
						gId=gId,
						gName=gName,
						username=username,
						user_id=user_id
					)
				bot.sendMessage(fuckchannel, tmp, parse_mode='markdown')
				try:
					bot.kickChatMember(
						chat_id, user_id)
					bot.deleteMessage((chat_id, message_id))
					print(tmp)
					break
				except Exception as e:
					# Bad Request: message can't be deleted
					permission = 'Bad Request: not enough rights to restrict/unrestrict chat member'
					if str(e.description) == permission:
						tmp = '我踢不走[這個廣告帳號](tg://user?id={user_id})\n' \
							'因為你沒給我濫權 (´･_･`)'.format(user_id=user_id)
						bot.sendMessage(
							chat_id, tmp, parse_mode='html', reply_markup=message_id)
						bot.leaveChat(chat_id)
						tmp = '離開惹\n' \
							'group id: `{gId}`\n' \
							'group name: {gName}\n'.format(
								gId=gId, gName=gName)
						bot.sendMessage(fuckchannel, tmp,
										parse_mode='markdown')
					#print(e.description)
					logging.warning(str(e.description))

	elif content_type == 'text':
		say = msg['text'].lower()
		if 'reply_to_message' in msg.keys() and user_id == int(owner):
			reply_msgId = msg['reply_to_message']['message_id']
			reply_user_id = msg['reply_to_message']['from']['id']

			def fucknDel(chat_id, message_id, reply_user_id, bang=False):
				try:
					for x in [reply_msgId, message_id]:
						bot.deleteMessage((chat_id, x))
					if bang == True:
						bot.kickChatMember(
							chat_id, reply_user_id)
				except Exception as e:
					logging.warning(str(e.description))

			if say == '@admin':
				fucknDel(chat_id, message_id, reply_user_id)
			elif say == '@admin bang':
				fucknDel(chat_id, message_id, reply_user_id, bang=True)




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
