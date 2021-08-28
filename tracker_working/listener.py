import sys
import numpy as np
import socket
import javaobj
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3
import time
import csv
from Corrections import *

xa = [0]
ay = [0]
az = [0]

lim = 5

addr = 0
acc = 0
prev = 0.0
file = 0
cwriter = 0
file_acc = 0
awriter = 0
plot_title = ""

if len(sys.argv)>1: plot_title = sys.argv[1]

thresh_hold = 0.8

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


def animate(i,line):
    start = time.perf_counter()
    global prev
    data = acc.recv(1024)
    print(f'Received : {len(data)}')

    data = (javaobj.loads(data)).values
    delta = round(time.perf_counter() - prev,2)

    ac = (np.array(data["ACC"]) - np.array(data["GRV"]))
    prev = time.perf_counter()

    truths = check(ac[0],ac[1],ac[2],thresh_hold)
    print(truths)
    if(not truths):return line,

    ac = corrections(ac,data["ORI"])

    print(delta)
    # awriter.writerow([ac[0],ac[1],ac[2]])
    vals =[]
    for each in truths:
        if(each):
            vals.append(round(ac[truths.index(each)]*(delta**2)/2,2))
        else:
            vals.append(0)
    corrected = dist_correction(vals,data["ORI"])
    xa.append(xa[-1]+corrected[0])
    ay.append(ay[-1]+corrected[1])
    az.append(az[-1]+vals[2])    
    # az.append(0)
    cwriter.writerow([xa[-1],ay[-1],az[-1]])
    
    if(len(xa)>20):
        xa.pop(0)
        ay.pop(0)
        az.pop(0)

    line.set_data(np.array(xa),np.array(ay))
    line.set_3d_properties(np.array(az))

    print(f'Time spent : {time.perf_counter()-start}')
    return line,

def getLocalIp():
    sck = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sck.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sck.connect(("8.8.8.8",1))
    return str(sck.getsockname()[0])

try:
    print(getLocalIp())
    server.bind((getLocalIp(),9000))
    server.listen()
    print("server started...")
    acc,addr = server.accept()
    print(f'Connection from {addr}')

    file = open("path.csv","a")
    file_acc = open("acc.csv","a")
    cwriter = csv.writer(file)
    awriter = csv.writer(file_acc)
    if plot_title:
        cwriter.writerow([f"TST {plot_title}"])
        awriter.writerow([f"TST {plot_title}"])
    cwriter.writerow(["x","y","z"])
    cwriter.writerow([0,0,0])
    awriter.writerow(["x","y","z"])
    awriter.writerow([0,0,0])


    prev = time.perf_counter()
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    ax.set_xlim3d([-lim, lim])
    ax.set_xlabel('Est')

    ax.set_ylim3d([-lim, lim])
    ax.set_ylabel('Nrth')

    ax.set_zlim3d([-lim, lim])
    ax.set_zlabel('UP')
    # //ax.set_autoscale_on(True)
    ax.set_title('3D Test')

    line = ax.plot([0],[0],[0])[0]

    ani = FuncAnimation(fig,animate,frames=100,blit=True,fargs=(line,))
    plt.show()
    file.close()
except Exception as e:
    print(e)
    _,_,tb = sys.exc_info()
    print(tb.tb_lineno)
    server.detach()
    server.close()
    

