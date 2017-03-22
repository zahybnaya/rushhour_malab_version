import re
from test import magsize
from collections import namedtuple
from rushhour import instance_dict,do_move_from_fixed,opt_solution_instances
from copy import deepcopy
from try_pygame import show
from astar import make_Astar

Rec=namedtuple('Rec','t event piece move_nu move instance')
Rec.__new__.__defaults__ = (None,) * len(Rec._fields)

def read_log(filename):
    recs=[]
    with open(filename,'r') as log:
        for l in log:
            recs.append(Rec(*[s.replace('[','').replace(']','') for s in re.findall('\[.*?\]',l)]))
    return recs


def recs_to_paths(recs,ins):
    paths=[]
    recs_ret=[]
    ins_rec= [r for r in recs  if r.instance == ins]
    mv_ins_rec= [r for r in ins_rec  if r.event == 'commit_move' or r.event== 'win' ]
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

#show_paths(argv[1],'Jam-8')

def calc_real_dist(filename):
    recs=read_log(filename)
    instances=set([r.instance for r in recs])
    a=make_Astar(heur=magsize)
    for ins in instances:
        paths,rs_paths=recs_to_paths(recs,ins)
        for path,rs_path in zip(paths,rs_paths):
            for i in range(len(path)):
                state=path[i]
                rec = rs_path[i]
                real_dist=len(a(state)[0])
                print rec,real_dist



def paths(filename):
    recs=read_log(filename)
    subject=filename.split('/')[-1]
    instances=set([r.instance for r in recs])
    for ins in instances:
        opt_solution=opt_solution_instances[ins]
        paths,rs_paths=recs_to_paths(recs,ins)
        for p,rs_p in zip(paths,rs_paths):
            solved= p[-1].is_goal()
            ttl_time = float(rs_p[-1].t)-float(rs_p[0].t)
            print '{}, {}, {}, {}, {}, {}'.format(subject, ins, opt_solution, len(p), solved, ttl_time)



#calc_real_dist(argv[1])
#TODO:
"""
Change log_likelihood function to use IBS
Submit the fittings of subjects
Drag and drop in experiment
Change of colors and square instead of Rectangle

Summary reports:
Surrenders vs restarts  () median + CI (show variability across subjects)
(stacked bars of solved/skipped/restarted )
#subjects who skipped per puzzle 
Stacked bars of response times/ human lengths.

Human solution length vs optimal solution length

Solving time vs optimal solution length
Distance from the goal vs move number
Backtracks
RT vs move number
RT per move
RT for subgoals and non-subgoals
RT vs distance to goal
RT vs number of legal moves
RT vs change in distance
"""


