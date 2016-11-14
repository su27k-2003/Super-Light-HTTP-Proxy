#usr/bin/python
# -*- coding: UTF-8 -*-

## Authors Leo Liu, liuqi.au@gmail.com
## Version v1.0


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import urllib
import urlparse

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        url = self.path
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        path = rest
        host, port = urllib.splitnport(host)

        if port < 0: port = 80

        ip = socket.gethostbyname(host)

        del self.headers['Proxy-Connection']
        self.headers['Connection'] = 'close'

        send_data = 'GET ' + path + ' ' + self.protocol_version + '\r\n'
        head = ''

        for key, val in self.headers.items():
            head = head + "%s: %s\r\n" % (key, val)

        send_data = send_data + head + '\r\n'
        print send_data
        
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.connect((ip, port))
        so.sendall(send_data)

        data = ''
        while 1:
            try:
                buf = so.recv(8129)
                data += buf
            except:
                buf = None
            finally:
                if not buf:
                    so.close()
                    break
                    
        self.wfile.write(data)
     

def main():
    try:
        server = HTTPServer(('', 8888), Handler)
        print 'Welcome to the Super light HTTP Proxy.'
        print 'Waiting for connection...'
        server.serve_forever()
    except KeyboardInterrupt:
        print ''
        print 'Shutting down...'
        server.socket.close()

if __name__ == '__main__':
    main()