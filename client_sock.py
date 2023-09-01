import tkinter as tk
import socket
import threading

def on_closing():
    try:
        client.send('exit'.encode('ascii'))
        client.close()
    except:
        pass
    root.quit()

def on_btn_ok_click():
    global client
    global nickname
    nickname = entry.get()
    if nickname != '':
        nickname = entry.get()
        entry.config(state='disabled')
        btn_ok.config(state='disabled')
        memo.config(state='normal')
        btn_send.config(state='normal')
        print(nickname)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 50001))
        client.send(nickname.encode('ascii'))
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

def on_btn_send_click():
    text = memo.get()
    print(text)
    message = '{}: {}'.format(nickname, text)
    client.send(message.encode('ascii'))
    memo.delete(0, 'end')

root = tk.Tk()
root.minsize(400, 400)
root.maxsize(800, 600)
root.protocol('WM_DELETE_WINDOW', on_closing)

entry = tk.Entry(root)
entry.pack(fill='x', pady=10)

btn_ok = tk.Button(root, text='OK', command=on_btn_ok_click)
btn_ok.pack(fill='x')

log = tk.Text(root)
log.config(state='disabled')
log.pack(fill='both', expand=True, pady=20)

memo = tk.Entry(root)
memo.config(state='disabled')
memo.pack(fill='both', expand=True, pady=20)

btn_send = tk.Button(root, text='Send', command=on_btn_send_click)
btn_send.config(state='disabled')
btn_send.pack(fill='x')

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'exit':
                log.config(state='normal')
                log.insert('end', 'Сервер отключен.\n')
                log.config(state='disabled')
                client.close()
                break
            else:
                log.config(state='normal')
                log.insert('end', message + '\n')
                log.config(state='disabled')
        except:
            log.config(state='normal')
            log.insert('end', 'Произошла ошибка.\n')
            log.config(state='disabled')
            client.close()
            break

root.mainloop()
