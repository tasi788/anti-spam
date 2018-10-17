__author__ = '@hexlightning'

import time
import logging
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint as pp
from configparser import SafeConfigParser
from itertools import zip_longest
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


def checkName(username, user_id=123):
	with open('fuckdict.txt', encoding='utf8') as f:
		fuckname = f.read().split('\n')
		try:
			fuckname.remove('')
		except:
			pass
	with open('fuckuid.txt', mode='r', encoding='utf8') as f:
		fuckuid = f.read().split(',')
	for x, y in zip_longest(fuckname, fuckuid):
		if x in username:
			return True, x
		elif str(y) == str(user_id):
			return True, 'uid'


def on_callback_query(msg):
	#pp(msg)
	query_id, from_id, query_data = telepot.glance(
		msg, flavor='callback_query')
	content_type, chat_type, chat_id, date, message_id = telepot.glance(
		msg['message'], long=True)
	status, gId, targetuser = query_data.split(' ')
	if status == 'ban':
		print('ban')
		tmp = '{text}' \
			'\n' \
			'Ban by: ' \
			'{name}'.format(text=msg['message']['text'], name=msg['from']['first_name'])
		try:
			bot.kickChatMember(gId, targetuser)
			bot.answerCallbackQuery(query_id, text='Banned.')
			reply_markup = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='等等，火錯人了', callback_data='unban {gId} {user_id}'.format(
					gId=gId, user_id=targetuser))]
			])
			# message': {'chat
			bot.editMessageText((chat_id, message_id), tmp.replace(
				'New', 'Banned'), parse_mode='html', reply_markup=reply_markup)
		except Exception as e:
			print(e)
			bot.answerCallbackQuery(query_id, text='踢不走。')
			#bot.sendMessage(checkNamelog, )
	elif status == 'pass':
		print('pass')
		tmp = '{text}' \
			'\n' \
			'Passed by: ' \
			'{name}'.format(text=msg['message']['text'], name=msg['from']['first_name'])
		try:
			bot.answerCallbackQuery(query_id, text='好ㄛ')
			reply_markup = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='欸幹回去，這人怪怪的', callback_data='back {gId} {user_id}'.format(
					gId=gId, user_id=targetuser))]
			])
			# message': {'chat
			bot.editMessageText((chat_id, message_id), tmp.replace(
				'New', 'Passed'), parse_mode='html', reply_markup=reply_markup)
		except Exception as e:
			print(e)
			bot.answerCallbackQuery(query_id, text='??????')
			#bot.sendMessage(checkNamelog, )

	elif status == 'unban':
		print('unban')
		tmp = '{text}' \
			'\n' \
			'Unban by: ' \
			'{name}'.format(text=msg['message']['text'], name=msg['from']['first_name'])
		try:
			bot.unbanChatMember(gId, targetuser)
			bot.answerCallbackQuery(query_id, text='Done.')
			reply_markup = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='阿拉花瓜', callback_data='ban {gId} {user_id}'.format(
					gId=gId, user_id=targetuser)),
				InlineKeyboardButton(text='好人', callback_data='pass {gId} {user_id}'.format(
					gId=gId, user_id=targetuser)),
			]])
			#bot.editMessageText((chat_id, message_id), 'Done.', reply_markup=reply_markup)
			bot.editMessageText((chat_id, message_id), tmp.replace(
				'Banned', 'New'), parse_mode='html', reply_markup=reply_markup)
		except Exception as e:
			print(e)
			#bot.answerCallbackQuery(query_id, text='踢不走。')
	else:
		try:
			tmp = msg['message']['text']
			bot.answerCallbackQuery(query_id, text='Done.')
			reply_markup = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='阿拉花瓜', callback_data='ban {gId} {user_id}'.format(
					gId=gId, user_id=targetuser)),
				InlineKeyboardButton(text='好人', callback_data='pass {gId} {user_id}'.format(
					gId=gId, user_id=targetuser)),
			]])
			#bot.editMessageText((chat_id, message_id), 'Done.', reply_markup=reply_markup)
			bot.editMessageText((chat_id, message_id), tmp, parse_mode='html', reply_markup=reply_markup)
		except Exception as e:
			print(e)
			#bot.answerCallbackQuery(query_id, text='踢不走。')



