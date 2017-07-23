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
    numenv = 25
    noise = 0.01
    randarr = lambda: 1 - 2 * np.random.rand(4, 2)
    spar = randarr()
    bestpt = 0
    cnoise = 0.01
    avgnoise = 0
    updb = 0
    for cb in range(1500):
        dpar = spar + randarr() * cnoise        
        nowpt = 0
        for _ in range(numenv):
            ev = InvPerSim().randomize()
            nowpt += 1/ev.ct_sim(HillClimber(dpar))
        nowpt = numenv / nowpt
        if(nowpt > bestpt):
            print(cb, bestpt, nowpt, cnoise)
            bestpt = nowpt
            spar = dpar
            avgnoise += cnoise
            updb += 1
            cnoise = noise
        else:
            cnoise *= 1.03
        if cb % 100 == 0:
            print("SHOW: ", cb)
            yield HillClimber(spar)
        cb += 1
    avgnoise /= updb
    print("FINISHED IN {} STEP WITH {} POINTS".format(cb, bestpt))
    print("NEEDED {} IMPROVEMENT WITH {} NOISE".format(updb, avgnoise))
    print("FINAL TENSOR:")
    print(spar)
    yield HillClimber(spar)
    
    
if __name__ == "__main__":
    for ok in train():
        cpt = 0
        for _ in range(100):
            tester = InvPerSim()
            tester.randomize()
            #tester.start_show(800)
            res = tester.ct_sim(ok)
            cpt += res
            #tester.stop_show()
        print("POINTS: ", cpt / 100)
    
    
