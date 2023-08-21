# importing all required libraries
#reciver 1264789410
#sender app.Id  12649513
#hash e2ce54566874a998cabbf19b5a86909f
#tocken .Id  12649513
#hash e2ce54566874a998cabbf19b5a86909f
#token 5347981978:AAHs2C9JC3S65O5aUkN0nR9F9-nsxCb26MI

import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

import cv2

# get your api_id, api_hash, token
# from telegram as described above
api_id = '12649513'
api_hash = 'e2ce54566874a998cabbf19b5a86909f'
token = '5347981978:AAHs2C9JC3S65O5aUkN0nR9F9-nsxCb26MI'
message = "wellcome"

# your phone number
phone = '+919492440835'

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():

	client.send_code_request(phone)
	
	# signing in the client
	client.sign_in(phone, input('Enter the code: '))

print(client)
#try:
	# receiver user_id and access_hash, use
	# my user_id and access_hash for reference
#receiver = InputPeerUser(1158987081, 0)
#receiver = InputPeerUser(803015402, 0)

#receiver = InputPeerUser(, 0)
group = "thisisthesecurity"
ent_group = client.get_entity(group)

client.send_message(entity = ent_group, message = "testingggg")
def send_image(img):
    """
    sends cv2 image 
    """
    # store cv2 image temporarily
    cv2.imwrite("temp.jpg", img)
    client.send_file(entity = ent_group, file = "temp.jpg")

def send_message(message):
    """
    will send message to number in telegram
    """
    client.send_message(entity = ent_group, message = message)

reply = None
def get_message():
    """
    wait for reply and returns reply 
    """
    global reply 
    @client.on(events.NewMessage)
    async def send_relpy(event):
        global reply
        sender = await event.get_sender()
        print(sender)
        print(event.sender_id)
        print(event)
        print("raw text is : ",event.raw_text)
        if event.sender_id ==1264789410:
            raw_text = event.raw_text
            reply = raw_text
            await event.reply("yes I recieved the data")
            await client.disconnect()
            print("after disconnected ")

    client.start()
    client.run_until_disconnected()
    client.connect()
    return reply

if _name=="__main_":
    
    send_image(cv2.imread("im1.jpeg"))
    
    get_message()
    
    send_message("hey testing here again after recieve message")