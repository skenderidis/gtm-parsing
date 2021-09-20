import socket
from datetime import datetime
import time

limit = 5                       ### "How many DNS requets you want to execute? (for example 10,000): ")
dns_name = "www.test.local"     #### "What is the hostname you want to resolve? (for example www.test.local): ")
sleep_time = 0.005              ##### Sleep between DNS requests. 0.005 is 5 milliseconds while 1 is 1 second.
start_time = datetime.now()
addr1="Failed"

x=0
y=0
while True:
    x=x+1
	time.sleep (sleep_time)
    try:
        addr1 = socket.gethostbyname(dns_name)
#        print(addr1)

    except Exception, exc:
#        print("error while processing item:")
        y=y+1
    if x>=limit:
        break;


end_time = datetime.now()

print("Attempted DNS requests:" + str(x))
print("Failed DNS requests:" + str(y))
print('Duration: {}'.format(end_time - start_time))
print(addr1)

