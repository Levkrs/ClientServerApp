from socket import socket, AF_INET, SOCK_STREAM
import sys
from common.external_func import send_msg_finish, get_message
from common.vars import DEF_PORT, DEF_IP, EXIT, ACTION, TIME, ACCOUNT_NAME, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT, \
    PRESENCE, USER, ERROR, RESPONCE_200, RESPONCE_400, GET_CONTACT, ADD_CONTACT, DEL_CONTACT, USER_ID_TO_CONTACT, RESPONCE_202, \
    CUSTOM_RESPONCE, RESPONCE, DATA
import argparse
import select
from metaclass import ServerMaker
from descrptrs import Port
from db_class_server import ServerStorage
import threading



def arg_parce():
    parser = argparse.ArgumentParser()
    print('ARG PARCE')
    parser.add_argument('-p', default=DEF_PORT)
    parser.add_argument('-a', default=DEF_IP, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    print(listen_address, listen_port)
    return listen_address, listen_port



class ServerClass(metaclass=ServerMaker):
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        self.addr = listen_address
        self.port = listen_port
        self.database = database
        self.all_clients = []
        self.name = dict()
        self.message = []


    def create_socket(self):
        srv_transport = socket(AF_INET, SOCK_STREAM)
        srv_transport.bind((self.addr, self.port))
        srv_transport.settimeout(0.5)

        self.socket = srv_transport
        self.socket.listen()


    def mainlopp(self):

        self.create_socket()
        try:
            while True:
                try:
                    client, client_address = self.socket.accept()
                except:
                    pass
                else:
                    print(f'Получен запрос на соединение.{client_address}')
                    self.all_clients.append(client)

                recv_data_lst = []
                send_data_lst = []
                err_lst = []
                try:
                    if self.all_clients:
                        recv_data_lst, send_data_lst, err_lst = select.select(self.all_clients, self.all_clients, [], 0)
                except:
                    pass

                # Прием сообщений
                if recv_data_lst:
                    for client_with_message in recv_data_lst:
                        try:
                            # print('Try process_client_message')
                            self.process_client_message(get_message(client_with_message), client_with_message)

                            # принимаем сообщения
                        except:
                            self.all_clients.remove(client_with_message)

                for message in self.message:
                    try:
                        # print('Process_message try')
                        self.process_message(message, send_data_lst)
                    except:
                        self.all_clients.remove(self.name[message[DESTINATION]])
                        del self.name[message[DESTINATION]]
                self.message.clear()
        except:
            pass

    def process_client_message(self, message, client):
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            if message[USER][ACCOUNT_NAME] not in self.name.keys():
                self.name[message[USER][ACCOUNT_NAME]] = client
                print('---')
                client_ip, client_port = client.getpeername()
                user = message[USER][ACCOUNT_NAME]
                print('Username -- ', user)
                # print(client_ip, client_port)
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                print('----')
                send_msg_finish(client, RESPONCE_200)
            else:
                responce = RESPONCE_400
                responce[ERROR] = 'Имя занято'
                send_msg_finish(client, responce)
                self.all_clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
            self.message.append(message)
            return
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.database.user_logout(message[ACCOUNT_NAME])
            self.all_clients.remove(self.name[ACCOUNT_NAME])
            self.name[ACCOUNT_NAME].close()
            del self.name[ACCOUNT_NAME]
            return
        # Запрос контак листа
        elif ACTION in message and message[ACTION] == GET_CONTACT and SENDER in message:
            # self.database.contact_list(message[SENDER])
            print('Запрос контакт листа ----')
            print('----')
            RESPONCE_202[RESPONCE] = 202
            RESPONCE_202[DATA] = self.database.contact_list(message[SENDER])
            print('-----')
            send_msg_finish(client, RESPONCE_202)
            print('----')


        # Добавление в контакт лист
        elif ACTION in message and message[ACTION] == ADD_CONTACT and SENDER in message and USER_ID_TO_CONTACT in message:
            print('Запрос на добавление в контакт лист')
            self.database.add_contact(message[SENDER], message[USER_ID_TO_CONTACT])
            print('---')
            CUSTOM_RESPONCE[RESPONCE] = 500
            CUSTOM_RESPONCE[DATA] = 'OK'
            print(CUSTOM_RESPONCE)
            send_msg_finish(client,CUSTOM_RESPONCE )
            print('-------')
            # send_msg_finish(client, RESPONCE_200)


        else:
            response = RESPONCE_400
            response[ERROR] = 'Запрос некорректен'
            send_msg_finish(client, response)


    def process_message(self, message, listen_socket):
        if message[DESTINATION] in self.name and self.name[message[DESTINATION]] in listen_socket:
            send_msg_finish(self.name[message[DESTINATION]], message)
            print(f'Отправлено сообщение пользователю {message[DESTINATION]} от {message[SENDER]}')
        else:
            print(f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере')

def main():
    database = ServerStorage()
    listen_address, listen_port = arg_parce()
    server = ServerClass(listen_address, listen_port, database)
    # server.daemon = True
    # server.start()
    server.mainlopp()

if __name__ == '__main__':
    main()
