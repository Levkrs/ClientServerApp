import socket
import time
import threading
from common.external_func import get_message, send_msg_finish

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

message = 'Первое сообщение кудато'
account_name = 'Egorka'
to_user = 'Guest'

message_dict = {
    ACTION: MESSAGE,
    SENDER: account_name,
    DESTINATION: to_user,
    TIME: time.time(),
    MESSAGE_TEXT: message
}


def message_from_server(sock):
    while True:
        try:
            # message = get_msg(sock)
            message = sock.recv(4096)
            message = get_message(message)
            print(message)
        except:
            print('Except')


def send_msg_to_server(sock, message):
    send_msg_finish(sock, message)


def user_menu_loop(sock):
    while True:
        msg = input('Введи чтонибудь')
        send_msg_to_server(sock, msg)
        if msg == 'stop':
            break


def create_connect():
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect(('localhost', 65000))
        print('Connect rdy')
        send_msg_to_server(transport, message)
        # send_msg(transport, message)
    except:
        pass
    else:
        receiver = threading.Thread(target=message_from_server, args=(transport,))
        receiver.daemon = True
        receiver.start()

        user_send_msg = threading.Thread(target=user_menu_loop, args=(transport,))
        user_send_msg.daemon = True
        user_send_msg.start()
        # print('Процессы запущены')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_send_msg.is_alive():
                continue
            break


if __name__ == '__main__':
    create_connect()
