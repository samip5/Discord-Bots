import os

from http.server import BaseHTTPRequestHandler, HTTPServer


class samip537FunHTTPServer_RequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		rootdir = os.getcwd()
		try:
				f = open(rootdir + "\index.html")

				self.send_response(200)
				self.send_header('Contet-type', 'text/html')
				self.end_headers()

				self.wfile.write(bytes(f.read(), "utf8"))
				f.close()
				return
		except IOError:
			self.send_error(404, 'file not found')

	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Contet-type', 'text/html')
		self.end_headers()
		return


def run_httpd():
	print('Starting HTTPD server....')

	port = int(os.environ.get('PORT', 8080))
	server_address = ('0.0.0.0', port)
	httpd = HTTPServer(server_address, samip537FunHTTPServer_RequestHandler)
	httpd.serve_forever()


run_httpd()
