import re
import json
from datetime import datetime


def server(file, next_line):
    server_brackets = 0
    server = {}
    vs={}
    vs_array=[]
    server_name = re.findall(r'gtm server (.*?) {', next_line.strip())
    server["name"] = server_name[0]
    server["virtual_server"] = []
    while True:
        if not next_line:
           #print("end_of_file")
            break;
        if ('{' in next_line):
            server_brackets+=1
        if ('}' in next_line):
            server_brackets-=1
        if server_brackets <=0:
            #print("end_of_brackets")
            break;
        next_line = file.readline()

        if (next_line.strip().startswith('datacenter')):
            datacenter_name = re.findall(r'[^{ ]*', next_line.strip())
            server["dc"] = datacenter_name[2]

        if (next_line.strip().startswith('product')):
            product = re.findall(r'[^{ ]*', next_line.strip())
            server["product"] = product[2]

        if (next_line.strip().startswith('destination')):
            destination = re.findall(r'[^{ ]*', next_line.strip())
            vs["address"] = destination[2]
            server["virtual_server"].append(vs["address"])

    return(server)




file = open("test.txt",'r')
output = []
while True:
    next_line = file.readline()
    
    if not next_line:
        break;
    if (next_line.strip().startswith('gtm server')):
        result = server(file,next_line)
        output.append(result)

file.close()
print (json.dumps(output))

