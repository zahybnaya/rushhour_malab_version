import re
from sys import argv
from test import magsize,magsize_admissible
from collections import namedtuple,defaultdict
from rushhour import instance_dict,do_move_from_fixed,opt_solution_instances, min_manhattan_distance, rhstring
from copy import deepcopy
#from try_pygame import show
from astar import make_Astar, h_unblocked
from random import random

Rec=namedtuple('Rec','t event piece move_nu move instance')
Rec.__new__.__defaults__ = (None,) * len(Rec._fields)

PsiturkRec=namedtuple('PsiturkRec','worker ord t event piece move_nu move instance')
PsiturkRec.__new__.__defaults__ = (None,) * len(PsiturkRec._fields)

#debugPv12P:debugP70lV,6,1512669772746,""" t:[1512669772746] event:[start] piece:[NA] move#:[0] move:[NA] instance:[prb42331]"""

def read_psiturk_data(filename):
    recs=[]
    with open(filename,'r') as log:
        for l in log:
            v=l.split(',')[:2]
            v+=[s.replace('[','').replace(']','') for s in re.findall('\[.*?\]',l)]
            recs.append(PsiturkRec(*v))
    return recs


def read_log(filename):
    recs=[]
    with open(filename,'r') as log:
        for l in log:
            recs.append(Rec(*[s.replace('[','').replace(']','') for s in re.findall('\[.*?\]',l)]))
    return recs

def read_dist_log(filename):
    real_dists={}
    with open(filename,'r') as log:
        for l in log:
            ls=l.split('|')
            try:
                rec=eval(ls[0])
            except:
                continue
            dist=eval(ls[1])
            real_dists[rec]=dist
    return real_dists


def recs_to_paths(recs,ins):
    """
    Returns matching paths and records - state i in the path is the one after perfoming record i
    """
    #TODO add the time to restart
    paths=[]
    recs_ret=[]
    ins_rec= [r for r in recs  if r.instance == ins]
    mv_ins_rec= [r for r in ins_rec  if r.event == 'commit_move' or r.event== 'win' or r.event== 'restart']
    starts= [r for r in ins_rec  if r.event == 'start']
    instance = instance_dict()[ins]
    i=0
    for rs in range(len(starts)):
        p=[instance]
        r=[starts[rs]]
        try:
            next_rs=float(starts[rs+1].t)
        except:
            next_rs=float('inf')
        while i<len(mv_ins_rec) and float(mv_ins_rec[i].t) < next_rs  :
            if not p[-1].is_goal():
                _ins_=deepcopy(p[-1])
                if mv_ins_rec[i].event!='restart':
                    move=mv_ins_rec[i].piece,eval(mv_ins_rec[i].move)
                    do_move_from_fixed(_ins_,move)
                p.append(_ins_)
                r.append(mv_ins_rec[i])
            i+=1
        paths.append(p)
        recs_ret.append(r)
    return paths,recs_ret



def show_paths(filename,instance_name):
    paths,recs=recs_to_paths(read_log(filename),instance_name)
    print recs
    for p in paths:
        show(p)

def calc_real_dist(filename,dist_filename):
    rd=read_dist_log(dist_filename)
    recs=read_log(filename)
    instances=set([r.instance for r in recs])
    for ins in instances:
        paths,rs_paths=recs_to_paths(recs,ins)
        for path,rs_path in zip(paths,rs_paths):
            search_limit=opt_solution_instances[ins]+2
            for i in range(len(path)):
                state=path[i]
                rec = rs_path[i]
        if rec in rd:
            print 'skipped ' +str(rec)
            continue
        a=make_Astar(heur=min_manhattan_distance,search_limit=search_limit)
        the_path,stat=a(state)
        real_dist=len(the_path)
        if real_dist==0:
            search_limit=opt_solution_instances[ins]+2
        else:
            search_limit=real_dist+2 # one for the step and one for error 
            line='{0}|{1}|{2}|{3}|{4}|{5}\n'.format(rec,real_dist,stat['expanded'],stat['generated'],stat['open_size'],stat['close_size'])
        subject=filename.split('/')[-1]
        outf='../output/'+subject+'_md_dist.csv'
        with open(outf, 'a') as f:
            f.write(line)




#def calc_real_dist(filename):
#    recs=read_log(filename)
#    instances=set([r.instance for r in recs])
#    for ins in instances:
#        paths,rs_paths=recs_to_paths(recs,ins)
#        for path,rs_path in zip(paths,rs_paths):
#	    search_limit=opt_solution_instances[ins]+2
#            for i in range(len(path)):
#                state=path[i]
#                rec = rs_path[i]
#                a=make_Astar(heur=magsize_admissible,search_limit=search_limit)
#                the_path,stat=a(state)
#                real_dist=len(the_path)
#                search_limit=real_dist+1
#                print rec,real_dist
#
#
#            search_limit=opt_solution_instances[ins]+1
#            for i in range(len(path)):
#                state=path[i]
#                rec = rs_path[i]
#                a=make_Astar(heur=min_manhattan_distance,search_limit=search_limit)
#                the_path,stat=a(state)
#                real_dist=len(the_path)
#                search_limit=real_dist+2 # one for the step and one for error 
#                print '{0}|{1}|{2}|{3}|{4}|{5}'.format(rec,real_dist,stat['expanded'],stat['generated'],stat['open_size'],stat['close_size'])
#
#
#
# TODO: Add surrender,restart events to all logs


