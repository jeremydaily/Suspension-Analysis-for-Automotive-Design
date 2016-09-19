#!/usr/env/python 
#-*- coding: utf-8 -*-
"""
Python Code
Created on Mon Sep 12 21:29:16 2016
by
author: jeremy-daily

Title: Quarter Car Simulation

Description: An example of simulating the suspension response of a quarter car model 
 from a step input. Teh vehicle parameters can be changed according to the entries in the
 getSpringMassDamperValues() function.

"""
#import the plotting engine
import matplotlib.pyplot as plt

# Code from : http://www.codeproject.com/Tips/792927/Fourth-Order-Runge-Kutta-Method-in-Python
def RK4(x, fx, n, hs):
    k1 = [] #reset the lists for computing the next output
    k2 = []
    k3 = []
    k4 = []
    xk = []
    for i in range(n):
        k1.append(fx[i](x)*hs)
    for i in range(n):
        xk.append(x[i] + k1[i]*0.5)
    for i in range(n):
        k2.append(fx[i](xk)*hs)
    for i in range(n):
        xk[i] = x[i] + k2[i]*0.5
    for i in range(n):
        k3.append(fx[i](xk)*hs)
    for i in range(n):
        xk[i] = x[i] + k3[i]
    for i in range(n):
        k4.append(fx[i](xk)*hs)
    for i in range(n):
        x[i] = x[i] + (k1[i] + 2*(k2[i] + k3[i]) + k4[i])/6
    return x
    
# These functions are derived from applyting the equations of motion to the free body diagrams.
# Once the equations are obtained, they are cast into the state-space form or a system of first
# order differential equations of the form d[x]/dt = f([x]). The last entry in [x] is time.
def f0(x):
    return x[1]
    
def f1(x):
    (m_wheel,M_car,c_shock,c_tire,k_spring,k_tire,g) = getSpringMassDamperValues()
    return - k_spring*(x[0]-x[2])/M_car - c_shock*(x[1]-x[3])/M_car

def f2(x):
    return  x[3]

def f3(x):
    (m_wheel,M_car,c_shock,c_tire,k_spring,k_tire,g) = getSpringMassDamperValues()
    return - k_spring*(x[2]-x[0])/m_wheel - c_shock*(x[3]-x[1])/m_wheel  - k_tire*(x[2]-Zsurf(x[4]))/m_wheel - c_tire*(x[3]-Zdotsurf(x[4]))/m_wheel

def f4(x):
    return 1

def Zsurf(t): #Step function input
    v = 80
    if v*t < 8:
        return 0
    else:
        return 4 #4

def Zdotsurf(t): #Approximate an impulse
    v = 80
    if v*t < 7  and v*t > 9:
        return 4# 4
    else:
        return 0
    
def getSpringMassDamperValues():
    '''A list of constants. Access this list by invoking the command 
    
     (m_wheel,M_car,c_shock,c_tire,k_spring,k_tire,g) = getSpringMassDamperValues()
     
     These constants should have something to do with the problem being solved. The units
     must be consistent
    '''
    #acceleration due to gravity
    g         = 386.4 #in/sec/sec
    #calculate mass by weight / gravity    
    m_wheel   = 50/g #lb-s^2/in
    M_car     = 1500/g 
    c_shock   = 10 #lb-s/in
    c_tire    = 1
    k_spring  = 250 #lb/in
    k_tire    = 2000 
    
    return (m_wheel,M_car,c_shock,c_tire,k_spring,k_tire,g) 

#all the functions that are called must be defined before the main script runs.

#assemble all the functions
f = [f0, f1, f2, f3, f4] #This is d[x]/dt

#Initial conditions
x = [0,0,0,0,0] # [x](t=0)

#number of state variables and functions
n = len(x)

#time step increment
hs = 0.001 #seconds for the time step

time=[]
wheelBounce=[]
carBounce=[]
for i in range(5000):
    #Run the runge-kutta algorithm
    x = RK4(x,f,n,hs)
    #print(x) #debug only
    
    #Add to the lists for the variables needed to plot.
    time.append(x[4])
    carBounce.append(x[0])
    wheelBounce.append(x[2])

(m_wheel,M_car,c_shock,c_tire,k_spring,k_tire,g) = getSpringMassDamperValues()


#Plot the result on 2 subplots on 1 piece of paper.
#see the documetation at matplotlib.org for details regarding the format and syntax
plt.figure(figsize=(8.5,11))
plt.suptitle("Quarter Car Suspension Simulation Output\nDr. Daily's Example",fontsize=16)
ax = plt.subplot(2,1,1)
plt.plot(time,carBounce,'-',label="Car")
plt.plot(time,wheelBounce,'--',label="Wheel")
plt.xlabel("Time (sec.)")
plt.ylabel("Displacement (inches)")
plt.legend(loc='upper right')
plt.grid(b=True,linestyle=':')
plt.axis([0,5,0,7])
plt.text(.99,0.02,"$m_{wheel} = %g$ lb-s$^2$/in \n$M_{car} = %g$ lb-s$^2$/in\n$c_{shock}=%g$ lb-s/in\n$c_{tire}=%g$ lb-s/in\n$k_{spring}=%g$ lb/in\n$k_{tire}=%g$ lb/in " %(m_wheel,M_car,c_shock,c_tire,k_spring,k_tire),fontsize=12,bbox=dict(facecolor='white'),transform=ax.transAxes,horizontalalignment='right',verticalalignment='bottom',)

ax = plt.subplot(2,1,2)
plt.plot(time,carBounce,'-',label="Car")
plt.plot(time,wheelBounce,'--',label="Wheel")
plt.xlabel("Time (sec.)")
plt.ylabel("Displacement (inches)")
plt.grid(b=True,linestyle=':')
plt.legend(loc='upper right')
plt.text(.99,0.02,"Zoomed in to see \nwheel response",fontsize=12,bbox=dict(facecolor='red', alpha=0.25),transform=ax.transAxes, horizontalalignment='right', verticalalignment='bottom')
plt.axis([0,.5,0,6])
plt.savefig("quarterCarStepInputSimulation.pdf",transparent=False)
plt.show()