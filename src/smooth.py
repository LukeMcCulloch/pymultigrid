#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 21:31:08 2019

@author: lukemcculloch
"""

import numpy as np

def get_lhs(u,h2):
    w = np.zeros_like(u)
    w[1:-1,1:-1] = (
            u[0:-2,1:-1]+u[2: , 1:-1] +
            u[1:-1,0:-2]+u[1:-1,2:] - 
            4.*u[1:-1,1:-1])/h2 +u[1:-1,1:-1]*u[1:-1,1:-1]
    return w

def gs_rb_step(v,f,h2):
    u = v.copy()
    res = np.empty_like(v)
    
    res[1:-2,1:-1:2] = (u[])
    

def get_lhs(u,h2):
    """ Return discretized operator L(u).  
    h2=h**2 for spacing h. """
    w=np.zeros_like(u)
    w[1:-1,1:-1]=(
            u[0:-2,1:-1] + u[2: ,1:-1]+
            u[1:-1,0:-2]+u[1:-1,2: ]-
            4*u[1:-1,1:-1])/h2
            +u[1:-1,1:-1]**2
    return w

def gs_rb_step(v,f,h2):
    """ Carry out single Gauss-Seidel 
    iteration step on v.f is source term, 
    h2 is square of grid spacing."""
    u=v.copy()
    
    res=np.empty_like(v)
    
    res[1:-1:2,1:-1:2]=(
                        u[0:-2:2,1:-1:2] + u[2: :2,1:-1:2] + 
                        u[1:-1:2,0:-2:2] + u[1:-1:2,2: :2] - 
                        4*u[1:-1:2,1:-1:2]
                        ) / h2 + \
                        u[1:-1:2,1:-1:2]**2 - f[1:-1:2,1:-1:2]
            
    u[1:-1:2,1:-1:2] -= res[1:-1:2,1:-1:2] / 
                        (-4.0/h2+2*u[1:-1:2,1:-1:2])
                        
    res[2:-2:2,2:-2:2] = (u[1:-3:2,2:-2:2] + u[3:-1:2,2:-2:2] + 
                           u[2:-2:2,1:-3:2]+u[2:-2:2,3:-1:2] - 
                           4*u[2:-2:2,2:-2:2])/h2 +\
                           u[2:-2:2,2:-2:2]**2 - f[2:-2:2,2:-2:2]
                           
    u[2:-2:2,2:-2:2] -= res[2:-2:2,2:-2:2] / (
                                    -4.0/h2+2*u[2:-2:2,2:-2:2])
    
    res[2:-2:2,1:-1:2]=(u[1:-3:2,1:-1:2]+u[3:-1:2,1:-1:2]+
                       u[2:-2:2,0:-2:2]+u[2:-2:2,2: :2]-
                       4*u[2:-2:2,1:-1:2])/h2 +\
                       u[2:-2:2,1:-1:2]**2-f[2:-2:2,1:-1:2]
                       
    u[2:-2:2,1:-1:2]-=res[2:-2:2,1:-1:2]/(
                        -4.0/h2+2*u[2:-2:2,1:-1:2])
    
    res[1:-1:2,2:-2:2]=(u[0:-2:2,2:-2:2]+u[2: :2,2:-2:2]+
                       u[1:-1:2,1:-3:2]+u[1:-1:2,3:-1:2]-
                       4*u[1:-1:2,2:-2:2])/h2 +\
                       u[1:-1:2,2:-2:2]**2-f[1:-1:2,2:-2:2]
                       
    u[1:-1:2,2:-2:2]-=res[1:-1:2,2:-2:2]/(
                        -4.0/h2+2*u[1:-1:2,2:-2:2])
    
    return u


def solve(rhs):
    """ Return exact solution 
    on the coarsest 3x3 grid.
    """
    h=0.5
    u=np.zeros_like(rhs)
    fac=2.0/h**2
    dis=np.sqrt(fac**2+rhs[1,1])
    u[1,1]=-rhs[1,1]/(fac+dis)
    return u