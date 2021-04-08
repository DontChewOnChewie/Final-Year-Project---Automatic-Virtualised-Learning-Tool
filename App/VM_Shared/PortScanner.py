import socket
from optparse import OptionParser

class PortScanner:

	def __init__(self, target, verbose, maxport):
		self.target = target
		self.verbose = verbose
		self.maxport = int(maxport)

	def full_scan(self):
		for i in range(1, self.maxport):
			try:
				if self.verbose:
					print("Attempting connection to {} on port {}.".format(self.target, str(i)))

				soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				soc.connect((self.target, i))
				print("Port {} on {} is open.".format(str(i), self.target))
				soc.settimeout(10)

				soc.send("data".encode()) if i != 80 else soc.send("GET /\r\n".encode())
				data = soc.recv(1024)
				print(data.decode())

			except ConnectionRefusedError:
				if self.verbose:
					print("Port {} for {} is not open.".format(str(i), self.target))
			except UnicodeDecodeError:
				print("{}\n".format(data))
			except ConnectionResetError:
				print("Port {} reset connection.".format(str(i)))
			except socket.timeout:
				print("Couldn't retrieve headers for port {}, timed out.".format(str(i)))
			finally:
				soc.close()

		print("Scan completed, {} ports were scanned.".format(self.maxport))


if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-t", "--target", dest="target")
	parser.add_option("-p", "--maxport", dest="maxport", default=1025)
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Show more details.", default=False)

	(options, args) = parser.parse_args()
	if not options.target:
		print("You must include a target target! e.g. python3 PortScanner.py -t 192.168.1.1")
		exit()

	try:
		int(options.maxport)
	except:
		print("ERROR : -p or --maxport should be a number, '{}' is not valid.".format(options.maxport))
		exit()

	ps = PortScanner(options.target, options.verbose, options.maxport)
	ps.full_scan()
