__author__ = '@hexlightning'

import re
import json
import time
import random
import asyncio
import pymongo
from pymongo.errors import ConnectionFailure
import logging
import requests
import telepot
import telepot.text
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint as pp
from configparser import SafeConfigParser
from itertools import zip_longest



import killall
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
try:
	client = pymongo.MongoClient("172.17.0.3")#, 27017)
	#client.admin.command('ismaster')
	db = client.db
	record = db.join
	print('DB Loaded')
except ConnectionFailure:
	print('DB DOWN...!!')
	#sys.exit()


async def Loadfuck():
	global fuckname, fuckuid
	url = 'https://raw.githubusercontent.com/tasi788/anti-spam/master/fuckdict.txt'
	try:
		fuckname = requests.get(url)
		fuckname.text.split('\n')
		fuckname.remove('')
	except:
		pass
	url = 'https://raw.githubusercontent.com/tasi788/anti-spam/master/fuckuid.txt'
	try:
		fuckuid = requests.get(url)
		fuckuid.text.split('\n')
		fuckuid.remove('')
	except:
		pass
	await asyncio.sleep(600)

'''loop = asyncio.get_event_loop()
loop.create_task(Loadfuck)
loop.run_forever()'''

def checkName(username, user_id=123):
	#if ad.only_alphabet_chars(username, 'ARABIC'):
	#	return True, '是瓜仔'
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
		if y == str(user_id):
			return True, 'uid'


def on_callback_query(msg):
	#pp(msg)
	query_id, from_id, query_data = telepot.glance(
		msg, flavor='callback_query')
	content_type, chat_type, chat_id, date, message_id = telepot.glance(
		msg['message'], long=True)
	status, gId, targetuser = query_data.split(' ')
	if 'entities' in msg['message'].keys():
		oldmsg = telepot.text.apply_entities_as_html(msg['message']['text'], msg['message']['entities'])
	if status == 'ban':
		print('ban')
		tmp = '{text}' \
			'\n' \
			'Ban by: ' \
			'{name}'.format(text=oldmsg, name=msg['from']['first_name'])
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
			'{name}'.format(text=oldmsg, name=msg['from']['first_name'])
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
			'{name}'.format(text=oldmsg, name=msg['from']['first_name'])
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
	elif status == 'boom':
		if from_id not in [525239263, 184805205, 162874313]:
			bot.answerCallbackQuery(query_id, text='你不是路西法:3')
			return
		tmp = killall.fuck(targetuser, act=True)
		for x in tmp:
			try:
				print(x)
				bot.sendMessage(chat_id, f'{x[2]}')
				bot.kickChatMember(x[0], x[1])
				bot.deleteMessage((x[0], x[3]))
			except Exception as e:
				print(e)
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

def release(msg):
	print(msg)


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
			record.insert_one(msg).inserted_id
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
	elif 'forward_from_chat' in msg.keys():
		gId = msg['chat']['id']
		gName = msg['chat']['title']
		fw = msg['forward_from_chat']
		if checkName(fw['title'], fw['id']):
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
	elif content_type == 'text':
		say = msg['text'].lower()
		#if -1001409787631
		#小精靈們的 (´提ω供`)
		re_list = ['(d(.*)?d(.*)?a(.*)?v(.*)?[0-9]((.*)?[0-9])(.*)?[点.](.*)?C(.*)?[0O](.*)?M)|(585781612|873014133|951613797|926066663)']#['^.*(a.?i.?s.*c.?[o0].?m).*']
		gId = msg['chat']['id']
		if 'title' in msg['chat']:
			gName = msg['chat']['title']
		if 'forward_from_chat' in msg.keys():
			fw = msg['forward_from_chat']
		if gId != -1001409787631:
			
			for x in re_list:
				re_result = re.findall(x, say, re.IGNORECASE)
				if re_result:
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
		elif say[:5] == '/ping':
			bot.sendMessage(chat_id, 'pong')

		elif say[:5] == '/info':
			tmp = json.dumps(msg, ensure_ascii=False, indent=4)
			bot.sendMessage(msg['from']['id'], tmp)#, parse_mode='html')
			bot.deleteMessage((chat_id, message_id))

		if gId == -1001409787631:
			if say[:5] == '/test':
				for x in re_list:
					re_result = re.findall(x, msg['reply_to_message']['text'], re.IGNORECASE)
					if re_result:
						bot.sendMessage(chat_id, f'True {re_result}')
					else:
						bot.sendMessage(chat_id, 'False.')
			elif say[:4] == '/chk':
				tmp = checkName(say[5:])
				if tmp:
					bot.sendMessage(chat_id, '{} {}'.format(tmp[0], tmp[1]))
				else:
					bot.sendMessage(chat_id, 'False')


			elif say[:5] == '/boom':
				if 'reply_to_message' in msg and 'forward_from' in msg['reply_to_message']:
					target = msg['reply_to_message']['forward_from']['id']
				else:
					target = say[6:]
				txt, keyboard = killall.fuck(target)
				inline = InlineKeyboardMarkup(inline_keyboard=[[keyboard]])
				if txt:
					bot.sendMessage(chat_id, f'<a href="tg://user?id={target}">boom 目標</a>\n'+txt, reply_markup=inline, parse_mode='HTML')
				else:
					bot.sendMessage(chat_id, '什麼都沒有。')

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
				print('bangg')
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

	elif content_type == 'sticker':
		if chat_id == -1001061319491:
			bot.deleteMessage((chat_id, message_id))

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
	MessageLoop(bot,  {'chat': release,
					   'callback_query': on_callback_query}).run_as_thread()
	while 1:
		time.sleep(10)


print ('監聽中 ...')

looooo()
