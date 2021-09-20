import re
import json

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


file = open("temp.conf",'r')
output = []
while True:
    next_line = file.readline()
    
    if not next_line:
        break;
    if (next_line.strip().startswith('gtm pool a')):
        result = pool(file,next_line)
        output.append(result)

file.close()
print (json.dumps(output))

