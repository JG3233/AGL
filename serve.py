# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

hostName = "192.168.1.18"
serverPort = 9999
magic_bytes = "hacked"
is_port_open = True

class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        if self.path == '/' + magic_bytes:
            print('Secret path discovered!')
            close_my_port()
        if self.path == '/reopen':
            print('Server restored')
            open_my_port()

def close_my_port():
    global is_port_open
    if is_port_open:
        os.popen('iptables -I INPUT -p tcp --dport 7777 -j REJECT')
        is_port_open = False
        print('Port closed')

def open_my_port():
    global is_port_open
    if not is_port_open:
        os.popen('iptables -I INPUT -p tcp --dport 7777 -j ACCEPT')
        is_port_open = True
        print('Port opened')

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")