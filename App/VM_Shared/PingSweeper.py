import subprocess
import netifaces
from optparse import OptionParser

class PingSweeper:

	def __init__(self, outfile, verbose):
		self.host_address = netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr']
		self.outfile = outfile
		self.verbose = verbose

	def write_to_file(self, file, ip):
		with open(file, 'w', encoding='utf-8') as ip_file:
			ip_file.write("\nPotential target {} found.".format(ip))

	def sweep(self, ip):
		try:
			output = subprocess.check_output("ping {} -c 1".format(ip), shell=True, universal_newlines=True)
			packets_recieved = int(output.split("\n")[4].split(",")[1].split(" ")[1])
			if packets_recieved == 1:
				print("{} is up.".format(ip))
				if self.outfile:
					self.write_to_file(self.outfile, ip)

		except subprocess.CalledProcessError as e:
			if self.verbose:
				print("{} is unresponsive.".format(ip))

	def mass_sweep(self, start_ip):
		base_address = ".".join(start_ip.split(".")[0:3]) + "."
		next_ip = start_ip
		device = int(next_ip.split(".")[-1])
		while device < 255:
			device += 1

			if next_ip == self.host_address:
				if self.verbose:
					print("Skipping host address {}".format(self.host_address))
				next_ip = base_address + str(device)
				continue

			self.sweep(next_ip)
			next_ip = base_address + str(device)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-o", "--outfile", dest="outfile", help="Path of file for data to be outputted.")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Show more details.", default=False)
	(options, args) = parser.parse_args()

	ps = PingSweeper(options.outfile, options.verbose)
	ps.mass_sweep("10.10.10.4")
