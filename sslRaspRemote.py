#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import BaseHTTPServer
import base64
import json
import os
import re
import ssl
import sys
import time
from SimpleHTTPServer import SimpleHTTPRequestHandler

key = ""
init_ir_send = "irsend -d /run/lirc/lircd-lirc0 SEND_ONCE "
init_rf_send = "python3 /usr/bin/rfsend.py -p 180 -t 1 "


class AuthHandler(SimpleHTTPRequestHandler):
    # Main class to present web pages and authentication.

    def execute(self, command):
        print(command)
        result = os.system(command)
        self.wfile.write(json.dumps({"Command":result}))

    def do_HEAD(self):
        print "Send header"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "Send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        ''' Present front page with user authentication. '''
        if self.headers.getheader('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write('No auth header received')
            pass
        elif self.headers.getheader('Authorization') == 'Basic ' + key:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if re.match('/AAProKlima/', self.path) is not None:
                send_command = init_ir_send + "AAProKlima " + self.path[12:]
                self.execute(send_command)
            elif re.match('/AAKaysun/', self.path) is not None:
                send_command = init_ir_send + "AAKaysun " + self.path[10:]
                self.execute(send_command)
            elif re.match('/HBathroom/', self.path) is not None:
                send_command = init_rf_send + self.path[11:]
                self.execute(send_command)
            elif re.match('/Pruebas/', self.path) is not None:
                send_command = init_rf_send + self.path[9:]
                print send_command
            elif re.match('/exitprogram/', self.path) is not None:
                self.wfile.write(json.dumps({"Exit": 0}))
                time.sleep(1)
                print "Exiting"
                sys.exit(0)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('Not authenticated')
            pass


def create_server(port, password):
    global key
    key = base64.b64encode(password)
    httpd = BaseHTTPServer.HTTPServer(('', port), AuthHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                                   # certfile='/home/osmc/ewolvy.mooo.com.pem',
                                   # keyfile='/home/osmc/ewolvy.mooo.com.private.pem',
                                   certfile='./ewolvy.mooo.com.pem',
                                   keyfile='./ewolvy.mooo.com.private.key',
                                   ssl_version=ssl.PROTOCOL_TLSv1)
    httpd.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage sslRaspRemote.py [port] [username:password]"
        sys.exit()
    create_server(int(sys.argv[1]), sys.argv[2])
