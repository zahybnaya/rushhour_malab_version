"""
A generic fitting for a function
"""
import numpy as np
from scipy import optimize
from inspect import getargspec

class Parameter:
    def __init__(self, value):
            self.value = value

    def set(self, value):
            self.value = value

    def __call__(self):
            return self.value

def fit(stimuli, model_creator, likelihood_function,parameters,bounds, data):
    def f(params):
        for p,(lb,ub) in zip(params,bounds):
            if p<lb or p>ub:
                print 'Out of bound {}<{}<{}. All={} '.format(lb,p,ub,params)
                return 1000 #float('inf')
        model = model_creator(*params)
        print 'Checking {} -> '.format(model.__name_),
        val=-likelihood_function(stimuli,model,data,1000)
        print val
        return val
    p = [param for param in parameters]
    constraints=[{'type':'ineq', 'fun':lambda x:x[0]>=0 and x[0]<=1},{'type':'ineq', 'fun':lambda x:x[1]>=0 and x[1]<=1}]
    bounds=((0,1),(0,1))
    return optimize.minimize(f,p,method='Powell')


def test():
    # giving initial parameters
    mu = Parameter(1)
    sigma = Parameter(3)
    height = Parameter(5)

    # define your function:
    def f(x): return height() * np.exp(-((x-mu())/sigma())**2)

    # fit! (given that data is an array with the data to fit)
    data = 10*np.exp(-np.linspace(0, 10, 100)**2) + np.random.rand(100)
    print fit(f, [mu, sigma, height], data)


#argnames,varargs,keywords,defaults=getargspec(make_Astar)
#print argnames
