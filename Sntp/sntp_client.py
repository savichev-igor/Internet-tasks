# !/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import struct
import time

HOST = "127.0.0.1"
PORT = 123

FORMAT = "BBBBII4sQQQQ"

TIME1970 = 2208988800  # Thanks to F.Lundh


class Client():

    def __init__(self):
        self.packet = struct.Struct(FORMAT)
        self.s = socket.create_connection((HOST, PORT), 3.0)

    def send_request(self):
        packet_bin = self.packet.pack(0b00100011, 0, 0, 0, 0, 0, b'Hi',
                                      0, 0, 0, self.get_time())
        self.s.sendall(packet_bin)

    def get_reply(self):
        answer_packet_bin = self.s.recv(1024)
        # t4 = self.get_time()  # Время приёма пакета клиентом
        # t1 = self.packet.unpack(answer_packet_bin)[8]  # Начальн. отпр. кл-ом
        # t2 = self.packet.unpack(answer_packet_bin)[9]  # Приём сервером
        t3 = self.packet.unpack(answer_packet_bin)[10]  # Отправка сервером
        self.s.close()
        # print(self.get_offset(t1, t2, t3, t4))
        return time.ctime(self.get_normal_time(t3))
        # return time.ctime(self.get_normal_time(t3) -
        #                   self.get_offset(t1, t2, t3, t4))

    def get_time(self):
        t = int((time.time() + TIME1970) * 2**32)
        return t

    def get_normal_time(self, t):
        t = (t // 2**32) - TIME1970
        return t

    def get_offset(self, t1, t2, t3, t4):
        """ В этой функции мы высчитываем поправку
            исходя из всем известной формулы t = ((t2 - t1) + (t3 - t4)) // 2
        """
        t1 = self.get_normal_time(t1)
        t2 = self.get_normal_time(t2)
        t3 = self.get_normal_time(t3)
        t4 = self.get_normal_time(t4)
        return ((t2 - t1) + (t3 - t4)) // 2


def main():
    A = Client()
    A.send_request()
    time = A.get_reply()
    print(time)

if __name__ == "__main__":
    main()
