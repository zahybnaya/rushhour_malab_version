from astar import LRTA, RTA, make_Astar
from instance_generator import json_to_ins
from rushhour import min_manhattan_distance, find_terminal_states
from sys import argv
from os import listdir
from os.path import join,isfile



def run_instance(jsonfile):
    ins=json_to_ins(jsonfile)
    terms=[(t.h,t.v) for t in find_terminal_states(ins)]

    def h_func(instance):
        return min_manhattan_distance(instance,terms)
    h_func.__name__='min_manhattan_distance'
    #rta=RTA(heur=h_func)
    lrta=LRTA(heur=h_func, iters=3)
    #rta_path=rta.solve(ins)
    #print ','.join([str(rta),jsonfile,str(len(rta_path))])
    lrta_path=lrta.solve(ins)
    print ','.join([str(lrta),jsonfile,str(len(lrta_path))])



def main(json_dir):
    print ','.join(['model,jsonfile,model_path_length'])
    jsons=[join(json_dir, f) for f in listdir(json_dir) if f.endswith('.json') and isfile(join(json_dir, f))]
    for f in jsons:
        run_instance(f)

try:
    json_dir = argv[1]
except:
    print 'usage <json_dir>'
main(json_dir)







