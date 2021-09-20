import re
import json
import paramiko
from scp import SCPClient
import sys

#######   Function to parse the Server entries   #########
def server(file, next_line):
    server_brackets = 0
    server = {}
    vs={}
    vs_array=[]
    server_name = re.findall(r'[^{ ]*', next_line.strip())
    server["name"] = server_name[4]
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

#######   Function to parse the Pool entries   #########
def pool(file, next_line):
    pool_brackets = 0
    pool = {}
    member={}
    member_array=[]
    pool_name = re.findall(r'gtm pool a (.*?) {', next_line.strip())
    pool["name"] = pool_name[0]
    pool["members"] = []
    while True:
        if not next_line:
            #print("end_of_file")
            break;
        if ('{' in next_line):
            pool_brackets+=1
        if ('}' in next_line):
            pool_brackets-=1
        if pool_brackets <=0:
            #print("end_of_brackets")
            break;
        next_line = file.readline()


        if (next_line.strip().startswith('/Common/')):
            member_info = re.findall(r'[^{ ]*', next_line.strip())
            member["address"] = member_info[0]
            pool["members"].append(member)

    return(pool)

#######   Function to parse the wideip entries   #########
def wideip(file, next_line):
    wideip_brackets = 0
    wideip = {}
    pool={}
    pool_array=[]
    wideip_name = re.findall(r'[^{ ]*', next_line.strip())
    wideip["name"] = wideip_name[6]
    wideip["pools"] = []
    while True:
        if not next_line:
            #print("end_of_file")
            break;
        if ('{' in next_line):
            wideip_brackets+=1
        if ('}' in next_line):
            wideip_brackets-=1
        if wideip_brackets <=0:
            #print("end_of_brackets")
            break;
        next_line = file.readline()


        if (next_line.strip().startswith('/Common/')):
            pool_info = re.findall(r'[^{ ]*', next_line.strip())
            pool["name"] = pool_info[0]
            wideip["pools"].append(pool)

    return(wideip)

#######   Function to connect with scp to bigip   #########
def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

#######   Command line input to determine whether to parse pools/servers/wideips #########
select=sys.argv[1]

######   BIGIP variables #########
bigip_ip_address="192.168.5.91"
username="root"
password="Kostas123"

######## Connecting to bigip and transfering the bigip_gtm.conf  #######
ssh = createSSHClient(bigip_ip_address, 22, username, password)
sftp = ssh.open_sftp()
sftp.get("/config/bigip_gtm.conf", "config.conf")
sftp.close()
ssh.close()

######## parsing the server entries  #######
if (select=="server"):
    file = open("config.conf",'r')
    file_output = open ("server.json",'w') 

    output = []
    while True:
        next_line = file.readline()
        if not next_line:
            break;
        if (next_line.strip().startswith('gtm server')):
            result = server(file,next_line)
            output.append(result)

    file_output.write(json.dumps(output))
    file.close()
    file_output.close()


######## parsing the pool entries  #######
if (select=="pool"):
    file = open("config.conf",'r')
    file_output = open ("pool.json",'w') 

    output = []
    while True:
        next_line = file.readline()
        
        if not next_line:
            break;
        if (next_line.strip().startswith('gtm pool a')):
            result = pool(file,next_line)
            output.append(result)

    file_output.write(json.dumps(output))
    file.close()
    file_output.close()


######## parsing the wideip entries  #######
if (select=="wideip"):
    file = open("config.conf",'r')
    file_output = open ("wideip.json",'w') 

    output = []
    while True:
        next_line = file.readline()
    
        if not next_line:
            break;
        if (next_line.strip().startswith('gtm wideip a')):
            result = wideip(file,next_line)
            output.append(result)
    file_output.write(json.dumps(output))
    file.close()
    file_output.close()

