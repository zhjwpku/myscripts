#!/usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params

def main():
	URL = 'https://192.168.1.112:443/api'
	USERNAME = 'admin@internal'
	PASSWORD = 'mprc'
	api = API(url=URL, username=USERNAME, password=PASSWORD, insecure=True)
	vm = api.vms.get(name="ubuntu14.04")
	print vm.name
	#vm_list = api.vms.list()
	#for vm in vm_list:
	#	print vm.name
	api.disconnect()

if __name__ == '__main__':
	main()
