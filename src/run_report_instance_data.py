from sys import argv
from test import *

def report_instance_data(iterations, alg_ind, instance_ind):
    instance=instance_set[instance_ind]
    #astr=[make_Astar(heur=min_manhattan_distance,calcF=make_fCalc(0)),make_Astar(heur=min_manhattan_distance),make_Astar(),make_Astar(min_manhattan_distance,calcF=make_fCalc(1,1.5,1))][alg_ind]
    astr=[make_Astar(heur=min_manhattan_distance,calcF=make_fCalc(0)),make_Astar(heur=min_manhattan_distance),make_Astar(), make_Astar(min_manhattan_distance,calcF=make_fCalc(1,1.5,1)),make_Astar(min_manhattan_distance,calcF=make_fCalc(1,1.1,1)),make_Astar(min_manhattan_distance,calcF=make_fCalc(1,1.5,1)),make_Astar(min_manhattan_distance,calcF=make_fCalc(1,2.0,1))][alg_ind]
    for i in range(iterations):
        report_instance(instance,astr)

try:
   iterations=int(argv[1])
   alg_ind=int(argv[2])
   instance_ind=int(argv[3])
except:
    print "script <iterations> <alg_ind> <instance_ind> "
    exit()

report_instance_data(iterations, alg_ind, instance_ind)


