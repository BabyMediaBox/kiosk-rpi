import os
import sys
import json
import serial
import requests
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse

if not os.path.exists('config.json'):
    print('Missing config.json')
    sys.exit()

serialEnabled=False
serverUri="http://localhost:4010"
PORT=3030
httpd=False
soundDevice="Master"

def rgb(r, g, b):
    global ser
    print("R", r, "G", g, "B", b)
    if serialEnabled:
        ser.write(bytes(r+","+g+","+b))

class httpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            self.wfile.write(b'ok')
            return

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', serverUri)
        """Send the blank line ending the MIME headers."""
        if self.request_version != 'HTTP/0.9':
            self._headers_buffer.append(b"\r\n")
            self.flush_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        print('options')
        return

    def do_POST(self):
        print("self.path", self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == '/rgb':
            content_length = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_length)
            params = parse.parse_qs(post_body.decode('utf-8'))
            rgb(params['r'][0], params['g'][0], params['b'][0])
            return

        elif self.path == '/volume':
            content_length = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_length)
            params = parse.parse_qs(post_body.decode('utf-8'))
            print("volume", params['volume'])

            subprocess.call(["amixer", "set", soundDevice, params['volume'][0].strip()])

            return
        elif self.path == '/shutdown':
            subprocess.call(["sudo", "shutdown", "-h", "now"])
            return

try:
    with open('config.json') as f:
        Config = json.load(f)
        PORT=int(Config['port'])
        soundDevice=Config['soundDevice']
        serverUri=Config['server']
        serialEnabled=Config['serialEnabled']

        vol=subprocess.check_output(["./getVolume.sh", soundDevice])
        result = requests.post(serverUri+'/kiosk-volume', data={'volume': vol.decode('utf-8').replace('%','')})

        if serialEnabled:
            ser = serial.Serial(Config['serialDevice'], int(Config['serialPort']), timeout=0.5)

        httpd = HTTPServer(('localhost', PORT), httpHandler)
        print('listening on localhost:',PORT)
        httpd.serve_forever()

except:
    try:
        print("Main exception", sys.exc_info())
    except:
        print('httpd was not started', sys.exc_info())

