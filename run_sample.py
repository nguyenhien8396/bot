from telethon import TelegramClient, events
from telethon.sync import TelegramClient as TelegramClientSync

import sys
import csv

api_id = 0000
api_hash = ''

client = TelegramClient("anon", api_id, api_hash)

input_file = sys.argv[1]
users = []

with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    print('rows', rows)
    for row in rows:
        print('row', row)
        user = {}
        user['username'] = row[0]
        user['api_id'] = int(row[1])
        user['api_hash'] = row[2]
        users.append(user)
print("user2", users[0])

client2 = TelegramClientSync("anon2", users[0]["api_id"], users[0]["api_hash"])
client2.connect()
client2.start()
print(client2.is_connected())

print('aa')
def sendMessage():
    for user in users:
        receiver = client.get_input_entity(user['username'])

@client.on(events.NewMessage())
#glorious 1221886695
async def newMessageListener(event):
    try:
        print('channelId', event.message.peer_id.channel_id)
        if event.message.peer_id.channel_id == 1623261282:
            newMessage = event.message.message
            print("abc", event.message)
            if client2.is_connected():
                print('connected')
            else:
                await client2.connect()
                await client2.start()

            entity= await client2.get_entity("gloriousgemgroup")

            if event.message.media:
                msg_media_id = str(event.message.media.photo.id)
                output = str('download/{}'.format(msg_media_id))
                print('download media', output)
                await client.download_media(event.message.media, file=output)

                input_file = str('download/{}.jpg'.format(msg_media_id))
                await client.send_file(entity, input_file)
            else:
                await client2.send_message(entity=entity,message=newMessage)

    except Exception as e:
        print('e', e)
with client:
    client.run_until_disconnected()