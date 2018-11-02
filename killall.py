import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo
import sys

client = pymongo.MongoClient('172.17.0.6', 27017)
db = client.db
join = db.join

def fuck(uid, act=False):
	tmp, tmptxt = [], ''
	uid = int(uid)
	result = join.find({"from.id": uid})
	for x in result:
		gid = x['chat']['id']
		title = x['chat']['title']
		uid = x['from']['id']
		msgid = x['message_id']
		tmp.append((gid, uid, title, msgid))
		tmptxt += f'{title}\n'
	if act == False:
		return tmptxt, InlineKeyboardButton(
						text = '幹他',
						callback_data = f'boom boom {uid}')
	else:
		return tmp
		'''for x in tmp:
			try:
				print(f'{x[2]}')
				bot.kickChatMember(x[0], x[1])
				bot.deleteMessage((x[0], x[3]))
			except Exception as e:
				print(e)'''