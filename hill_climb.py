import numpy as np
from invpersim import InvPerSim

class HillClimber:
    def __init__(self, par):
        self.par = par
    
    def __call__(self, t, av, p, v):
        inp = np.array([t, av, p, v])
        ap, an = inp @ self.par
        if(ap > an):
            return 20
        else:
            return -20

def train():
    numenv = 20
    noise = 0.01
    randarr = lambda: 1 - 2 * np.random.rand(4, 2)
    spar = randarr()
    envs = [InvPerSim().randomize() for _ in range(numenv)]
    bestpt = 0
    cnoise = 0.01
    cb = 1
    avgnoise = 0
    updb = 0
    while bestpt < 100:
        dpar = spar + randarr() * cnoise        
        cenvs = [env.copy() for env in envs]
        nowpt = 0
        for ev in cenvs:
            nowpt += 1/ev.ct_sim(HillClimber(dpar))
        nowpt = numenv / nowpt
        if(nowpt > bestpt * 1.01):
            print(cb, bestpt, nowpt, cnoise)
            bestpt = nowpt
            spar = dpar
            avgnoise += cnoise
            updb += 1
            cnoise = noise
        else:
            cnoise *= 1.03
        if cb % 100 == 0:
            print("SHOW: ", cb, cnoise)
            yield HillClimber(spar)
        cb += 1
    avgnoise /= updb
    print("FINISHED IN {} STEP WITH {} POINTS".format(cb, bestpt))
    print("NEEDED {} IMPROVEMENT WITH {} NOISE".format(updb, avgnoise))
    yield HillClimber(spar)
    
    
if __name__ == "__main__":
    for ok in train():
        lst = []
        for x in range(100):
            tester = InvPerSim()
            tester.randomize()
            #tester.start_show(800)
            res = tester.ct_sim(ok)
            lst.append(res)
            #tester.stop_show()
        print("POINTS: ", np.average(lst))
        
    