def moves(filename,dist_filename):
    print 'subject, instance, optimal_length, move_number, move, pre_actions,meta_move, rt, trial_number, progress, distance_to_goal'
    try:
        real_dists=read_dist_log(dist_filename)
    except:
        real_dists=defaultdict(lambda:'NA')
    recs=read_log(filename)
    subject=filename.split('/')[-1]
    pre_actions_counter=0
    trial_number=0
    for r in recs:
        ins=r.instance
        opt_solution=opt_solution_instances[ins]+1
        move_nu=r.move_nu
        pre_actions=pre_actions_counter
        pre_actions_counter+=1
        if r.event == 'start':
            trial_number+=1
            is_last_win=False
            initial_time=r.t
            pre_actions_counter=0
            prev_dist=opt_solution
        if r.event == 'commit_move' or r.event == 'win' :
            move='{0}@{1}'.format(r.piece,r.move).replace(',','.').replace(' ','')
            meta_move=r.event
            if r.event =='win':
                if is_last_win:
                    continue
                distance_to_goal=1
                is_last_win=True
            else:
                distance_to_goal=real_dists[r]
            try:
                progress= prev_dist - distance_to_goal
            except:
                progress='NA'
            try:
                assert(progress in set([0,1,-1,'NA']))
            except:
                print 'prev_dist:{} distance_to_goal:{} opt_solution:{}'.format(prev_dist,distance_to_goal,opt_solution)
                print 'progress:{}'.format(progress)
                print r
                progress='NA'

            prev_dist=distance_to_goal
            rt=float(r.t)-float(initial_time)
            initial_time=r.t
            pre_actions_counter=0
            nodes_expanded='NA'
            nodes_generated='NA'
            fields=[subject, ins, opt_solution, move_nu, move, pre_actions, meta_move, rt, trial_number, progress, distance_to_goal]
            print ','.join(['{}']*len(fields)).format(*fields)
            if r.event =='win':
                trial_number=0

def psiturk_paths(filename):
    print 'subject, instance, optimal_length, human_length, complete, rt,nodes_expanded, skipped, trial_number'
    recs=read_psiturk_data(filename)
    instances=set([r.instance for r in recs])
    subject = recs[0].worker
    for ins in instances:
        opt_solution=999
        nodes_expanded=999
        paths,rs_paths=recs_to_paths(recs,ins)
        trial_number=0
        for p,rs_p in zip(paths,rs_paths):
            solved= p[-1].is_goal()
            skipped= (trial_number==(len(paths)-1) and not solved)
            assert(rs_p[0].event=='start')
            ttl_time = float(rs_p[-1].t)-float(rs_p[0].t)
            fields=[subject, ins, opt_solution, len(p), solved, ttl_time, nodes_expanded, skipped, trial_number]
            print ','.join(['{}']*len(fields)).format(*fields)
            trial_number+=1

def paths(filename):
    expanded_nodes_unblocked={}
    for jam in range(1,39):
        expanded_nodes_unblocked['Jam-'+str(jam)]=36026 + int(jam*random()*10000)
    print 'subject, instance, optimal_length, human_length, complete, rt,nodes_expanded, skipped, trial_number'
    recs=read_log(filename)
    subject=filename.split('/')[-1]
    instances=set([r.instance for r in recs])
    for ins in instances:
        opt_solution=opt_solution_instances[ins]
        nodes_expanded=expanded_nodes_unblocked[ins]
        paths,rs_paths=recs_to_paths(recs,ins)
        trial_number=0
        for p,rs_p in zip(paths,rs_paths):
            solved= p[-1].is_goal()
            skipped= (trial_number==(len(paths)-1) and not solved)
            assert(rs_p[0].event=='start')
            ttl_time = float(rs_p[-1].t)-float(rs_p[0].t)
            fields=[subject, ins, opt_solution, len(p), solved, ttl_time, nodes_expanded, skipped, trial_number]
            print ','.join(['{}']*len(fields)).format(*fields)
            trial_number+=1
#TODO:

#example from psiurk:
#debugPv12P:debugP70lV,6,1512669772746,""" t:[1512669772746] event:[start] piece:[NA] move#:[0] move:[NA] instance:[prb42331]"""
"""
Look at nested-anova or factor analysis. in order to account for the subject as a random variable.  
Change log_likelihood function to use IBS
Submit the fittings of subjects
Drag and drop in experiment
Change of colors and the square instead of Rectangle

Summary reports:
1. Scatter plot of Human solution length, vs Optimal solution length, shape/color by instance. (done)
2. Instances optimal length ordered by the experiment.
3. Scatter plot of rt vs move_number
4. Counting the move_number occurences.
5. Barplot of Good/Neutral/Bad moves
6. Solution progress per instance (plot per subject)
7. Instance status (solved/restarted/skipped)
8. Barplot of Good/Neutral/Bad moves aggregate per subject
9. Rt per move_number, aggregated by subject
10. Scatter plot of Human solution length, vs Optimal solution length aggregated by instance
11. line plot of response-time as move number for each solution path
12. Plot of response-time as move number aggregated by move-number
13. Plot histograms of response times.
14. histogram of response times, normalized by median
15. histogram of response times, normalized by median, zoomed on (-1,1)
16. RT histograms per move category (good, neutral, wrong), trucncated (rt<15), with medians. 
17. RT per distance to goal
18. RT per distance to goal (normalized)
.distance_to_goal (across subjects)

Better admissble heuristic. (Something with the MAG)

.Stacked bars of response times/ human lengths.
.Solving time per instance histogram
.Solving time as a relation of expanded nodes
.num of backtracks per instances
. RT for subgoals and non-subgoals (find specific states with high RT)
. RT vs number of legal moves
. Surrenders vs restarts  median + CI (show variability across subjects)???
"""


#for k in psiturk_paths(argv[1]):
#    print k
