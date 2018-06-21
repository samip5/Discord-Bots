import os

from http.server import BaseHTTPRequestHandler, HTTPServer

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

	def do_get(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		message = "Hello world!"
		self.wfile.write(bytes(message, "utf8"))
		return


def run_httpd():
	print('Starting HTTPD server....')

	port = int(os.environ.get('PORT', 5000))
	server_address = ('0.0.0.0', port)
	httpd = HTTPServer(server_address,testHTTPServer_RequestHandler)
	httpd.serve_forever()


run_httpd()