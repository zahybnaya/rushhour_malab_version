from heapq import heappop, heappush
from graphics import *
from copy import deepcopy
from rushhour import *
from random import randint
import numpy as np
from scipy.stats import rv_discrete


"""
Suboptimality:
    1) Using inadmissible heuristic - Factor it    (done)
    1) Using inadmissible heuristic - adding Gaussian noise (done)
    1) Shuffeling F values (done)
    1) ClosedList expiration limitation (works well only with partial search)
    2) Lapses (done, not tested)
    6) Weighting of g+h (done)
    3) Partial search -Limited openList/Closed/Generated. (done)

Parameters:
"""

def reconstruct_path(backtrace,n):
    """
    returns a list of states from the goal to the start
    """
    path=[]
    while n in backtrace:
        path.append(n)
        _,n = backtrace[n]
    path.append(n)
    return path

def entry(g,h,s):
    return (g+1+h,g+1,h,s)

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


def make_Astar(heur=lambda x:0,entry=entry,is_stop=lambda x:False, shuffle=False):
    def tmp_f(start):
        return Astar(start,heur,entry,is_stop, shuffle)
    tmp_f.__name__='A* h:{} entry:{} is_stop:{} shuffle:{}'.format(heur.__name__,entry.__name__,is_stop.__name__,shuffle)
    return tmp_f


def Astar(start,heur=lambda x:0,entry=entry,is_stop=lambda x:False, shuffle=False):
    stats={'expanded':0,'generated':0,'open_size':0,'close_size':0,'stops':0}
    backtrace={}
    closed = set()
    openList = []
    #print 'PUSH '+str(start.__hash__())
    heappush(openList,(heur(start),0,heur(start),start))
    while len(openList)>0:
        if shuffle:
            #print 'TEST THIS'
            f,g,h,n = heappop_shuffle(openList)
        else:
            f,g,h,n = heappop(openList)
            #print 'POP '+str(n.__hash__())
        if is_goal(n):
            return reconstruct_path(backtrace,n),stats
        closed.add(n)
        succs = expand(n)
        for s in succs:
            #print 'GENERATED '+str(s.__hash__())
            if s in closed:
                continue
            best_g,_ = backtrace.get(s,(float('inf'),None))
            if g+1 >= best_g: #already in open and not better
                continue
            # if in openlist and needs to be updates, remove push and hepify.
            backtrace[s]=(g+1,n)
            #print 'PUSH '+str(s.__hash__())
            heappush(openList,entry(g,heur(s),s))
        stats['open_size']=len(openList)
        stats['close_size']=len(closed)
        stats['generated']+=len(succs)
        stats['expanded']+=1
        if is_stop(stats):
            #print 'stopping'
            n=select_state_from_open(openList)
            path_,stats_ = Astar(n,heur,entry,is_stop)
            stats['stops']+=1
            stats['generated']+=stats_['generated']
            stats['expanded']+=stats_['expanded']
            path_.extend(reconstruct_path(backtrace,n))
            return path_,stats
    return 'failure'

def lapsingAstar(start,heur,entry,is_stop=lambda x:False, shuffle=False,lapse_rate=0.01):
    print 'TEST THIS'
    path=[start]
    while 1:
        if is_goal(path[-1]):
            return path
        astar_path=Astar(path[-1],heur,entry,is_stop, shuffle)
        astar_path.reverse()
        for i in range(1,len(astar_path)):
            if random()>lapse_rate:
                path.append(astar_path[i])
            else:
                path.append(rand_move(path[-1]))
                break


