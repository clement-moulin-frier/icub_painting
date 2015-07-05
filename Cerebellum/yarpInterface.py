#!/usr/local/bin/python

from pyNNLib import *
import yarp
from CerebConnection import cs_us, cerebellarPainter
from numpy.linalg import norm
from numpy import delete #, linspace, array, cos, sin, pi
from numpy.random import random as rand

def prepareOscBottle(cmd):
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('draw')
    return cmd

def newOscFigure(port):
    cmd = port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('draw')
    cmd.addString('setBorder')
    x=int(rand()*3)+1
    print 'type: ' + str(x)
    cmd.addInt(x)
    port.write()
    yarp.Time.delay(0.2)

def moveOscFigure(port):
    x=0.4
    y=0.13
    cmd = port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('draw')
    cmd.addString('setLocation')
    cmd.addDouble(x)
    cmd.addDouble(y)
    port.write()
    yarp.Time.delay(0.2)

def sendOscDimension(port):
    x=0.13
    y=0.1
    cmd = port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('draw')
    cmd.addString('setDimension')
    cmd.addDouble(x)
    cmd.addDouble(y)
    port.write()
    yarp.Time.delay(0.2)

def sendOscPosition(port,x,y):
    cmd = port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('draw')
    cmd.addString('setDrawing')
    cmd.addDouble(x)
    cmd.addDouble(y)
    port.write()
    return True

def startOscDrawer(port):
    cmd = port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('reactable')
    cmd.addString('drawing')
    cmd.addString('start')
    port.write()
    yarp.Time.delay(0.2)
    return True

def stopOscDrawer(port):
    cmd = port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('reactable')
    cmd.addString('drawing')
    cmd.addString('stop')
    port.write()
    yarp.Time.delay(0.2)
    return True

def sendOscReset(port):
    cmd=port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('draw')
    cmd.addString('reset')
    port.write()
    yarp.Time.delay(0.2)
    return True

def sendOscDistance(port,d):
    cmd=port.prepare()
    cmd.clear()
    cmd.addString('osc')
    cmd.addString('/event')
    cmd.addString('draw')
    cmd.addString('setDistance')
    cmd.addDouble(d)
    port.write()
    yarp.Time.delay(0.2)
    return True

def sendSimData(port,x):
    cmd = port.prepare()
    cmd.clear()
    cmd.addDouble(x)
    port.write()
    return True

def sendCRPort(port,x,y,z):
    cmd = port.prepare()
    cmd.clear()
    cmd.addString('pos')
    cmd.addDouble(x)
    cmd.addDouble(y)
    cmd.addDouble(z)
    port.write()
    return True

def calibrateXY(x,y):
    minX=-0.4
    ranX = 0.15
    maxX=-minX+ranX
    minY=-0.17
    ranY=0.32
    maxY=minY+ranY
    dz=0.145
    dx=minX + ranX*(x+1)/2
    dy=minY + ranY*(y+1)/2
    return dx,dy,dz

