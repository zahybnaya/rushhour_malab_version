from heapq import heappop, heappush,heapify
#from graphics import *
from copy import deepcopy
from rushhour import *
from random import randint,random
#import numpy as np
from scipy.stats import rv_discrete


"""
Suboptimality:
    1) Using inadmissible heuristic - Factor it    (done)
    1) Using inadmissible heuristic - adding Gaussian noise (done)
    1) ClosedList expiration limitation (works well only with partial search)
    2) Lapses (done, not tested)
    6) Weighting of g+h (done)
    3) Partial search -Limited openList/Closed/Generated. (done)

Parameters:
"""

def zipf(total,rank,s):
    ret= (1/pow(rank,s)) / sum([1/pow(n,s) for n in total])
    return ret

def zipf_choice(vals,shape):
    ranks=sorted(vals)
    decision=random()
    t,r=0,0
    while True:
        t+=zipf(range(1,len(ranks)+1),r+1,shape)
        if t>=decision:
            return ranks[r]
        r+=1


def select_from_backtrace(backtrace,n,shape):
    dicts=backtrace[n]
    g=zipf_choice(dicts.keys(),shape)
    return choice(dicts[g])

def print_backtrace(backtrace):
    print '**************START backtrace print*************'
    for n in backtrace:
        print '-'
        for g in backtrace[n]:
            print '{}->{}'.format(g,len(backtrace[n][g]))
    print '**************END backtrace print*************'

def make_fCalc(gF=1,hF=1,gAddition=1):
    def tmp_f(g,h,s):
        return (gF*(g+gAddition)+hF*h,g+gAddition,hF,s)
    tmp_f.__name__='{0}*(g+{1})+{2}h'.format(gF,gAddition,hF)
    return tmp_f

def select_state_from_open(openList):
    p=[f for f,g,h,n in openList]
    norm=float(sum(p))
    p=[f/norm for f in p]
    distrib = rv_discrete(values=(range(len(openList)), p))
    f,g,h,n=openList[distrib.rvs(size=1)]
    return n


def heappop_shuffle(openList):
    nodes=[]
    minf=openList[0][0]
    while len(openList)>0:
        f,g,h,n = heappop(openList)
        nodes.append((f,g,h,n))
        if f!=minf:
            heappush(openList,(f,g,h,n))
            break
    e=choice(nodes)
    nodes.remove(e)
    for ee in nodes:
        heappush(openList,ee)
    return e

def zeroh(instance):
    return 0

def h_unblocked(instance,level=1):
    return len(find_constraints(instance.goal_car,instance,instance.goal_loc[0]))

def minimin(instance):
    pass

def make_Astar(heur=zeroh,calcF=make_fCalc(),is_stop=lambda x:False, lapse_rate=0,search_lapse=0,plan_correction_level=1,reconstruct_accuracy=100.0,search_limit=float('inf')):
    if lapse_rate>0:
        astar=make_Astar(heur,calcF,is_stop,0,search_lapse,plan_correction_level,reconstruct_accuracy,search_limit)
        def tmp_f(start):
            return lapsingAstar(start,astar,lapse_rate)
    else:
        def tmp_f(start):
            return Astar(start,heur,calcF,is_stop,search_lapse,plan_correction_level,reconstruct_accuracy,search_limit)
    tmp_f.__name__='A*h:{0}f:{1}istop:{2}lapse:{3}slapse:{4}reca:{5}'.format(heur.__name__,calcF.__name__,is_stop.__name__,lapse_rate,search_lapse,reconstruct_accuracy)
    return tmp_f

def RTA(start,heur=zeroh,calcF=make_fCalc(),is_stop=lambda x:False):
    plan=[start]
    physical_loc=start
    previous_loc=None
    potentials=[]
    while not physical_loc.is_goal():
        succs = expand(physical_loc)
        [heappush(potentials,(heur(s),s)) for s in succs if s != previous_loc]
        previous_loc=physical_loc
        _,physical_loc=heappop(potentials)
        draw(physical_loc)
        next_val,_ = heappop(potentials)
        potentials=[]
        heappush(potentials,(next_val+1,previous_loc))
        plan.append(physical_loc)
    return plan


