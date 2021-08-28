import sys
import csv
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np


lim = float(sys.argv[1] if len(sys.argv) else 1)
count = 0
def set3D():
    fig = plt.figure()
    for each in range(0,count):
        ax = fig.add_subplot(1,count,each+1,projection='3d')

        ax.set_xlim3d([-lim,lim])
        ax.set_xlabel('Est')

        ax.set_ylim3d([-lim,lim])
        ax.set_ylabel('Nrth')

        ax.set_zlim3d([-lim,lim])
        ax.set_zlabel('UP')
        if(count>0):
            ax.set_title(titles[each])
        else:
            ax.set_title("3D Test")

        ax.scatter([0],[0],[0],c="b")
        ax.scatter(data[each][:,0],data[each][:,1],data[each][:,2],c="r")
        ax.plot(data[each][:,0],data[each][:,1],data[each][:,2])
        print(type(ax))
    print(data)
    
    plt.show()

def isEven(n):
    return True if not n%2 else False

def set2D():
    grid = int(count/2 if isEven(count) else ((count+1)/2))
    fig,axis = plt.subplots(grid,grid,figsize=(5,5))
    if(count==0):
        axis.set_xlabel("Est")
        axis.set_ylabel("Nrth")
        axis.set_title("2D Test")
        axis.scatter(data[count][:,0],data[count][:,1],c="r")
        axis.plot(data[count][:,0],data[count][:,1])
        plt.show()
        return 
    print(data[0][0,0])
    gridx = 0
    gridy = 0
    for each in range(0,count):
        axis[gridy,gridx].set_xlabel("Est")
        axis[gridy,gridx].set_ylabel("Nrth")
        axis[gridy,gridx].set_title(titles[each])
        axis[gridy,gridx].scatter(data[each][:,0],data[each][:,1],c="r")
        axis[gridy,gridx].plot(data[each][:,0],data[each][:,1])

        if(not gridx%grid):
            gridx+=1
        else:
            gridx=0
            gridy+=1

    plt.show()

fields = []
data = []
titles = []
test_case_found = False
test_case_count = False
def read():
    global data,count,test_case_count,test_case_found
    file = open("path.csv","r")
    creader = csv.reader(file)
    for each in creader:
        if(test_case_found):
            test_case_found = False
            test_case_count = True
            continue
        if(each[0].find("TST")!=-1):
            test_case_found = True
            data.append([])
            titles.append(each[0])
            count += 1
            continue
        if(each==['x', 'y', 'z']):
            if(not count):
                data.append([])
            continue
        if(test_case_count):   
            data[count-1].append(np.array([float(i) for i in each]))
            continue
        data[count-1].append(np.array([float(i) for i in each]))
    
    for i in range(len(data)):
        data[i] = np.array(data[i])
    data = np.array(data)
    if(len(data) and not count):
        titles.append("Normal")
        count+=1

read()
# with open("path.csv","r") as file:
#     creader = csv.reader(file)
#     fields = next(creader)
#     print(fields)
#     for each in creader:
#         rows.append([float(i) for i in each])

if(lim==0.111):
    set2D()
else:
    set3D()