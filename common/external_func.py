from common.vars import ENCODE_LANG, MAX_LENG
import json
from common.vars import ENCODE_LANG



def get_message(client):
    # print('get_message_func ')
    encode_resp = client.recv(MAX_LENG)
    # print('WAit')
    if isinstance(encode_resp, bytes):
        json_resp = encode_resp.decode(ENCODE_LANG)
        resp = json.loads(json_resp)
        if isinstance(resp, dict):
            # print('message is getting')
            return resp
        else:
            print('Error')
    else:
        print('Incorrect Data from get_message')





def send_msg_finish(socket, msg):
    print('Sending message..')
    if not isinstance(msg, dict):
        raise print('ERROR DICT SEND MSG')
    js_msg = json.dumps(msg)
    encode_msg = js_msg.encode(ENCODE_LANG)
    socket.send(encode_msg)
    print('Send OK')
