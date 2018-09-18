__author__ = '@hexlightning'

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


def checkName(username):
	with open('fuckdict.txt', encoding='utf8') as f:
		fuckname = f.read().split('\n')
		fuckname.remove('')
	for x in fuckname:
		if x in username:
			return True

def handle(msg):
	#pp(msg)
	content_type, chat_type, chat_id, msg_date, message_id = telepot.glance(
		msg, long=True)
	user_id = msg['from']['id']
	username = msg['from']['first_name']
	if 'last_name' in msg['from'].keys():
		username += ' ' + msg['from']['last_name']
	if content_type == 'new_chat_member':
		gId = msg['chat']['id']
		gName = msg['chat']['title']
		if msg['new_chat_member']['id'] == botId:
			tmp = 'Invited\n' \
				'group name: <code>{gName}</code> \n' \
				'group id: <code>{gId}</code> \n' \
				'Invited by\n' \
				'username: <a href="tg://user?id={user_id}">{username}</a>\n' \
				'uid: <code>{user_id}</code> '.format(
					gName=gName,
					gId=gId,
					username=username.replace('<', ' &lt; ').replace('>', ' &gt; '),
					user_id=user_id
				)
			greeting = '我沒有濫權就會自己離家出走唷'
			bot.sendMessage(chat_id, greeting)
			bot.sendMessage(invitelog, tmp, parse_mode='html')

		if checkName(username) == True:
			tmp = 'Banned\n' \
				'group id: <code>{gId}</code>\n' \
				'group name: <code>{gName}</code>\n' \
				'name: <a href="tg://user?id={user_id}">{username}</a>\n' \
				'uid: <code>{user_id}</code>\n'.format(
					gId=gId,
					gName=gName,
					username=username.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;'),
					user_id=user_id
				)
			try:
				bot.kickChatMember(
					chat_id, user_id)
				bot.deleteMessage((chat_id, message_id))
				bot.sendMessage(fuckchannel, tmp, parse_mode='html')
				print(tmp)
			except Exception as e:
				# Bad Request: message can't be deleted
				permission = 'Bad Request: not enough rights to restrict/unrestrict chat member'
				if str(e.description) == permission:
					tmp = '我踢不走 <a href="tg://user?id={user_id}">{username}</a> 這個廣告帳號\n' \
						'因為你沒給我濫權 (´･_･`)\n' \
						'所以我要傷心的離開了'.format(user_id=user_id, username=username)
					bot.sendMessage(
						chat_id, tmp, parse_mode='html', reply_markup=message_id)
					bot.leaveChat(chat_id)
					tmp = '離開惹\n' \
						'group id: `{gId}`\n' \
						'group name: {gName}\n'.format(
							gId=gId, gName=gName)
					bot.sendMessage(fuckchannel, tmp,
									parse_mode='markdown')
				logging.warning(str(e.description))

	elif content_type == 'text':
		say = msg['text'].lower()
		# 作者濫權部分。
		if say[:5] == '@bang' and user_id == int(owner):
			sayList = say.split(' ')
			varList = ['cmd', 'tuser', 'tchatId']
			for x, y in zip(sayList, varList):
				globals()[y] = x
			if chat_type == 'private':
				try:
					bot.kickChatMember(
						tchatId, tuser)
				except Exception as e:
					bot.sendMessage(chat_id, str(e.description))
			else:
				bot.deleteMessage((chat_id, message_id))
				bot.kickChatMember(
					chat_id, tuser)

		elif 'reply_to_message' in msg.keys() and user_id == int(owner):
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
			elif say == 'delmsg':
				fucknDel(chat_id, message_id, reply_user_id)

		'''
		elif user_id in [397835845, 438685534]:
			if say == '/leave@fuck_spam_bot' and chat_type != 'private':
				bot.deleteMessage((chat_id, message_id))
				bot.leaveChat(chat_id)
				bot.sendMessage(int(owner), '滾出了 '+msg['chat']['title'])
		'''



# 登入資訊
parser = SafeConfigParser()
parser.read('apitoken.txt')
owner = parser.get('apitoken', 'owner')
bot_apitoken = parser.get('apitoken', 'token')
fuckchannel = int(parser.get('apitoken', 'channel'))
invitelog = int(parser.get('apitoken', 'invitelog'))
botId = int(bot_apitoken.split(':')[0])

bot = telepot.Bot(bot_apitoken)
bot.sendMessage(int(owner), '運轉中!')
bot.message_loop(handle)
print ('監聽中 ...')

while 1:
	time.sleep(10)
