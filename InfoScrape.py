#!/usr/bin/python3

#1. Read list of IPs
#2. Query IPs to RDAP/whois
#  a. Output to Owner/Location in CSV with IP Information
#3. Query DNS for IPs
#  a. Output with IP/hostnames to CSV
#4. Port scan
#  a. Output to CSV with IP
#5. HTTP response codes to CSV with IP
#  a. curl?
#6. Scrape web content?
import sys
import os
import socket
from ipwhois import IPWhois
from pprint import pprint

ip_file = sys.argv[1]

with open(ip_file) as x:
    content = x.read().splitlines()
for line in content:
    obj = IPWhois(line)
    results = obj.lookup_rdap(depth=1)
    pprint(results)
