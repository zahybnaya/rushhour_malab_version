from pymc3 import Model, DiscreteUniform, Uniform, Discrete, Deterministic
import theano.tensor as tt
from theano.compile.ops import as_op
from rushhour import min_manhattan_distance, opt_solution_instances
from astar import LRTA, eval_theano
import numpy as np
from test import instance_set
from csv import DictReader
from random import random
from sys import argv

# Two parameters 
try:
    subject=argv[1]
    path_file=argv[2]
except:
    print 'Args:  <subject> <path_file>'

class IVS(Discrete):
    def __init__(self,instances,h_epsilon,learning_iter, *args, **kwargs):
        super(IVS, self).__init__(*args, **kwargs)#What does discrete expects?
        self.instances = instances
        self.h_epsilon = h_epsilon
        self.learning_iter = learning_iter

    def logp(self, value):
        print value
        return logp(self.instances,self.h_epsilon,self.learning_iter,value)


def get_instances_by_subject(path_file,subject):
    with open(path_file,'rb') as f:
        reader=DictReader(f)
        data=[d['instance'] for d in reader if d['subject']==subject and d['complete']=='True']
        return sorted(data)

def get_paths_by_subject(path_file,instance_names,subject,fun):
    with open(path_file,'rb') as f:
        reader=DictReader(f)
        data=[(d['instance'],fun(d)) for d in reader if d['subject']==subject and d['instance'] in instance_names]
        return [fr for (x,fr) in sorted(data, key=lambda x: instance_names.index(x[0]))]

def make_model_path_length(i):
    @as_op(itypes=[tt.dscalar,tt.lscalar], otypes=[tt.lscalar])
    def model_path_length(h_epsilon,learning_iter):
        path,_= LRTA(i,heur=lambda x: (1+h_epsilon)*min_manhattan_distance(x),update_h=True,iters=learning_iter)
        print len(path)
        return len(path)
    return model_path_length

# TODO: store per trial 
def logp(instances,h_epsilon,learning_iter,sub_path_length):
    max_trials=20
    lp=0
    trials=1;
    for i,sr in zip(instances,sub_path_length):
        m_path_f = make_model_path_length(i)
        while True:
            r=m_path_f(h_epsilon,learning_iter)
            print 'Model:{} Subject:{}'.format(r,sr)
            if len([1 for _ in r]) == len([1 for _ in sr]) or trials > max_trials:
                break
            trials+=1
        print '{0},{1},{2},{3}'.format(i.name,h_epsilon,learning_iter,trials)
        sample_data[(i.name,str(h_epsilon),str(learning_iter))]=trials
        lp+=sum([(1./t) for t in range(1,trials+1)])
        trials=1
    return -lp


lrta_model=Model()
with lrta_model:
    d=get_paths_by_subject(path_file,get_instances_by_subject(path_file,subject),subject,lambda x:int(x['human_length']))
    print d
    sample_data={}
    learning_iter_=DiscreteUniform('learning_iter_',lower=1, upper=5)
    learning_iter=Deterministic('learning_iter',learning_iter_)
    h_epsilon_ = Uniform('h_epsilon_',lower=0.,upper=1.)
    h_epsilon = Deterministic('h_epsilon',h_epsilon_)
    instances=np.array([i for i in instance_set if i.name in get_instances_by_subject(path_file,subject)]) #is this sorted properly?
    path_length=IVS('path_length',instances,h_epsilon,learning_iter, observed=d)


