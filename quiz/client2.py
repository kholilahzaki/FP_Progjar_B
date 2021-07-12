import socket
import sys
import threading

def read_msg(sock_cli, friend_req_queue):
    while True:
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break
        cmd, message = data.split(b"|", 1)
        cmd = cmd.decode("utf-8")
        if cmd == "message":
            message = message.decode("utf-8")
            print(message)
        elif cmd == "soal":
            nomer, soal = message.split(b"|",1)
            soal = soal.decode("utf-8")

            print(nomer)

            print(soal)

sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# sock_cli.connect(("0.0.0.0", 80))
sock_cli.connect(('127.0.0.1', 6666))

#kirim username ke server.py
uname = input("Masukkan username: ")
sock_cli.send(bytes(uname, "utf-8"))

friend_req_queue = set()

#buat thread utk membaca pesan dan jalankan threadnya
thread_cli = threading.Thread(target=read_msg, args=(sock_cli, friend_req_queue))
thread_cli.start()

try:
    while True:
        type = input("press enter to continue or type chat\n")
        if type != "chat":
            num = input("Pilih angka 0 - 16 atau masukkan jawaban \n")
            if num == "":
                continue
            elif num == "a":
                sock_cli.send(bytes("jawaban|{}".format(num), "utf-8"))
            elif num == "b":
                sock_cli.send(bytes("jawaban|{}".format(num), "utf-8"))
            elif num == "c":
                sock_cli.send(bytes("jawaban|{}".format(num), "utf-8"))
            elif num == "d":
                sock_cli.send(bytes("jawaban|{}".format(num), "utf-8"))
            else:
                sock_cli.send(bytes("soal|{}".format(num), "utf-8"))

        else:
            dest = input("Ketik input sesuai format : \n"
                         "- Kirim Pesan (message <username> <message>)\n"
                         "- Pesan Broadcast (bcast <message>)\n"
                         "- Tambah Teman (addfriend <username>)\n"
                         "- Keluar (exit)\n")
            msg = dest.split(" ", 1)

            if msg[0] == "message":
                uname, message = msg[1].split(" ", 1)
                sock_cli.send(bytes("{}|{}".format(uname, message), "utf-8"))
            elif msg[0] == "bcast":
                sock_cli.send(bytes("bcast|{}".format(msg[1]), "utf-8"))
            elif msg[0] == "addfriend":
                sock_cli.send(bytes("addfriend|{}".format(msg[1]), "utf-8"))
            elif msg[0] == "exit":
                sock_cli.close()
                break

except KeyboardInterrupt:
    sock_cli.close()
    sys.exit(0)