#!/usr/local/bin/python

import cerebellum
import numpy as np

class cerebellumInstance:
    def __init__(self):

        # Configure Cerebellum
        self.US_size = 1
        self.CS_size = 1  # CS size must be different
        self.crb_V = cerebellum.Cerebellum()
        self.crb_V.config('basis_visual_sim.cfg')

        self.crb_V.plug(self.US_size,20,self.CS_size,0.5,5.0,1,10.0) #nDoF, nBasis, nPNs, k_NOI, beta, delay, SR
        
        self.crb_V.initTrial()
        self.CRB_V_CR = []
        
        self.opt = 3
        self.n = 0
        self.R = 0.2

    def update(self,CS,US):
        # Connect to CS the distance and to US the 'simulated' touch
        if self.opt == 1: # Full distance
            CS = np.copy(CS)
        elif self.opt ==2: # 0 or 1, if it's in the range R
            c = self.R-CS
            if c>0:
                c=1
            CS = np.max(0, c)
        elif self.opt == 3: # 0 or distance to threshold. Requires separate CS into several CSs
            c = self.R - CS
            c = max(0., c)
            CS=[]
            for i in range(self.CS_size):
                if c < (i)*self.R/(self.CS_size):
                    c = 0
                CS.append(c)
        print c

        u = max(0,US) 
        if u>0:
            u=1

        US_list = [u]

        #print US
        crb_post = self.crb_V.input(np.append(CS, US))
        self.CRB_V_CR.append(crb_post)
        
        if self.n<30:
            self.crb_V.doUpdate()
            self.n += 1
        else:
            self.n=0


if __name__ == "__main__":
    __main__()
