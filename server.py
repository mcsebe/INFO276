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
    except struct.error:
        pass
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

def changeData(valores, llegada):
    valores['Leap Indicator'] = 0
    valores['Stratum'] = 1
    if (valores['Mode'] == 3): valores['Mode'] = 4 
    else: valores['Mode'] = 2
    valores['Root Delay'] = float(0)
    valores['Root Dispersion'] = float(0)
    valores['Reference Clock Identifier'] = 0 #Si no se especifica
    valores['Receive Timestamp'] = llegada
    valores['Transmit Timestamp'] = time.time() + TIME1970

def packed_Data(valores):
    try:
        packed = struct.pack("!B B B b 11I", (valores['Leap Indicator'] << 6 | valores['Version Number'] << 3 | valores['Mode']),
                    valores['Stratum'],
                    valores['Poll Interval'],
                    valores['Precision'],                              
                    int(valores['Root Delay']) << 16 | int(abs(valores['Root Delay'] - int(valores['Root Delay'])) * 2**16),
                    int(valores['Root Dispersion']) << 16 | int(abs(valores['Root Dispersion'] - int(valores['Root Dispersion'])) * 2**16),
                    valores['Reference Clock Identifier'],
                    int(valores['Reference Timestamp']),
                    int(abs(valores['Reference Timestamp'] - int(valores['Reference Timestamp'])) * 2**32),
                    int(valores['Originate Timestamp']),
                    int(abs(valores['Originate Timestamp'] - int(valores['Originate Timestamp'])) * 2**32),
                    int(valores['Receive Timestamp']),
                    int(abs(valores['Receive Timestamp'] - int(valores['Receive Timestamp'])) * 2**32),
                    int( valores['Transmit Timestamp']),
                    int(abs( valores['Transmit Timestamp'] - int( valores['Transmit Timestamp'])) * 2**32)
                    )   
    except struct.error:
        pass
    return packed   

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
            llegada = time.time() + TIME1970
            print("Link bussy")

            valores = unpackData(data)
            print(valores)
            # Sending a reply to client
            changeData(valores, llegada)
            print(valores)

            packed_val = packed_Data(valores)

            UDPServerSocket.sendto(packed_val, address)
            print("Link Available")
        except:
            pass

if __name__ == '__main__':
    sntp_server()

