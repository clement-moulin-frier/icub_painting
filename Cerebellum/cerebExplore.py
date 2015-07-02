#!/usr/local/bin/python

import cerebellum
import numpy as np

class cerebellumInstance:
    def __init__(self,US_size=1, CS_size=1,nBasis=20,k_NOI=0.5,LR=5.0, delay=1,SR=10.0,Range=1,update=30,cfile='basis_visual_sim.cfg'):

        # Configure Cerebellum
        self.US_size = US_size
        self.CS_size = CS_size  # CS size must be different
        self.crb_V = cerebellum.Cerebellum()
        self.crb_V.config(cfile)
        self.udp = update
        self.all_CS = []

        self.crb_V.plug(self.US_size,nBasis,self.CS_size,k_NOI,LR,delay,SR) #nDoF, nBasis, nPNs, k_NOI, beta, delay, SR
        
        self.crb_V.initTrial()
        self.CRB_V_CR = []
        
        self.opt = 3
        self.n = 0
        self.R = Range

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
            #c/=self.R
            c = max(0., c)
            CS=[]
            for i in range(self.CS_size):
                #if c < (i)*self.R/(self.CS_size):
                #    c = 0
                CS.append(c*c)


        u = max(0,US) 
        if u>0:
            u=1
        #print CS
        US_list = [u]

        #print US
        crb_post = max(0,self.crb_V.input(np.append(CS, US)))
        self.CRB_V_CR.append(np.copy(crb_post))
        self.all_CS.append(CS)
        #print crb_post
        
        if self.n<self.udp:
            self.n += 1
        else:
            self.crb_V.doUpdate()
            self.n=0


if __name__ == "__main__":
    __main__()
