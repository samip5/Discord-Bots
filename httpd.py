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

	server_address = ('0.0.0.0', 8000)
	httpd = HTTPServer(server_address,testHTTPServer_RequestHandler)
	print('running server....')
	httpd.serve_forever()


run_httpd()