def __main__(yarpSim=False):
    #Open network
    yarp.Network.init()
    
    # Open CS Port
    CSInput = yarp.BufferedPortBottle()
    portToCS="/cerebellum/context"+":i"#"/NNsound:i"    
    CSInput.open(portToCS)

    if yarpSim:
        # Open port for simulated CS
        simcs = yarp.BufferedPortBottle()
        portName="/cerebellum/fakeCS"+":o"
        simcs.open(portName)

        #Connect to CS port
        while not yarp.Network.connect(portName, portToCS):
                print "Unable to connect to " + portToCS + " ..."
                yarp.Time.delay(1.0)
    else:
        # Connect to reactable
        portFromTuio = "/reactable2opc/osc:o"

        while not yarp.Network.connect(portFromTuio, portToCS):
    	    	print "Unable to connect to " + portFromTuio + " ..."
    	    	yarp.Time.delay(1.0)

    # Open alternate CR port
    aCR = yarp.BufferedPortBottle()
    portName="/cerebellum/CR/alternate"+":o"#"/NNsound:i"    
    aCR.open(portName)

    # Connect to reactable input
    portToTuio = "/reactable2opc/command:i"
    while not yarp.Network.connect(portName, portToTuio):
            print "Unable to connect to " + portToTuio + " ..."
            yarp.Time.delay(1.0)

    # Open US port
    USInput = yarp.BufferedPortBottle()
    portToUS="/cerebellum/US"+":i"#"/NNsound:i"    
    USInput.open(portToUS)

    if yarpSim:
        # Open port for simulated US
        simus =  yarp.BufferedPortBottle()
        portName="/cerebellum/fakeUS"+":o"#"/NNsound:i"    
        simus.open(portName)

        # Connect to US input
        while not yarp.Network.connect(portName, portToUS):
                print "Unable to connect to " + portToUS + " ..."
                yarp.Time.delay(1.0)
    else:
        # Connect to homeostatic skin drive
        portToHomeo = "/homeoManager/skin/max:o"

        while not yarp.Network.connect(portToHomeo, portToUS):
    	    	print "Unable to connect to " + portToHomeo + " ..."
    	    	yarp.Time.delay(1.0)

    # Open CR port
    CROutput=yarp.BufferedPortBottle()
    portName="/cerebellum/CR"+":o"
    CROutput.open(portName)
    if not yarpSim:
        # Connect to rightArm
        portToController ="/xy/rpc"

        while not yarp.Network.connect(portName, portToController):
                print "Unable to connect to " + portToController + " ..."
                yarp.Time.delay(1.0)

    # Open US Output Port, for plotting
    USOutput=yarp.BufferedPortBottle()
    portName="/cerebellum"+"/US:o"
    USOutput.open(portName)

    # Check that there's input in the ports
    CS=None
    US=None
    if not yarpSim:
        while CS == None or US == None:
            print "data"
            print CS
            CS = CSInput.read()
            US = USInput.read()
        if CS != None and US != None:
            print "data2"
            print CS
            CS_size=CS.size()
            US_size=US.size()
    '''print "data3"
    print CS
    print CS_size
    print US_size'''
    # Configure Cerebellum
    US_size = 1
    cp = cerebellarPainter()
    cp.configure()
    
    #startOscDrawer(aCR)
    newOscFigure(aCR)
    moveOscFigure(aCR)
    sendOscDimension(aCR)
    sendOscReset(aCR)
    sendOscDistance(aCR, 0.1)

    n=0
    tactile_us = False

    try:
        ni=int(raw_input('Select a number of iterations (recommended > 100):'))
    except ValueError:
        print "Not a number"
    
    #while(True):
    for ni in range(1000):
        yarp.Time.delay(0.05)
        
        dx = cp.x_pos[0]
        cp.x_pos = delete(cp.x_pos,0)
        dy = cp.y_pos[0]
        cp.y_pos = delete(cp.y_pos,0)

        if yarpSim:
            CS,US = cs_us(dx,dy)
            sendSimData(simcs,CS)
            sendSimData(simus,US)

        CS=[]
        US=[]
        CSBottle = CSInput.read()
        USBottle = USInput.read()
        
        if CSBottle != None and USBottle != None:

            #print "updating loop: "
            for i in range(CSBottle.size()):
                
	            	c = CSBottle.get(i).asDouble()
	            	 

            for i in range(USBottle.size()):
                #print i
                u = max(0,USBottle.get(i).asDouble()) 
                if u>0:
                	u=1

            # Update explorer/cerebellum
            cp.update(c,u,True)
            

            # Send data to motors
            dx,dy,dz = calibrateXY(dx,dy)
            sendCRPort(CROutput,dx,dy,dz)
            # Send data to reactable
            cmd = aCR.prepare()
            x=dy+0.4
            y=dx+0.5
            cmd.clear()
            cmd.addString('osc')
            cmd.addString('/event')
            cmd.addString('draw')
            cmd.addString('setDrawing')
            cmd.addDouble(x)
            cmd.addDouble(y)
            aCR.write()
            print 'x = ' + str(dx/2+0.5) + '  ;   y = ' + str(dy/2+0.5)

            USo = USOutput.prepare()
            USo.clear()
            try:
                for n in range(len(US)):
                	#print US[n]
                	USo.addDouble(US[n])
            except TypeError:
            	#print US
                USo.addDouble(float(US))
            USOutput.write()
    stopOscDrawer(aCR)
            
if __name__ == "__main__":
    __main__(True)
