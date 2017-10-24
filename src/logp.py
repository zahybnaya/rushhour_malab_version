import logging
from copy import deepcopy
from rushhour import rhstring,do_move_from_fixed
import numpy as np
from csv import reader
from test import instance_set

# constant for when a trial is not found
NOT_FOUND_LOGLIK_VALUE=14

def get_moves_by_subject(move_file,subject):
    """
    extracts a list of lists of moves done by subject.
    """
    with open(move_file,'rb') as f:
        header=f.readline().strip().split(',')
        r=reader(f)
        data=[]
        path=[]
        path_ind=''
        for d in r:
            if d[header.index('subject')]!=subject:
                continue
            if ''.join([d[header.index('instance')],d[header.index('trial_number')]])==path_ind:
                path.append(d)
            else:
                path_ind=''.join([d[header.index('instance')],d[header.index('trial_number')]])
                data.append(path)
                path=[]
    return data[1:]
        #data=[(d['instance'],fun(d)) for d in reader if d['subject']==subject]
        #return np.array([fr for (x,fr) in data])



def get_instances_by_subject(path_file,subject,instance_set):
    """
    return a list of instances used by subject
    """
    with open(path_file,'rb') as f:
        reader=DictReader(f)
        data=[d['instance'] for d in reader if d['subject']==subject and d['complete']=='True']
        ins_d=dict([(i.name,i) for i in instance_set])
        return [ins_d[x] for x in data]


def get_paths_by_subject(path_file,subject,fun):
    """
    returns a list of applying fun on instanaces for subject in path_file
    """
    with open(path_file,'rb') as f:
        reader=DictReader(f)
        data=[(d['instance'],fun(d)) for d in reader if d['subject']==subject]
        return np.array([fr for (x,fr) in data])



def calc_logp_path_length(model,instances,sub_path_lengths,max_trials=40):
    logging.debug('*Calling logp function guessing: {0} using {1}'.format(sub_path_lengths,[i.name for i in instances]))
    lp=0
    trials=1;
    for i,sr in zip(instances,sub_path_lengths):
        while True:
            logging.debug('Solving {0} (trials={1})'.format(i.name,trials))
            r=len(model.solve(i))
            logging.debug('model={0},data={1})'.format(r,sr))
            if  r ==  sr or trials > max_trials:
                break
            trials+=1
        mlp=-sum([(1./t) for t in range(1,trials)])
        lp+=mlp
        logging.debug('  Guessed {0} with {1} trials. mlp={2} lp={3}'.format(sr,trials,mlp,lp))
        trials=1
    logging.debug('*Total lp={0}'.format(lp))
    return lp

def string_to_move(mv_str):
    piece=mv_str.split('@')[0]
    (nc,nl,ns)=eval(mv_str.split('@')[1].replace('.',','))
    return piece,(nc,nl,ns)

def convert_path_to_states(path):
    header=['subject', 'instance', 'optimal_length', 'move_number', 'move', 'pre_actions', 'meta_move', 'rt', 'trial_number', 'progress', 'distance_to_goal']
    ins=dict([(i.name,i) for i in instance_set])[path[0][header.index('instance')]]
    states=[]
    ins_m=deepcopy(ins)
    for i in range(len(path)-1):
        states.append(rhstring(ins_m))
        do_move_from_fixed(ins_m,string_to_move(path[i][header.index('move')]))
    return ins,states


def convert_path_to_state_pairs(path):
    header=['subject', 'instance', 'optimal_length', 'move_number', 'move', 'pre_actions', 'meta_move', 'rt', 'trial_number', 'progress', 'distance_to_goal']
    ins=dict([(i.name,i) for i in instance_set])[path[0][header.index('instance')]]
    state_pairs=[]
    ins_m=deepcopy(ins)
    for i in range(len(path)-1):
       first_state=rhstring(ins_m)
       do_move_from_fixed(ins_m,string_to_move(path[i][header.index('move')]))
       state_pairs.append((first_state,rhstring(ins_m)))
    return ins,state_pairs

