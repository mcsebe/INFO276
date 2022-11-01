import socket
import time
import datetime
import struct

localIP     = "127.0.0.1"
localPort   = 123
bufferSize  = 1024
TIME1970   = 2208988800

# https://docs.python.org/3/library/struct.html
def unpackData(data):
        try:
            unpacked = struct.unpack("!B B B b 11I", data[0:48])
            print(unpacked)
        except struct.error:
            pass
        #  00011011
        valores = {}
        valores['Leap Indicator'] = unpacked[0] >> 6 & 0x3
        valores['Version Number'] = unpacked[0] >> 3 & 0x7
        valores['Mode'] = unpacked[0] & 0x7
        valores['Stratum'] = unpacked[1]
        valores['Poll Interval'] = unpacked[2]
        valores['Precision'] = unpacked[3]
        valores['Root Delay'] = float(unpacked[4])/2**16
        valores['Root Dispersion'] = float(unpacked[5])/2**16
        valores['Reference Clock Identifier'] = unpacked[6]
        valores['Reference Timestamp'] = unpacked[7] + float(unpacked[8])/2**32
        valores['Originate Timestamp'] = unpacked[9] + float(unpacked[10])/2**32
        valores['Receive Timestamp'] = unpacked[11] + float(unpacked[12])/2**32
        valores['Transmit Timestamp'] = unpacked[13] + float(unpacked[14])/2**32

        return valores

# Listen for incoming datagrams
def sntp_server():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    print("Link Available")
    while(True):
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            data = bytesAddressPair[0]
            address = bytesAddressPair[1]
            print("Link bussy")
            print(data)
            valores = unpackData(data)
            print(valores)
            # Sending a reply to client

            tiempo = time.time() + TIME1970
            print(tiempo)
            UDPServerSocket.sendto(str.encode(str(tiempo)), address)
            print("Link Available")
        except:
            pass

if __name__ == '__main__':
    sntp_server()

