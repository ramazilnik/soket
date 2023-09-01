import tkinter as tk
import socket
import threading

root = tk.Tk()

root.minsize(200, 200)
root.maxsize(800, 600)

entry = tk.Entry(root)
entry.pack()

def on_btn_ok_click():
    nickname = entry.get()
    print(nickname)

btn_ok = tk.Button(root, text='OK', command=on_btn_ok_click)
btn_ok.pack()

root.mainloop()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 50001))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
