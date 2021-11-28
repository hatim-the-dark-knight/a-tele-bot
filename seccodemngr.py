from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from numpy import random
import logging


code = [6, 1, 7, 4]
difficulty = 0
moves = 8
again = 0
reply_keyboard = [["Easy"], ["Normal"], ["Hard"]]


def start (update, context) -> int:
	update.message.reply_text ("Hii! I am the 'Crypt' bot! Nice to meet ya!")
	update.message.reply_text ("Difficulty:\nEasy -> 4-digit codes\nNormal -> 5-digit codes\nHard -> 6-digit codes")
	update.message.reply_text (
		"Now, what difficulty would you like to play at?",
		reply_markup = ReplyKeyboardMarkup (reply_keyboard, one_time_keyboard = True)
	)


def check_code (test):
	print (test)
	fm = []
	nm = []
	for i in range (len (code)):
		for j in range (len (test)):
			if (code[i] == test[j]):
				if (i == j):
					if test[j] not in fm:
						if test[j] in nm:
							nm.remove (test[j])
						fm.append (test[j])
				else:
					if test[j] not in fm:
						if test[j] not in nm:
							nm.append (test[j])
	return (len (fm), len (nm))

def game_logic (update, context):
	global moves, again
	if again == 0:
		return
	(fm, nm) = (0, 0)
	test_code = update.message.text
	if int (test_code):
		test = [int (x) for x in str (int (test_code))]
		if len (test) != len (code):
			reply = "\nError!  [No. of digits]"
			update.message.reply_text (reply)
		else:
			(fm, nm) = check_code (test)
			moves -= 1
			if fm == 0 and nm == 0:
				update.message.reply_text ("Oops!  None matched!")
			else:
				if (fm == len (code)):
					moves = 8
					update.message.reply_text ("Kudos to ya!  Successfully Decoded!")
					update.message.reply_text (
					"Now, the bot is idle!  So if you wanna play once more, select your next game's difficulty mode!\nIf you don't, then stop the bot!"
					, reply_markup = ReplyKeyboardMarkup (reply_keyboard, one_time_keyboard = True)
					)
					again = 0
					return
				fm_str = "FM "
				nm_str = "NM "
				reply = ""
				for x in range (fm):
					reply += fm_str
				for x in range (nm):
					reply += nm_str
				update.message.reply_text (reply)
			if moves != 0:
				reply = str (moves) + " moves left!  Use them wisely!"
				update.message.reply_text (reply)
			else:
				moves = 8
				reply = "Oops!  Out of Moves!  But, it's OK! \nThe secret code was: " + str (code) + "\nGood Luck for your next game!"
				update.message.reply_text (reply)
				update.message.reply_text (
				"Now, the bot is idle!  So if you wanna play once more, select your next game's difficulty mode!\nIf you don't, then stop the bot!", 
				reply_markup = ReplyKeyboardMarkup (reply_keyboard, one_time_keyboard = True)
				)
				again = 0
				return
	elif str (test_code):
		update.message.reply_text ("Error!  [Not an integer]")


def initiate_game(update, context):	
	global again
	if update.message.text == "Easy":
		difficulty = 4
	elif update.message.text == "Normal":
		difficulty = 5
	else:
		difficulty = 6
	
	update.message.reply_text("Difficulty set to " + update.message.text)
	again = 1

	code.clear ()
	code.insert (0, random.randint (1, 10))

	i = 1
	while (len (code) != difficulty):
		num = random.randint (0, 10)
		if num not in code:
			code.append (num)
			i+=1

	#update.message.reply_text ("The secret code generated is: ")
	#update.message.reply_text (code)
	update.message.reply_text ("Code Generated!  Now, Guess!")
	

updater = Updater (token = "1754277356:AAF4rPQTAYACkVKCJIHr231zOyOFQjwfDrU")
logging.basicConfig (
	format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)

start_handler = CommandHandler ("start", start)
updater.dispatcher.add_handler (start_handler)
updater.dispatcher.add_handler (
	MessageHandler (Filters.regex ("^(Easy|Normal|Hard)$"), initiate_game)
)
updater.dispatcher.add_handler (
	MessageHandler (Filters.text & ~Filters.command, game_logic)
)
updater.start_polling ()
updater.idle ()