#-*- coding: UTF-8 -*- 

import socket
import os
import cv2
import time
import socket


IMG_PATH = './output'
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)
GAP_TIME = 500



def img_list(dir):
    files = [os.path.join(dir, file) for file in os.listdir(dir)]
    files_sorted = sorted(files, key=os.path.getmtime, reverse=True)
    return files_sorted


tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(SERVER_ADDRESS)

while True:
    start = time.perf_counter()

    img = cv2.imread(img_list(IMG_PATH)[0])
    img_encode = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 99])[1]
    data = img_encode.tostring()
    data_digest = (str(len(data))).encode() + ",".encode() + " ".encode()

    tcp_client.send(data_digest)
    recv_status_code = tcp_client.recv(1024)
    if ("ok" == recv_status_code.decode()):
        tcp_client.send(data)
    recv_status_code = tcp_client.recv(1024)
    if ("ok" == recv_status_code.decode()):
        print("Image TCP Transmission Latency: " + str(int((time.perf_counter() - start) * 1000)) + "ms")
    
    time.sleep(GAP_TIME / 1000)
