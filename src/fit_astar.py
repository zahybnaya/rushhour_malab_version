from fitting import *
from astar import make_Astar
from sys import argv
from test import log_likelihood,instance_set_easy,magsize
from rushhour import RHInstance


plan=[RHInstance({'r':(3,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,2,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,0,3),'g':(3,2,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,0,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,3,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(4,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,3,3),'g':(3,4,2)},'easy1'),
 ]

#def make_Astar(heur=zeroh,calcF=make_fCalc(),is_stop=lambda x:False, lapse_rate=0,search_lapse=0,plan_correction_level=1):

def lapse_alg(lapse_rate):
    return make_Astar(heur=magsize,lapse_rate=lapse_rate)

def lapse_in_search_alg(lapse_rate,search_lapse):
    return make_Astar(heur=magsize,lapse_rate=lapse_rate,search_lapse=search_lapse)

def partial_search(lapse_rate,max_expanded):
    def stop_X(stats):
        return stats['expanded']>max_expanded
    return make_Astar(heur=magsize,is_stop=stop_X,lapse_rate=lapse_rate,search_lapse=search_lapse)

def fit_plan(model_ind):
    stimuli=instance_set_easy[1]
    data=plan
    model,parameters,bounds={0:(lapse_alg,[0.1],((0,1))),
            1:(lapse_in_search_alg,[0.1,0.2],((0,1),(0,1))),
            2:(partial_search,[0.1,1000],((0,1),(10,500)))
            }[model_ind]
    #print 'fit({},{},{},{},{},{})'.format(stimuli,model,log_likelihood,parameters,bounds,data)
    print fit(stimuli,model,log_likelihood,parameters,bounds,data)


def test_00():
    stimuli=RHInstance({'r':(1,2,2)},{'o':(0,0,2)})
    data=[RHInstance({'r':(1,2,2)},{'o':(0,0,2)}),RHInstance({'r':(4,2,2)},{'o':(0,0,2)})]
    parameters=[-0.2, 0.1]
    bounds=((0,1),(0,1))
    print fit(stimuli,lapse_in_search_alg,log_likelihood,parameters,bounds,data)

try:
	alg_ind = int(argv[1])
except:
    print 'ERROR: {} alg_id (0-2)'.format(argv[0])
    exit(0)

fit_plan(alg_ind)
