#Satellite rotator for M2 Satellite Array
#Linux version that accepts rigctl commands from gpredict
import socket
import time
import serial
import signal

def getdde(connection):
    
    #print("waiting for connection")
    #connection, client_address = sock.accept()
    #print ("Connection from ", client_address)
    az = 0.0
    el = 0.0
    status = 0
    #print ("Received:", rcvdata)
    data = connection.recv(1024).decode('utf-8').split(" ")
    print ("received", data[0])
    #import pdb;pdb.set_trace()
    if (data[0][0] == 'p'):
        print("Sending hardcoded values")
        connection.sendall(b'181.0\n15.0\n')
        #connection.sendall(b'2.5')
        status="p"
    elif (data[0][0] == 'P'):
        az = float(data[1])
        el = float(data[2])
        print ("az is: ", az)
        print ("el is: ", el)
        #Set command require a response
        connection.sendall(b'RPRT 0\n')
        status = "P"
    #az = float(data[1].split(":")[1])
    #el = float(data[2].split(":")[1])
        if (el < 0):
            el = 0 #Don't send a negative elevation back
    elif (data[0][0] == 'S'):
        print("Shutdown command received")
        status="S"
    return (az,el, status)
    
def main():
    #Get az el from DDE server
    testing = True #Change to false when in operation
    TCP_IP = "127.0.0.1"
    TCP_PORT = 4533
    azcom = '/dev/ttyUSB0'
    elcom = '/dev/ttyUSB1' #Verify these!  May need to use a more specific device
    baudrate = 9600
    t = 200
    c=0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    #Setup serial connections.  For the M2, you need one for AZ and one for EL
    if not testing:
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
    sock.listen(1)
    connection, client_address = sock.accept()
    while (c < t):
        print("Beginning loop")
        azel = getdde(connection)
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
            if not testing:
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
            else:
                print ("Testing mode enabled")
        if (azel[2] == "S"):
            print("Shutdown received")
            print("waiting for new connection")
            connection.close()
            connection, client_address = sock.accept()
           
        c = c + 1
	
if __name__ == '__main__':
    main()
