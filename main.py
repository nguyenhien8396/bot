import random
from telethon import TelegramClient, events
from telethon.sync import TelegramClient as TelegramClientSync
# telethon '1.24.0'

print("Add account chinh vao group can clone message \n")
channel_id_listen = input("Nhap channel_id listen (ex: 1357859415):\n")
channel_id_listen = int(channel_id_listen)

channel_id_receiver = input(
    "Nhap channel_id receiver (them dau - dang truoc, ex: -744920642 ):\n")
channel_id_receiver = int(channel_id_receiver)


# 84973330213 19937677 9712470f8b286de877e864b24917d87a

client = TelegramClient("anon", 19937677, "9712470f8b286de877e864b24917d87a")


users = []
usersClients = []

f = open("accounts.txt", "r")
for idx, account in enumerate(f):
    user_data = account.split(" ")
    user = {}
    user['phone'] = user_data[0]
    user['api_id'] = int(user_data[1])
    user['api_hash'] = user_data[2]
    users.append(user)
    print("Connect account " + user_data[0] + "\n")
    clientX = TelegramClientSync("anon" + str(idx), user_data[1], user_data[2])
    clientX.connect()
    clientX.start()

    print("Connected account " +
          user_data[0] + " " + str(clientX.is_connected()) + "\n")
    usersClients.append(clientX)

preUserSentId = 0
preUserListenerId = random.randint(0, len(usersClients))


@client.on(events.NewMessage)
async def newMessageListener(event):
    try:
        chat = await event.get_chat()
        sender = await event.get_sender()
        print(event.raw_text)
        print(chat.id)
        if chat.id == channel_id_listen:
            if sender.id != preUserSentId:
                preUserListenerId = random.randint(0, len(usersClients))
            if usersClients[preUserListenerId].is_connected():
                print('connected')
            else:
                await usersClients[preUserListenerId].connect()
                await usersClients[preUserListenerId].start()

            if event.message.media:
                msg_media_id = str(event.message.media.photo.id)
                output = str('download/{}'.format(msg_media_id))
                await client.download_media(event.message.media, file=output)

                input_file = str('download/{}.jpg'.format(msg_media_id))
                await usersClients[preUserListenerId].send_file(channel_id_receiver, input_file)
            else:
                await usersClients[preUserListenerId].send_message(channel_id_receiver, event.raw_text)

    except Exception as e:
        print('e', e)
with client:
    client.run_until_disconnected()
