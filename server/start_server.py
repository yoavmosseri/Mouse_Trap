import time
from protocol.main_server import MainServer 
import sys

max_clients = int(sys.argv[1])
run_time = int(sys.argv[2])

server = MainServer('0.0.0.0',4444,max_clients)
server.activate()

time.sleep(60*60*run_time)

server.deactivate()

