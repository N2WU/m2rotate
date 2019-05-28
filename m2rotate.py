#Satellite rotator for M2 Satellite Array
import socket
import time

def getdde(sock):  
    rcvdata, addr = sock.recvfrom(1024)
    #print ("Received:", rcvdata)
    data = rcvdata.decode('utf-8').split(" ")
    #az = data.split(" ")[2]
    #el = data.split(" ")[3]
    az = float(data[1].split(":")[1])
    el = float(data[2].split(":")[1])
    if (el < 0):
        el = 0 #Don't send a negative elevation back
    #print("az is: ", az)
    #print("el is: ", el)
    return (az,el)
    
def main():
    #Get az el from DDE server
    t = 200
    c=0
    UDP_IP = "127.0.0.1"
    UDP_PORT = 7815
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    lastaz = 0
    lastel = 0
    while (c < t):
        azel = getdde(sock)
        if ((azel[0] != lastaz) or (azel[1] != lastel)):
            lastaz = azel[0]
            lastel = azel[1]
            print("Azimuth is: ", lastaz)
            print("Elevation is: ", lastel)
            
        c = c + 1
	

if __name__ == '__main__':
    main()