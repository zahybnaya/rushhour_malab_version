from test import *
from sys import argv

def test_log_likelihood(model,ins):
    plan=[RHInstance({'r':(3,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,2,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,0,3),'g':(3,2,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,0,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(1,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,3,3),'g':(3,4,2)},'easy1'),
          RHInstance({'r':(4,2,2),'y':(2,0,3),'o':(1,4,2)},{'p':(5,3,3),'g':(3,4,2)},'easy1'),
 ]
    count,ll=log_likelihood(ins,model,plan)
    print '{0},{1},{2}'.format(count,ll,model.__name__)

#    k=log_likelihood(ins,model,plan,sample_size=10)
#    print '{0},{1},{2}'.format(10,k,model.__name__)
#
#    k=log_likelihood(ins,model,plan,sample_size=50)
#    print '{0},{1},{2}'.format(50,k,model.__name__)
#
#    k=log_likelihood(ins,model,plan,sample_size=100)
#    print '{0},{1},{2}'.format(100,k,model.__name__)
#
#    k=log_likelihood(ins,model,plan,sample_size=1000)
#    print '{0},{1},{2}'.format(1000,k,model.__name__)
#
#    k=log_likelihood(ins,model,plan,sample_size=10000)
#    print '{0},{1},{2}'.format(10000,k,model.__name__)
#
models= [make_Astar(),make_Astar(search_lapse=0.4) ,make_Astar(search_lapse=0.2) ,make_Astar(lapse_rate=0.1)]
try:
	alg_ind = int(argv[1])
except:
	print 'ERROR: {} alg_id (0-3)'.format(argv[0])

test_log_likelihood(models[alg_ind],instance_set_easy[1])
