from sys import argv
from test import *
from itertools import product

def report_LRTA_instance_data(iterations, run_id):
    def lrta0(instance):
        return LRTA(instance,heur=lambda x: min_manhattan_distance(x),update_h=True,iters=1)

    def lrta1(instance):
        return LRTA(instance,heur=lambda x: min_manhattan_distance(x),update_h=True,iters=5)

    def lrta2(instance):
        return LRTA(instance,heur=lambda x: min_manhattan_distance(x),update_h=True,iters=10)

    def lrta3(instance):
        return LRTA(instance,heur=lambda x: min_manhattan_distance(x),update_h=True,iters=15)

    def lrta4(instance):
        return LRTA(instance,heur=lambda x: min_manhattan_distance(x),update_h=True,iters=25)

    def lrta5(instance):
        return LRTA(instance,heur=lambda x: 1.5*min_manhattan_distance(x),update_h=True,iters=25)


    runs=[_ for _ in product(range(20),range(6))]
    instance_ind,alg_ind=runs[run_id]

    instance=instance_set[instance_ind]
    lrta=[lrta0,lrta1,lrta2,lrta3,lrta4,lrta5][alg_ind]

    for i in range(iterations):
        report_LRTA_instance(instance,lrta)

try:
   iterations=int(argv[1])
   run_id=int(argv[2])
except:
    print "script <iterations> <run_id> "
    exit()

report_LRTA_instance_data(iterations, run_id)


