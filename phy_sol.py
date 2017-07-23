from math import *
import numpy as np
from invpersim import InvPerSim

def phy_sol(tilt, ang_vel, pos, vel):
    a = 20.0
    tilt_target = tilt + atan(pos + vel)/3
    if ang_vel * tilt_target > 0:
        acc = copysign(a, tilt_target)
    elif 10.0*(1-cos(tilt_target)) < (ang_vel)**2:
        acc = copysign(a, +ang_vel)
    elif 10.0*(1-cos(tilt_target)) > (ang_vel)**2:
        acc = copysign(a, -ang_vel)
    return acc
    
def phy_test():
    lst = []
    for x in range(100):
        tester = InvPerSim()
        tester.randomize()
#       tester.start_show(800)
        res = tester.ct_sim(phy_sol)
        lst.append(res)
        tester.stop_show()
    print(np.average(lst))
    

if __name__ == "__main__":
    phy_test()
