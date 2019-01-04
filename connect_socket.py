import socket
import json

HOST = socket.gethostname()
PORT = 27015
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def act_10(gw_id ):         #get log
    s.connect((HOST, PORT))
    show_ui = json.dumps({"Action" : 10, "Gateway_ID" : int(gw_id )})
    s.send(show_ui.encode("utf-8"))
    s.close()

def act_21(gw_id, ssid):    #change ssid
    s.connect((HOST, PORT))
    show_ui = json.dumps({"Action" : 21, "Gateway_ID" : int(gw_id ), "new_SSID" : ssid})
    s.send(show_ui.encode("utf-8"))
    s.close()

def act_23(gw_id, encry):   #change encryption type
    s.connect((HOST, PORT))
    show_ui = json.dumps({"Action" : 23, "Gateway_ID" : int(gw_id ), "Encryption" : encry})
    s.send(show_ui.encode("utf-8"))
    s.close()

def act_24(gw_id, key):     #change encryption key
    s.connect((HOST, PORT))
    show_ui = json.dumps({"Action" : 24, "Gateway_ID" : int(gw_id ), "Key" : key})
    s.send(show_ui.encode("utf-8"))
    s.close()

if __name__ == '__main__':
    print("blabla")