def calc_logp_unordered_states(model,subject_paths,max_trials=400):
    """
    Calculating the probability of getting sum(s_i). subject_paths is a list of paths and a path is a list of moves.
    """
    header=['subject', 'instance', 'optimal_length', 'move_number', 'move', 'pre_actions', 'meta_move', 'rt', 'trial_number', 'progress', 'distance_to_goal']
    lp=0
    trials=1;
    logging.debug('*Starting calc_logp_unordered_states on {0} paths with model={1} '.format(len(subject_paths),model))
    for path in subject_paths:
        path_name='_'.join(
                [path[0][header.index('subject')],path[0][header.index('instance')],path[0][header.index('trial_number')]])
        instance,states=convert_path_to_states(path)
        counters=dict([(x,None) for x in states])
        while trials<max_trials and None in counters.values():
            model_path=model.solve(instance)
            for pair_start in range(len(model_path)-1):
                state=rhstring(model_path[pair_start])
                if state in counters:
                    if counters[state] is None:
                        counters[state]=trials
            trials+=1
            logging.debug('function:unordered_states path:{0} trials:{1} hits:{2} path_length:{3} model:{4}'.format(
                path_name,trials,len([x for x in counters.values() if x is not None]),len(counters),model))
        lp+=trials_to_logp(counters)
        trials=1
    return lp




def calc_logp_unordered_action(model,subject_paths,max_trials=400):
    """
    Calculating the probability of getting sum(si->si+1). subject_paths is a list of paths and a path is a list of moves.
    """
    header=['subject', 'instance', 'optimal_length', 'move_number', 'move', 'pre_actions', 'meta_move', 'rt', 'trial_number', 'progress', 'distance_to_goal']
    lp=0
    trials=1;
    logging.debug('*Starting calc_logp_unordered_action on {0} paths with model={1} '.format(len(subject_paths),model))
    for path in subject_paths:
        path_name='_'.join(
                [path[0][header.index('subject')],path[0][header.index('instance')],path[0][header.index('trial_number')]])
        instance,state_path_pairs=convert_path_to_state_pairs(path)
        counters=dict([(x,None) for x in state_path_pairs])
        while trials<max_trials and None in counters.values():
            model_path=model.solve(instance)
            for pair_start in range(len(model_path)-1):
                pair=(rhstring(model_path[pair_start]),rhstring(model_path[pair_start+1]))
                if pair in counters:
                    if counters[pair] is None:
                        counters[pair]=trials
            trials+=1
            logging.debug('function:unordered_action path:{0} trials:{1} hits:{2} path_length:{3} model:{4}'.format(
                path_name,trials,len([x for x in counters.values() if x is not None]),len(counters),model))
        lp+=trials_to_logp(counters)
        trials=1
    return lp





def trials_to_logp(counters):
    """
    counters is a dict with #trials per stimuli
    """
    lp=0
    for trials in counters.values():
        if trials is None:
            lp+=NOT_FOUND_LOGLIK_VALUE
        lp+=sum([(1./t) for t in range(1,trials+1)])
    return lp



"""
Option 1: Path length
(summary stats: X-axis Instances, Y-axis mean path lengths for Model)
(report: logp for model and instance, semi-fitted)
(report: loo for model and instance, semi-fitted)
(report: model executions until getting the logp)
"""


"""
Option 2: Complete states unordered
(report: logp for model and instance(one), semi-fitted)
(report: model executions until getting the logp)
"""

"""
Option 3: Complete Action unordered
(report: logp for model and instance(one), semi-fitted)
(report: model executions until getting the logp)
"""

"""
Option 4: Distance to goal
(summary stats- X-axis:step#, Y-axis: mean distance)
calculates the exact sequence (10,9,8,9,9,4,3,2) very demanding
"""




