import socket
import struct
import time
import sys

server     = ("127.0.0.1", 123)
bufferSize = 1024
TIME1970   = 2208988800


def to_data(li = 0, vn = 3, mode = 3):
    try:
        packed = struct.pack("!B",
            (li << 6 | vn << 3 | mode))
    except struct.error:
        pass
    return packed

def sntp_client():
    li = 0
    vn = 3
    mode = 3
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sig = 47 * '\0'
    sig = sig.encode('utf-8')
    data = to_data(li, vn, mode) + sig
    client.sendto(data, server)
    data, address = client.recvfrom(1024)
    # if data: print('Response received from:', address)
    # t = struct.unpack('!12I', data)[10] - TIME1970
    # print('\tTime = %s' % time.ctime(t))

    print(time.ctime(float(str(data)[2:-1]) - TIME1970))

if __name__ == '__main__':
    sntp_client()
