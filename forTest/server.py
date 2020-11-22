from socket import socket, AF_INET, SOCK_STREAM
import sys
from common.external_func import get_msg, send_msg
from common.vars import DEF_PORT, DEF_IP
import argparse

msg_responce = '200'


def arg_parce():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEF_PORT)
    parser.add_argument('-a', default=DEF_IP, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    print(listen_address, listen_port)




def create_socket():

    srv_transport = socket(AF_INET,SOCK_STREAM)
    srv_transport.bind(('localhost', 65000))
    srv_transport.listen(3)
    return srv_transport



def mainloop():
    socket = create_socket()
    all_clients = []
    name = dict()
    try:
        while True:
            client, client_address = socket.accept()
            print(client)
            # print('ACCEPT')
            try:
                client_msg = client.recv(4096)
                get_msg(client_msg)
                print(get_msg(client_msg))
                send_msg(client,msg_responce)
                print(f'MSG RESPONCE {msg_responce}')
                # data_decode = client_msg.decode('utf-8')

            except OSError:
                pass
            else:
                print(f'Получен запрос на соединение.{client_address}')
                all_clients.append(client)
    except:
        pass


if __name__ == '__main__':
    print('SERVER IS START')
    arg_parce()
    mainloop()