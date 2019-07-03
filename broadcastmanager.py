#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# Broadcast manager is intended to use in a Raspberry Pi to send server information for different services
# controlled by Android applications created by Juanjo Soriano for personal use and distributed
# as is without any warranty and full freedom for reuse the code, change it, distribute it or do whatever
# you want, as long as it's kept free (both in money cost and rights for the user).

import socket

# Define the timeout for the sockets. Advice to 10 seconds
import sys

TIMEOUT = 10
# Define the UDP and TCP port
PORT = 19103

# Define RealRemote Data to be sent, JSON formatted
REAL_REMOTE = ('{"META":{'
               '"FieldCount":6,'
               '"Fields":["Name","Brand","Address","Port","Alias","Description"],'
               '"Description":"Salón en Sa Ràpita"'
               '},'
               '"RealRemote":{'
               '"Name":"Salón",'
               '"Brand":0,'
               '"Address":"https://ewolvy.mooo.com",'
               '"Port":1207,'
               'Alias":"AAKaysun",'
               'Description":"Salón en Sa Ràpita"}'
               '}\n')

# Define Youtube Data to be sent, JSON formatted
YOUTUBE = ('{"META":'
           '{"FieldCount":5,'
           '"Fields":["Name","Address","Port","Alias","Description"],'
           '"Description":"Salón en Sa Ràpita"'
           '},'
           '"YTToPi":{'
           '"Name":"Salón",'
           '"Address":"192.168.1.251",'
           '"Port":21603,'
           '"Alias":"YTToPi",'
           '"Description":"Salón en Sa Ràpita"}'
           '}\n')

# Define CloseKodi Data to be sent, JSON formatted
CLOSE_KODI = ('{"META":{'
              '"FieldCount":5,'
              '"Fields":["Name","Address","Port","Alias","Description"],'
              '"Description":"Salón en Sa Ràpita"'
              '},'
              '"CloseKodi":{'
              '"Name":"Salón",'
              '"Address":"https://ewolvy.mooo.com",'
              '"Port":1207,'
              '"Alias":"CloseKodi",'
              '"Description":"Salón en Sa Ràpita"}'
              '}\n')

# Define RaspRemote Data to be sent, JSON formatted
RASP_REMOTE = ('{"META":{'
               '"ObjectCount":3,'
               '"ObjectNames":["AirConditioner","Heater","Pruebas Palma"]'
               '},'
               '"AirConditioner":{'
               '"Name":"AA Salón",'
               '"Type":0,'
               '"Address":"https://ewolvy.mooo.com",'
               '"Port":1207,'
               '"Alias":"AAKaysun",'
               '"Description":"Aire acondicionado en salón de Sa Ràpita"'
               '},'
               '"Heater":{'
               '"Name":"Calefactor",'
               '"Type":3,"Address":"https://ewolvy.mooo.com",'
               '"Port":1207,'
               '"Alias":"HBathroom",'
               '"Description":"Calefactor en salón de Sa Ràpita"'
               '},'
               '"Pruebas Palma":{'
               '"Name":"Pruebas Palma",'
               '"Type":3,"Address":"https://192.168.1.230",'
               '"Port":1207,'
               '"Alias":"Pruebas",'
               '"Description":"Pruebas en Palma"'
               '}}\n')


# Function to create or get the socket:
# Params:
#   from_fd: if set to True, will get the socket from File Descriptor handled by Linux Daemon
#            if set to False, will create a new socket for all interfaces (intended for debugging and testing only)
def create_udp_socket(from_fd):
    if from_fd:
        new_socket = socket.fromfd(3, socket.AF_INET, socket.SOCK_DGRAM)
    else:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = ('', PORT)
        new_socket.bind(address)
    new_socket.settimeout(TIMEOUT)
    return new_socket


# Function to create a TCP socket:
def create_tcp_socket(address):
    print address
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.connect(address)
    new_socket.settimeout(TIMEOUT)
    return new_socket


if __name__ == "__main__":
    isOnLinux = True
    if sys.argv[1] == '0':
        isOnLinux = False
    getSocket = create_udp_socket(isOnLinux)  # True unless specified 0 on command line as first parameter
    try:
        data, contactAddress = getSocket.recvfrom(1024)
        sendSocket = create_tcp_socket((contactAddress[0], 19103))
        if data == "BROADCAST_REALREMOTE":
            sent = sendSocket.sendto(REAL_REMOTE, contactAddress)
            if sent > 0:
                print "Sent RealRemote data to " + contactAddress[0] + " on port 19103"
        elif data == "BROADCAST_YTTOPI":
            sent = sendSocket.sendto(YOUTUBE, contactAddress)
            if sent > 0:
                print "Sent Youtube data to " + contactAddress[0] + " on port 19103"
        elif data == "BROADCAST_CLOSEKODI":
            sent = sendSocket.sendto(CLOSE_KODI, contactAddress)
            if sent > 0:
                print "Sent CloseKodi data to " + contactAddress[0] + " on port 19103"
        elif data == "BROADCAST_RASPREMOTE":
            sent = sendSocket.sendto(RASP_REMOTE, contactAddress)
            if sent > 0:
                print "Sent RaspRemote data to " + contactAddress[0] + " on port 19103"
        else:
            print "No correct data: " + data
        sendSocket.close()
    except socket.timeout:
        print "Timeout after " + TIMEOUT.__str__() + " seconds"
        exit(1)
    getSocket.close()
