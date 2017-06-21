from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import html

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
    # GET
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(self.path[1:],'rb') 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: {}'.format(self.path))
        return
        
    def do_POST(self):
        content_len=int(self.headers.get('content-length',0))
        post_body = self.rfile.read(content_len)
        post_body = post_body.decode()
        post_body = html.escape(post_body)
        self.send_message(post_body)
    
    def send_message(self,message):
        self.wfile.write(bytes(message, "utf8"))
 
def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()
 
 
run()
