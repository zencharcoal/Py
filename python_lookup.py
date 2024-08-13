#!/usr/bin/python3
'''
]
Requirments:
nslookup
grep
cut
python3

'''
import os
import sys

#Open the file provided, catch exceptions
if len(sys.argv) > 1:
    try:
        iplist = open(sys.argv[1],'r')
    except:
        print("Error opening file, make sure it exists and you have permission.")
        sys.exit()
else:
    iplist = open('$1','r')

mylist = []
fqdn = []
dns1 = "8.8.8.8"
dns2 = "1.1.1.1"
dns3 = "1.0.0.1"

for ip in iplist:
    mylist.append(ip.rstrip('\n'))

print("Length: " + str(len(mylist)))

print('Processing list')
for host in mylist:
    if host != "":
        server = os.popen("nslookup %s %s | grep name | cut -d'=' -f2" % (host, dns1)).read()

        #If no output for DNS name then try another
        if server == "":
            server = os.popen("nslookup %s %s | grep name | cut -d'=' -f2" % (host, dns2)).read()
            if server == "":
                server = os.popen("nslookup %s %s | grep name | cut -d'=' -f2" % (host, dns3)).read()
                if server == "":
                    #print("Name cannot be found")
                    server = " NOT FOUND"

        #Remove the period from the end of the string, but don't do this for not found
        if server != " NOT FOUND":
            server = server[:-2]

        #Print the name of the server
        #print(server)

        #Append to fqdn list if not empty
        fqdn.append(host + " =" + server)

print("Writing to file")
output = open('nodup_attribution.txt','w')
for item in fqdn:
  output.write("%s\n" % item)
print("Done")
