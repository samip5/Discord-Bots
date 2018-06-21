import os

from http.server import BaseHTTPRequestHandler, HTTPServer


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		return

	def do_HEAD(self):
		return

	def do_POST(self):
		return


def run_httpd():
	print('Starting HTTPD server....')

	port = int(os.environ.get('PORT', 5000))
	server_address = ('0.0.0.0', port)
	httpd = HTTPServer(server_address,testHTTPServer_RequestHandler)
	httpd.serve_forever()


run_httpd()