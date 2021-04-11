import subprocess
import netifaces

class PingSweeper:

	def __init__(self):
		self.host_address = netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr']

	def sweep(self, ip):
		try:
			output = subprocess.check_output("ping {} -c 1".format(ip), shell=True, universal_newlines=True)
			packets_recieved = int(output.split("\n")[4].split(",")[1].split(" ")[1])
			if packets_recieved == 1:
				return ip
			return False

		except subprocess.CalledProcessError as e:
			return False

	def mass_sweep(self, start_ip):
		base_address = ".".join(start_ip.split(".")[0:3]) + "."
		next_ip = start_ip
		device = int(next_ip.split(".")[-1])
		while device < 255:
			device += 1

			if next_ip == self.host_address:
				next_ip = base_address + str(device)
				continue

			sweep_result = self.sweep(next_ip)
			if sweep_result:
				return "VM:{}".format(sweep_result)

			next_ip = base_address + str(device)
		return "No VMs were found on scan."
