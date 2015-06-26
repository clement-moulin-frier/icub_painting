#!/usr/local/bin/python

import cerebellum
import numpy as np

class cerebellumInstance:
	def __init__(self):

    # Configure Cerebellum
    US_size = 1
    CS_size = 1  # CS size must be different
    self.crb_V = cerebellum.Cerebellum()
    self.crb_V.config('basis_visual_sim.cfg')

    self.crb_V.plug(US_size,20,CS_size,0.5,5.0,1,10.0) #nDoF, nBasis, nPNs, k_NOI, beta, delay, SR
    
    self.crb_V.initTrial()
    self.CRB_V_CR = []
    

    n=0

    R=10

	def update(self,CS,US):
		# Connect to CS the distance and to US the 'simulated' touch
        
        if opt == 1: # Full distance
            CS = np.copy(CS)
        else if opt ==2: # 0 or 1, if it's in the range R
        	c = R-CS
        	if c>0:
        		c=1
        	CS = np.max(0, c)
        else if opt == 3: # 0 or distance to threshold. Requires separate CS into several CSs
        	c = R-CS
        	c = np.max(0, c)
        	CS=[]
        	for i in range(CS_size):
        		if c < (i)*R/(CS_size):
        			c = 0
        		CS.append[c]


        u = max(0,US) 
        if u>0:
        	u=1

        US.append(u)

    #print US
    crb_post = crb_V.input(np.append(CS,US))
    self.CRB_V_CR.append(crb_post)
    
    if n<30:
        crb_V.doUpdate()
        n += 1
    else:
        n=0

if __name__ == "__main__":
    __main__()