def perfecth(instance,from_noise=0,to_noise=0):
    add_noise_val=from_noise + random()* (to_noise-from_noise)
    return len(Astar(instance)[0])*(1+add_noise_val)


def replace_in_open(openList,f_val):
    f,g,h,n=f_val
    for i in range(len(openList)):
        if openList[i][3]==n:
            openList[i]=f_val
            heapify(openList)
            return
    raise(Exception)


def reconstruct_path(backtrace,n,plan_correction_level,reconstruct_accuracy):
    """
    returns a list of states from start to the goal
    """
    path=[]
    while n in backtrace:
        path.append(n)
        g,n = backtrace[n]
    #path.append(n)
    path.reverse()
    return plan_correction(path,plan_correction_level)


def add_to_backtrace(backtrace,s,n,g):
    """
    Single backtrace per node
    """
    og,on=backtrace.get(s,(float('inf'),None))
    if g<og:
        backtrace[s]=(g,n)


def Astar(start,heur=zeroh,calcF=make_fCalc(),is_stop=lambda x:False, search_lapse=0,plan_correction_level=1,reconstruct_accuracy=100.0, search_limit=float('inf')):
    stats={'expanded':0,'generated':0,'open_size':0,'close_size':0,'stops':0}
    backtrace={}
    closed = set()
    openList = []
    #print 'PUSH '+str(start.__hash__())
    heappush(openList,(heur(start),0,heur(start),start))
    while len(openList)>0:
        if stats['expanded']>2500000:
	    print 'aborted. {}'.format(stats)
	    return [],stats
        if random() > search_lapse:
            f,g,h,n = heappop(openList)
        else:
            f,g,h,n = openList.pop(randint(0,len(openList)-1))
            heapify(openList)
        #print 'POP '+str(n.__hash__())
        if n.is_goal():
            return reconstruct_path(backtrace,n,plan_correction_level,reconstruct_accuracy),stats
        closed.add(n)
        succs = expand(n)
        for s in succs:
            #print 'GENERATED '+str(s.__hash__())
            if s in closed:
                continue
            old_g,_ = backtrace.get(s,(float('inf'),None))
            if old_g <= g:
                continue
            hs=heur(s)
            f_val=calcF(g,hs,s)
            if f_val[0] <= search_limit:
                add_to_backtrace(backtrace,s,n,g)
                if old_g != float('Inf'):
                    replace_in_open(openList,f_val)
                else:
                    heappush(openList,f_val)
        stats['open_size']=len(openList)
        stats['close_size']=len(closed)
        stats['generated']+=len(succs)
        stats['expanded']+=1
        if is_stop(stats):
            #print 'stopping'
            n=select_state_from_open(openList)
            path_,stats_ = Astar(n,heur,calcF,is_stop,search_lapse,plan_correction_level,reconstruct_accuracy)
            stats['stops']+=1
            stats['generated']+=stats_['generated']
            stats['expanded']+=stats_['expanded']
            path_ = reconstruct_path(backtrace,n,plan_correction_level,reconstruct_accuracy) + path_
            return path_,stats
    return [],stats

def astar_tasks(start,astar):
    tasks=find_tasks(start)
    ins = deepcopy(start)
    ttl_path=[start]
    for piece,location in tasks:
        ins.goal_car,ins.goal_loc=start.goal_car,start.goal_loc
        sane=sane_plan(ins)
        if sane is not None:
            ttl_path.extend(sane)
            break
        ins.goal_car,ins.goal_loc=piece,location
        path,stat=astar(ins)
        ttl_path.extend(path[1:])
        ins=deepcopy(path[-1])
    return ttl_path,stat


def lapsingAstar(start,astar,lapse_rate=0.01):
    path=[start]
    while 1:
        if path[-1].is_goal():
            return path,stat
        astar_path,stat=astar(path[-1])
        for i in range(1,len(astar_path)):
            if random()>lapse_rate:
                path.append(astar_path[i])
            else:
                path.append(rand_move(path[-1]))
                break


