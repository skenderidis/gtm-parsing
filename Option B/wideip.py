import re
import json

def wideip(file, next_line):
    wideip_brackets = 0
    wideip = {}
    pool={}
    pool_array=[]
    wideip_name = re.findall(r'gtm wideip a (.*?) {', next_line.strip())
    wideip["name"] = wideip_name[0]
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

file = open("temp.conf",'r')
output = []
while True:
    next_line = file.readline()

    if not next_line:
        break;
    if (next_line.strip().startswith('gtm wideip a')):
        result = wideip(file,next_line)
        output.append(result)

file.close()
print (json.dumps(output))

