import socket
import sys
import threading

x = 0
def read_msg(clients, friends, sock_cli, addr_cli, src_uname):
    while True:
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        dest, msg = data.split(b"|", 1)
        dest = dest.decode("utf-8")
        print(dest)
        print(msg)

        if dest == "soal":
            msg = msg.decode("utf-8")
            num = int(msg)
            send_question(clients, Q[num], addr_cli, msg)
        elif dest == "jawaban":
            msg = msg.decode("utf-8")
            print(src_uname)
            print(A[num])
            if A[num] == msg:
                print("true")
                send_msg(clients[src_uname][0], "true")
                skor[src_uname] += 1
                score = str(skor[src_uname])
                send_msg(clients[src_uname][0], "skor : "+score)
            else:
                print("false")
                send_msg(clients[src_uname][0], "false")

        elif dest == "addfriend":
            dest_username = msg.decode("utf-8")
            friends[src_uname].append(dest_username)
            friends[dest_username].append(src_uname)
            send_msg(clients[dest_username][0], f"{src_uname} is now friend")
            send_msg(clients[src_uname][0], f"{dest_username} is now friend")
        elif dest == "bcast":
            msg = msg.decode("utf-8")
            _msg = "<{}>: {}".format(src_uname, msg)
            send_broadcast(clients, friends, src_uname, _msg, addr_cli)
        else:
            dest_uname = dest
            msg = msg.decode("utf-8")
            _msg = "<{}>: {}".format(src_uname, msg)
            dest_sock_cli = get_sock(clients, friends, src_uname, dest_uname)
            if dest_sock_cli is not None:
                send_msg(dest_sock_cli, _msg)
    sock_cli.close()
    print("connection closed", addr_cli)
    del clients[src_uname]

def send_question(clients, data, sender_addr_cli, nomer):
    data = data + "\n\npress enter "
    for sock_cli, addr_cli, _ in clients.values():
        sock_cli.send(bytes("soal|{}|{}".format(nomer, data), "utf-8"))

def send_broadcast(clients, friends, src_uname, data, sender_addr_cli):
    cur_friends = friends[src_uname]
    for cur_friend in cur_friends:
        if cur_friend not in clients:
            continue
        sock_cli, addr_cli, _ = clients[cur_friend]
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            send_msg(sock_cli, data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes("message|{}".format(data), "utf-8"))

def get_sock(clients, friends, src_uname, dest_uname):
    if dest_uname not in friends[src_uname]:
        send_msg(clients[src_uname][0], "Error: {} not a friend".format(dest_uname))
        return None
    if dest_uname not in clients:
        send_msg(clients[src_uname][0], "Error: {} not in clients".format(dest_uname))
        return None
    return clients[dest_uname][0]


# server_address = ("0.0.0.0", 80)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server_socket.bind(server_address)
server_socket.bind(('0.0.0.0', 6666))
server_socket.listen(5)
quest = ["tes1","tes2"]
Q = [" 0. -Fifth Harmony (Work From Home)-\n\n I know you're always on the night shift\n But I can't stand these ____ alone \n a.Roads b.Times c.Days d.Nights",
     " 1. -Dua Lipa (New Rules)-\n\n And if you're under him, you ain't gettin' over him\n I got new rules; I ____ 'em\n a.Count b.Got c.Like d.Choose",
     " 2. -Shawn Mendez (Treat You Better)-\n\n I know I can treat you better than he can\n Cause any girl like you deserves a ____ \n a.Good Man b.Gentleman c.Love d.Strong Man",
     " 3. -Ellie Goulding (Love Me Like You Do)-\n\n\ You're the light, You're the night\n You're the color of my ____ \n a.Blood b.Heart c.Soul d.Eyes",
     " 4. -Ed Sheeran (Perfect)-\n\n Well I found a woman, stronger than anyone I know\n She shares my ____, I hope that someday I'll share her home \n a.Dreams b.Words c.Thought d.Soul",
     " 5. -SIA (Chandelier)-\n\n Throw 'em back, 'til I lose count\n I'm gonna ____ from the chandelier \n a.Swing b.Shine c. Jump d.Scream",
     " 6. -Katy Perry (ROAR)- \n\n You held me down, but I got up (Hey)\n Already brushing off the ____ \n a.Dust b.Sound c.Dirts d.Lights",
     " 7. -Ed Sheeran (Shape of You)-\n\n Girl you know I want your love\n You're love was ____ for somebody like me \n a.Stolen b.Handmade c.Born d.Shone Brightly",
     " 8. -Justin Bieber (Sorry)-\n\n Is it too late now to say sorry?\n Cause I'm missing more than just your ____ \n a.Body b.Money c.Truth d.Glory",
     " 9. -Meghan Trainor (All About that Bass)-\n\n I see the magazines, working that Photoshop\n We know that ____ ain't real \n a.Pic b.Sheet c.Shit d.Shape",
     " 10. -Rihanna (Diamonds)\n\n Find light in the beautiful sea\n Ichoose to be ____ \n a.With you b.Happy  c.Brighter d.Your love ",
     " 11. -Lil Nas X (Old Town Road)-\n\n Hat is matte black\n Got the boot's that's ____ to match \n a.High b.Dark c.Brown d.Black",
     " 12. -Harry Styles (Watermelon Sugar)-\n\n Taste like strawberry, on the summer ____ \n a.Morning b.Night c.Afternoon d.Evening",
     " 13. -Calumn Scott (You Are The Reason)-\n\n I'd climb every ____, and swim every ocean  \n a.Cliff b.Stairs c.Mountain d.Hills",
     " 14. -Ariana Grande (Thank You, Next)-\n\n Thought I'd end up with ____, but he wasn't a match \n a.Sean b.Sam c.Mark d.John",
     " 15. -Naomi Scott (Speechless)-\n\n Here comes a wave meant to ____ me away \n a.Sweep b.Wash c.Walks d.Watch",
     " 16. -BTS (Dynamite)-\n\n Shoes on get up in the morn' cup of ____ let's rock and roll \n a.Milk b.Tea c.Drink d.Cream"]

A = ['d', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'c', 'a', 'b', 'a']

# buat dictionary utk menyimpan informasi
clients = {}
friends = {}
skor = {}

try:
    while True:
        sock_cli, addr_cli = server_socket.accept()

        # membaca username client
        src_uname = sock_cli.recv(65535).decode("utf-8")
        print(src_uname, "joined")

        # membuat thread
        thread_cli = threading.Thread(target=read_msg, args=(clients, friends, sock_cli, addr_cli, src_uname))
        thread_cli.start()

        # simpan informasi client ke dictionary
        clients[src_uname] = (sock_cli, addr_cli, thread_cli)
        friends[src_uname] = []
        skor[src_uname] = 0

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)