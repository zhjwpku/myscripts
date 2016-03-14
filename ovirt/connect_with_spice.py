#!/usr/bin/python

import os
import ovirtsdk.api
import ovirtsdk.xml
import subprocess
import tempfile
import urllib

# The parameters to connect to the engine:
engine_host = "192.168.1.112"
engine_port = 443
engine_user = "admin@internal"
engine_password = "mprc"

# The name of the vm:
vm_name = "ubuntu14.04"

# A template to generate the viewer connection file:
config_template = """\
[virt-viewer]
type={type}
host={host}
port={port}
password={password}
tls-port={tls_port}
fullscreen=0
title={title}
enable-smartcard=0
enable-usb-autoshare=1
delete-this-file=1
usb-filter=-1,-1,-1,-1,0
tls-ciphers=DEFAULT
host-subject={tls_subject}
ca={ca}
toggle-fullscreen=shift+f11
release-cursor=shift+f12
secure-channels=main;inputs;cursor;playback;record;display;usbredir;smartcard
"""

# Connect to the API:
api_url= "https://{host}:{port}/api".format(
	host=engine_host,
	port=engine_port
)

api = ovirtsdk.api.API(
	url=api_url,
	username=engine_user,
	password=engine_password,
	insecure=True
	#debug=True
)

# Download the CA certificate, as we need to pass this to the viewer so that
# it will trust the SSL certificate of the host:
#ca_url = "https://{host}:{port}/ca.crt".format(
#	host=engine_host,
#	port=engine_port
#)
#print ca_url
#ca_path, _ = urllib.urlretrieve(ca_url)
#print "end"
#with open(ca_path, "r") as ca_file:
#	ca_content = ca_file.read()
ca_content = """-----BEGIN CERTIFICATE-----\nMIIDqzCCApOgAwIBAgICEAAwDQYJKoZIhvcNAQEFBQAwQDELMAkGA1UEBhMCVVMxETAPBgNVBAoT\nCG15ZG9tYWluMR4wHAYDVQQDExVteWhvc3QubXlkb21haW4uNDA0NjYwHhcNMTUxMTE3MTA0OTE4\nWhcNMjUxMTE1MTA0OTE4WjBAMQswCQYDVQQGEwJVUzERMA8GA1UEChMIbXlkb21haW4xHjAcBgNV\nBAMTFW15aG9zdC5teWRvbWFpbi40MDQ2NjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\nANHhXIrZnyNwIDcZjqD6C3t0zYzuqVqNsovQKxzVC2XmU0KDbswBBGVQNI8yQWyBCsxXfi7jjHa0\nFDBH1ph3qmLVOYO4MunR5L3qz8ngi5vqNZ9/oHKZ6VZ5OZiVuvqmShOYCtCcRmK4pNG7bmDtn4sy\nQPtArAY8j/Eoa9M+LiK9UMTCFC3/4lb6AvduCm6exlbeULZjU49KgDzjYPqp19YpKTGJuwxthRaq\nZNkU37NAEuyHJhX01ApQwB3aSAoZHP2E63bFxO50qAQ4jd5s3szcP6J8mj/SvKoxKFY7XNSI0HLt\nRC0M8wkmDwUdy4mErKaav2ycUBK9MNiWWS0OThsCAwEAAaOBrjCBqzAdBgNVHQ4EFgQU64nZkWCA\nMxmnOwBW0rgfmCE45oUwaQYDVR0jBGIwYIAU64nZkWCAMxmnOwBW0rgfmCE45oWhRKRCMEAxCzAJ\nBgNVBAYTAlVTMREwDwYDVQQKEwhteWRvbWFpbjEeMBwGA1UEAxMVbXlob3N0Lm15ZG9tYWluLjQw\nNDY2ggIQADAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBBjANBgkqhkiG9w0BAQUFAAOC\nAQEAeXsbB2ZTinWrEOqafYm6fCUUU37QJ254BQKGTnF4MEw3oOBiBkz7BZoclmSYTmLMUbGRUQVx\nZgmDfGPWuYd8X9re5OgmQhX5RBOWYPnTJR/89EQo6YV1eZS7QraEPn2ULyYXdzoqvcnIs67dHUZX\nGWggn3+oev68HfRvFwhnIwQ2vArwOLkhtgDfxPb9cSwMvqS/q1trcHepmIdxwh8XXABFiSzaIpQB\n4eZk738HocoQlFdLZX0Lki8WDK+omnal3sNOsyMROrWdUALDw28+eIkFSRtFbPQXlE5jnwM6WCe0\n6rlYqUJKDvI3Tll71SFpvJhSMbKqel6PGbfHnXEERw==\n-----END CERTIFICATE-----\n"""

ca_content = ca_content.replace("\n", "\\n")

# Find the VM and get the display details:
vm = api.vms.get(name=vm_name, all_content=True)
display = vm.get_display()

# Request a ticket for the display of the VM:
ticket_result = vm.ticket()
ticket = ticket_result.get_ticket()

# Create the viewer configuration:
config_content = config_template.format(
	type=display.get_type(),
	host=display.get_address(),
	port=display.get_port(),
	password=ticket.get_value(),
	tls_port=display.get_secure_port(),
	title=vm_name,
	tls_subject=display.get_certificate().get_subject(),
	ca=ca_content
)

config_fd, config_path = tempfile.mkstemp()
with os.fdopen(config_fd, "w") as config_file:
	config_file.write(config_content)

# Run the viewer:
subprocess.call(["remote-viewer", config_path])
