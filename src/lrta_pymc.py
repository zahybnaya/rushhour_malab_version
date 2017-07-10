from pymc import DiscreteUniform,Uniform, stochastic,deterministic
from rushhour import min_manhattan_distance, opt_solution_instances
from astar import LRTA
import numpy as np
from test import instance_set
from csv import DictReader
from random import random


# LOOCV calculation (where to find the logp? how to weigh the samples?)

__all__=['instances','path_length','learning_iter',
'h_epsilon']

ins_limit=2
learning_iter=DiscreteUniform('learning_iter', lower=1, upper=5, doc='learning_iter')
h_epsilon = Uniform('h_epsilon',lower=0.,upper=1.)
instances=np.array(instance_set[:ins_limit])

def model_path_length(i,h_epsilon,learning_iter):
    return len(LRTA(i,heur=lambda x: (1+h_epsilon)*min_manhattan_distance(x),update_h=True,iters=learning_iter))


def get_paths_by_subject(paths_file,subject,instances,fun):
    instance_names=[i.name for i in instances]
    with open(paths_file,'rb') as f:
        reader=DictReader(f)
        data=[(d['instance'],fun(d)) for d in reader if d['subject']==subject and d['instance'] in instance_names]
        return [fr for (x,fr) in sorted(data, key=lambda x: instance_names.index(x[0]))]

def sub_path_length(x):
    return float(x['human_length'])

d=get_paths_by_subject('../results/pilot/paths.csv','andra.log',instances,sub_path_length)
sample_data={}

def logp(instances,h_epsilon,learning_iter,subject_ratio):
    max_trials=20
    lp=0
    trials=1;
    for i,sr in zip(instances,subject_ratio):
        while model_path_length(i,h_epsilon,learning_iter)!=sr:
            trials+=1
            if trials > max_trials:
                break
        print '{0},{1},{2},{3}'.format(i.name,h_epsilon,learning_iter,trials)
        sample_data[(i.name,str(h_epsilon),str(learning_iter))]=trials
        lp+=sum([(1./t) for t in range(1,trials+1)])
    return -lp


@stochastic(observed=True)
def path_length(value=d,instances=instances,h_epsilon=h_epsilon,learning_iter=learning_iter):
    return logp(instances,h_epsilon,learning_iter,d)


