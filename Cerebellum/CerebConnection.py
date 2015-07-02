#!/usr/local/bin/python

import sys
sys.path.insert(0, '../explorer')

from explorer_mod import Explorer

from cerebExplore import cerebellumInstance

def cs_us(x, y):
    us = float(norm([x, y]) > 1)
    cs = abs(1. - norm([x, y]))
    return cs, us

from numpy import linspace, array, cos, sin, pi, delete
from numpy.linalg import norm
from numpy.random import seed, randn
from numpy.random import random as rnd
from matplotlib.pyplot import subplots, show, plot, clf, ion, draw, figure

#Experiment cerebellum ctrl vs no cerebellum
class cerebellarPainter():
    def __init__(self):

        self.dt = 0.1
        self.all_us = []
        self.all_target_x = []
        self.all_target_y = []
        self.all_distance = []
        self.us=0
        self.punishment = False
        self.expl = Explorer(dist_mu = 0.3,dist_sigma=0.2,x=0.0,y=0.0)
        self.cer = cerebellumInstance(CS_size=20, Range=0.5,k_NOI=0.35, nBasis=250,LR=70,delay=0.9,SR=1/self.dt,update=50,cfile='basis_visual_sim2.cfg')
        self.connect_cerebellum=True
        self.crb_anticip=False
        self.new_target = True
        self.x_pos=[]
        self.y_pos=[]
        self.circle = [cos(array(range(360))*pi/180),sin(array(range(360))*pi/180)]
        #seed(s)

    def configure(self,plot_data=True):
        self.newTarget()
        if plot_data:
            ion()
            self.i=0
        return True

    def newTarget(self):
        if self.connect_cerebellum:
            if len(self.cer.CRB_V_CR)!=0:
                if self.crb_anticip:
                    self.expl.sample(self.punishment, self.cer.CRB_V_CR[-1])
                else:
                    self.expl.sample(self.punishment,0 )
            else:
                self.expl.sample(self.punishment,0 )
        else:
            self.expl.sample(self.punishment,0)

        X = self.expl.current_pos[0]
        Y = self.expl.current_pos[1]
        
        self.all_target_x.append(X)
        self.all_target_y.append(Y)
        #separate the data in a constant speed fashion
        n_dt = int(norm(array([X,Y]) - self.expl.previous_pos) / self.dt)
        self.x_pos = linspace(self.expl.previous_pos[0], X, n_dt)
        self.y_pos = linspace(self.expl.previous_pos[1], Y, n_dt)
        return True

    def update(self, US, CS, plot_data=True):

        # If there's a reflexive movement, it has priority to the cerebellum
        if self.crb_anticip or self.punishment:
            
            self.all_distance.append(CS)
            self.all_us.append(US)
            self.cer.update(CS, US)
            if self.x_pos.shape == 0:
                self.crb_anticip = False
                self.punishment = False
                self.new_target = True

        else:
            # else, the cerebellum can take over whenever it wants
            self.all_distance.append(cs)
            self.all_us.append(US)
            self.cer.update(CS,US)
            if self.connect_cerebellum:
                if len(self.cer.CRB_V_CR)!=0:
                    if self.cer.CRB_V_CR[-1]>0.01:
                        #print cer.CRB_V_CR[-1]
                        self.crb_anticip = True
                        self.new_target = True
        if self.crb_anticip:
            punishment = True

        if self.punishment == False:
            self.punishment = bool(US)
        #Check if a new target has to be defined, and how
        if self.new_target:
            self.newTarget()
            self.new_target = False
        # Plot if desired
        if plot_data:
            if self.i%20==0:
                self.updatePlot()
            self.i +=1
        return self.cer.CRB_V_CR
    
    def updatePlot(self):
        clf()
        plot(self.cer.CRB_V_CR[-500:])
        plot(self.all_us[-500:])
        plot(self.cer.all_CS[-500:])
        draw()
        '''figure()
        plot(self.all_target_x, self.all_target_y)
        plot(self.circle[0],self.circle[1])
        draw()
        '''

if __name__ == '__main__':
    cp=cerebellarPainter()
    cp.configure()

    for n in range(1000):
        dx = delete(cp.x_pos,0)
        dy = delete(cp.y_pos,0)
        cs,us = cs_us(dx,dy)
        cp.update(cs,us,True)
    print 'Done!!'

        


