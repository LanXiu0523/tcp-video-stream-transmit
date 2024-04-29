#-*- coding: UTF-8 -*- 

import socket
import cv2
import time
import numpy as np

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)


tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(SERVER_ADDRESS)

tcp_server.listen(1)

while True:
    print("Waiting for client TCP connection...")
    client_socket, client_address = tcp_server.accept()
    tcp_client_address = client_address[0] + ":" + str(client_address[1])
    print(tcp_client_address + " connection established!")
    
    try:
        while True:
            data_digest = client_socket.recv(1024)
            if data_digest:
                client_socket.send(b"ok")
                data_digest = data_digest.decode().split(",")
                data_len = int(data_digest[0])

                data_cnt = 0
                data = b""

                while data_cnt < data_len:
                    data_segment = client_socket.recv(256000)
                    data += data_segment
                    data_cnt += len(data_segment)
                    print("Received from " + tcp_client_address + " : " + str(data_cnt) + "/" + data_digest[0])
                client_socket.send(b"ok")


                img = np.asarray(bytearray(data), dtype="uint8")
                img = cv2.imdecode(img, cv2.IMREAD_COLOR)
                cv2.imshow("img", img)
                cv2.waitKey(500)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
            else:
                print("closed!")
                break
    finally:
        client_socket.close()