def handle(msg):
	# pp(msg)
	content_type, chat_type, chat_id, msg_date, message_id = telepot.glance(
		msg, long=True)
	user_id = msg['from']['id']
	username = msg['from']['first_name']
	if 'last_name' in msg['from'].keys():
		username += ' ' + msg['from']['last_name']
	if content_type == 'new_chat_member':
		gId = msg['chat']['id']
		gName = msg['chat']['title']
		new_user_id = msg['new_chat_member']['id']
		if new_user_id == botId:
			tmp = 'Invited\n' \
				'group name: <code>{gName}</code> \n' \
				'group id: <code>{gId}</code> \n' \
				'Invited by\n' \
				'username: <a href="tg://user?id={user_id}">{username}</a>\n' \
				'uid: <code>{user_id}</code> '.format(
					gName=gName,
					gId=gId,
					username=username.replace(
						'<', ' &lt; ').replace('>', ' &gt; '),
					user_id=user_id
				)
			greeting = '我沒有濫權就會自己離家出走唷'
			bot.sendMessage(chat_id, greeting)
			bot.sendMessage(invitelog, tmp, parse_mode='html')

		if checkName(username, new_user_id):
			tmp = 'Banned\n' \
				'group id: <code>{gId}</code>\n' \
				'group name: <code>{gName}</code>\n' \
				'name: <a href="tg://user?id={user_id}">{username}</a>\n' \
				'uid: <code>{user_id}</code>\n'.format(
					gId=gId,
					gName=gName,
					username=username.replace('<', '&lt;').replace(
						'>', '&gt;').replace('&', '&amp;'),
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
						'所以我要傷心的離開了'.format(
							user_id=user_id, username=username)
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
		else:
			userpic, userurl = True, ''
			if bot.getUserProfilePhotos(user_id)['total_count'] == 0:
				userpic = False
			if 'username' in msg['from'].keys():
				userurl = '@' + msg['from']['username']
			tmp = 'New\n' \
				'group id: <code>{gId}</code>\n' \
				'group name: <code>{gName}</code>\n' \
				'name: <a href="tg://user?id={user_id}">{username}</a>\n' \
				'username: {userurl}\n' \
				'uid: <code>{user_id}</code>\n' \
				'profile pic: <code>{userpic}</code>\n' \
				'======================='.format(
					gId=gId,
					gName=gName,
					username=username.replace('<', '&lt;').replace(
						'>', '&gt;').replace('&', '&amp;'),
					user_id=user_id,
					userpic=userpic,
					userurl=userurl
				)
			reply_markup = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='阿拉花瓜', callback_data='ban {gId} {user_id}'.format(
					gId=gId, user_id=user_id)),
				InlineKeyboardButton(text='好人', callback_data='pass {gId} {user_id}'.format(
					gId=gId, user_id=user_id)),
			]])
			bot.sendMessage(checkNamelog, tmp, parse_mode='html',
							reply_markup=reply_markup)

	elif content_type == 'text':
		say = msg['text'].lower()
		# 作者濫權部分。
		if say[:5] == '@bang' and str(user_id) in owner and chat_type == 'private':
			sayList = say.split(' ')
			varList = ['cmd', 'tuser', 'tchatId']
			def fucknDel(chat_id, message_id, reply_user_id=None, bang=False):
				try:
					bot.deleteMessage((chat_id, message_id))
					if bang == True:
						bot.kickChatMember(
							chat_id, sayList[1])
				except Exception as e:
					print('varlist fuck error')
					logging.warning(str(e))
			fucknDel(chat_id, message_id, bang=True)

		elif chat_type == 'private':
			if say[:4] == '/chk':
				tmp = checkName(say[5:])
				if tmp:
					bot.sendMessage(chat_id, '{} {}'.format(tmp[0], tmp[1]))
				else:
					bot.sendMessage(chat_id, 'False')
		elif 'reply_to_message' in msg.keys() and str(user_id) in owner:
			reply_msgId = msg['reply_to_message']['message_id']
			reply_user_id = msg['reply_to_message']['from']['id']

			def fucknDel(chat_id, message_id, reply_user_id=None, bang=False):
				try:
					for x in [message_id, reply_msgId]:
						bot.deleteMessage((chat_id, x))
					if bang == True:
						bot.kickChatMember(
							chat_id, reply_user_id)
						bot.sendMessage(checkNamelog, '#banglog \n{username} bang 飛了 `{reply}`'.format(username=username,reply=reply_user_id), parse_mode='markdown')
				except Exception as e:
					print('fuck error')
					logging.warning(str(e.description))
			if say == '@bang':
				fucknDel(chat_id, message_id, reply_user_id, bang=True)
			elif say == '@delmsg':
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
owner = parser.get('apitoken', 'owner').split(',')
bot_apitoken = parser.get('apitoken', 'token')
fuckchannel = int(parser.get('apitoken', 'channel'))
invitelog = int(parser.get('apitoken', 'invitelog'))
botId = int(bot_apitoken.split(':')[0])
checkNamelog = int(parser.get('apitoken', 'checkNamelog'))

bot = telepot.Bot(bot_apitoken)

# bot.message_loop(handle)


def looooo():
	bot.sendMessage(int(owner[0]), '運轉中!')
	MessageLoop(bot,  {'chat': handle,
					   'callback_query': on_callback_query}).run_as_thread()
	while 1:
		time.sleep(10)


print ('監聽中 ...')

looooo()
