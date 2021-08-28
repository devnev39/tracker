import math

def corrections(dists,ori):
    # Dists is acceleration list
    dists[0] -= 9.8*math.sin(math.radians(ori[2])) 
    dists[1] -= 9.8*math.sin(math.radians(ori[1]))

    return dists

def dist_correction(dists,ori):
    x = dists[0]
    y = dists[1]
    if(ori[0]<45 or ori[0]>315):
        return dists

    if(ori[0]>45 or ori[0]<135):
        # East side
        dists[0] = y
        dists[1] = -x
    if(ori[0]>135 and ori[0]<225):
        # North side
        dists[0] = -x
        dists[1] = -y
    if(ori[0]>225 and ori[0]<315):
        # West side
        dists[0] = -y
        dists[1] = x
    
    return dists


def check(x,y,z,r):
    truths = [True,True,True]
    if(x<r and x>-r):
        truths[0] = False
    if(y<r and y>-r):
        truths[1] = False
    if(z<r+0.5 and z>-r-0.5):
        truths[2] = False
    if(not sum(truths)):return False
    return truths
