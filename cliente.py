import socket
import struct
import time
import sys

server     = ("127.0.0.1", 123)
bufferSize = 1024
TIME1970   = 2208988800


def sntp_client():
    li = '00'
    vn = '011'
    mode = '011'
    primerByte = li + vn + mode
    primerByte = str(hex(int(primerByte, 2)))[1:]

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = '\\' + primerByte + 47 * '\0'
    print(data.encode('utf-8'))
    client.sendto(data.encode('utf-8'), server)
    data, address = client.recvfrom(1024)
    # if data: print('Response received from:', address)
    # t = struct.unpack('!12I', data)[10] - TIME1970
    # print('\tTime = %s' % time.ctime(t))

    print(time.ctime(float(str(data)[2:-1]) - TIME1970))

if __name__ == '__main__':
    sntp_client()
