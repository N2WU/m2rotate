#Satellite rotator for M2 Satellite Array
import socket
import time
import serial

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
    UDP_IP = "127.0.0.1"
    UDP_PORT = 7815
    azcom = 'COM3'
    elcom = 'COM5'
    baudrate = 9600
    t = 200
    c=0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    #Setup serial connections.  For the M2, you need one for AZ and one for EL
    try:
        azser = serial.Serial(azcom, baudrate, timeout=1)
    except:
        print("Failed to open azimuth", azcom)
        
        azser = 0
    try:
        elser = serial.Serial(elcom, baudrate, timeout=1)
    except:
        elser = 0
        print("Failed to open elevation", elcom)
    lastaz = 0
    lastel = 0
    while (c < t):
        azel = getdde(sock)
        if ((azel[0] != lastaz) or (azel[1] != lastel)):
            lastaz = azel[0]
            lastel = azel[1]
            print("Azimuth is: ", lastaz)
            print("Elevation is: ", lastel)
            #Send to com
            azupdate = "APn" + str(lastaz) + "\r;"
            elupdate = "APn" + str(lastel) + "\r;"
            print ("Sending this:")
            print (azupdate)
            print (elupdate)
            #Read where it is currently at
            azser.write("Bin;".encode('utf-8'))
            result = azser.read(8)
            print(result)
            try:
                azser.write(azupdate.encode('utf-8'))
            except:
                print("Failed to write azimuth")
                import pdb;pdb.set_trace()
            try:
                elser.write(elupdate.encode('utf-8'))
            except:
                print("Failed to write elevation")
                
            
        c = c + 1
	

if __name__ == '__main__':
    main()