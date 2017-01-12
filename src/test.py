from rushhour import *
from astar import *
from try_pygame import *
from random import random,seed
from itertools import product
#import matplotlib.pyplot as plt



instance_set_easy=[ RHInstance({'r':(2,2,2),'g':(4,5,2)},{'y':(4,0,3),'p':(2,3,3)},'easy0')
, RHInstance({'r':(3,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,4,2)},'easy1')
, RHInstance({'r':(2,2,2),'g':(4,3,2),'b':(4,5,2)},{'o':(2,4,2),'y':(4,0,3),'p':(3,3,3)},'easy2')
, RHInstance({'r':(0,2,2),'b':(0,3,3),'g':(4,4,2)},{'y':(2,0,3),'p':(5,1,3)},'easy3')
, RHInstance({'r':(0,2,2),'b':(2,5,3),'o':(3,4,2)},{'g':(1,4,2),'y':(3,0,3),'p':(5,3,3)},'easy4')
,RHInstance({'r':(2,2,2),'g':(0,2,2),'o':(1,4,2), 'b':(3,4,3)},{'y':(5,0,3),'p':(0,3,3)},'easy5')
,RHInstance({'r':(0,2,2),'b':(0,3,3),'y':(3,0,3),'g':(3,4,3)},{'o':(2,4,2),'p':(5,1,3)},'easy6')
,RHInstance({'r':(0,2,2),'b':(2,4,2)},{'y':(3,0,3),'g':(5,3,2),'o':(1,4,2),'p':(4,3,3)},'easy7')
,RHInstance({'r':(2,2,2),'o':(4,5,2)},{'y':(4,0,3),'g':(5,0,2),'b':(3,3,3),'p':(5,2,3)},'easy8')
,RHInstance({'r':(2,2,2),'o':(4,4,2)},{'y':(1,0,3),'g':(2,4,2),'b':(5,0,3),'p':(4,0,3)},'easy9')]

instance_set = read_instances()

def magsize(instance):
    mag,nodes=constuct_mag(instance)
    return sum([len(v) for k,v in mag.iteritems()])

def test_astar_instance(i,astar):
    ins=instance_set_easy[i]
    path,stats=astar(ins)
    stats['solution']=len(path)
    stats['quality']=len(path)/float(opt_solution_instances[i])
    stats['instance']=i
    print stats
    show(path,['A* instance:{}'.format(i),''+str(stats)])


def instance_distribution(ins,astar,sample_size=100, include_location=False):
    hist=defaultdict(int)
    for sample in range(sample_size):
        path,stats=astar(ins)
        for p in range(len(path)):
            key=path[p]
            if include_location:
                key=(key,p)
            hist[key]+=1
    return hist

def test_instance_same():
    ins1=deepcopy(instance_set[0])
    print 'should be T: {}'.format(ins1 == instance_set[0])
    d={ins1:1}
    print 'should be 1: {}'.format(d[ins1])
    d[instance_set[0]]=2
    print 'should be 2: {}'.format(d[ins1])
    d[ins1]=3
    print 'should be 3: {}'.format(d[instance_set[0]])

def test_astar(play=False, heur=magsize, entry=make_fCalc(), is_stop=lambda x:False):
    for i in range(len(instance_set)):
        path,stats=Astar(instance_set[i],magsize,entry,is_stop)
        stats['solution']=len(path)
        stats['quality']=len(path)/float(opt_solution_instances[i])
        stats['instance']=i
        stats['h']=heur.__name__
        stats['entry']=entry.__name__
        stats['is_stop']=is_stop.__name__
        print stats
        if play:
            show(path,['A* instance:'+str(i),str(stats)])

def test_plan_instance(i):
    show(make_path_for_plan_model(instance_set[i],plan(instance_set[i])),[' plan_construction instance: '+str(i)])


def test_plan():
    for i in range(len(instance_set)):
        show(make_path_for_plan_model(instance_set[i],plan(instance_set[i]),' plan_construction instance: '+str(i)))

def g_plus_2h(g,h,s):
    return (g+1+2*h,g+1,2*h,s)
def no_g(g,h,s):
    return (h,g,h,s)
def rand_magsize(instance):
    return magsize*random()
def randh(instance):
    return randint(0,20)
def expandLG1000(stats):
    return stats['expanded']>1000
def expandLG2000(stats):
    return stats['expanded']>2000
def expandLG5000(stats):
    return stats['expanded']>5000
def noisy(heur,mean,sd):
    tmph = lambda instance: heur(instance)+gauss(mean,sd)
    tmph.__name__ = 'noisy_{}_({},{})'.format(heur.__name__,mean,sd)
    return tmph



#test_astar()
#test_astar(is_stop=expandLG1000)
#test_astar(is_stop=expandLG5000)
#test_astar(heur=randh)
#test_astar(entry=no_g)
#test_astar(entry=g_plus_2h)
#test_astar(heur=randh,is_stop=expandLG1000)
#test_astar(heur=randh,entry=g_plus_2h,play=True)
#show 1 as an example of plan vs. A*
#test_astar_instance(22)
#test_plan_instance(9)
#test_astar_instance(6,entry=no_g,heur=randh)
#test_astar_instance(4,is_stop=expandLG1000)


def draw_dist_instance(instance,alg_name,hist):
    print '~~~~~~~instance {} using {}~~~~~~~~~~~~'.format(instance.name,alg_name)
    max_path=max([k[1] for k in hist])
    samples_per_step=dict([(step,sum([v for k,v in hist.iteritems() if k[1]==step])) for step in range(max_path+1)])
    for k,v in sorted(hist.iteritems(),key=lambda x:x[0][1]):
        print 'Step {}:{}{}'.format(max_path-k[1],''.join(['*' for _ in range(v)]),float(v)/samples_per_step[k[1]])
    for k,v in samples_per_step.iteritems():
        print 'Step {}:{}{}'.format(max_path-k,''.join(['=' for _ in range(v)]),v)

def write_distribuition_raw(ins,astar,sample_size=100, include_location=False):
    print 'sample step state instance alg '
    for sample in range(sample_size):
        path,stats=astar(ins)
        path.reverse() #start to goal
        for p in range(len(path)):
            print '{} {} {} {} {} '.format(sample, p, path[p].__hash__(), ins.name,astar.__name__.replace(' ','_'))



# The way it should be: Generate a few A* instances with a name: 
# For each A* write_distribution_raw 

#astar_solvers=[make_Astar(),make_Astar(entry=no_g,heur=magsize)]
#
#inst=instance_set_easy[1]
#astar=astar_solvers[0]
#draw(inst)
#for i in range(10):
#    path,_=astar(inst)
#    draw(path[-1])
#
#for astar,inst in product(astar_solvers,instance_set_easy):
#    print(inst.__hash__())
#    path,_=astar(inst)
#    hist=instance_distribution(inst,astar,sample_size=100,include_location=True)
#    draw_dist_instance(inst,astar.__name__,hist)
#    write_distribuition_raw(inst,astar)



def flip_distribution_raw():
    with open('./results/raw_path_dist.csv','r') as f:
        tmp=[]
        last_step=0
        sample=0
        for l in f:
            l_s = l.split()[0]
            if l_s=='step':
                print l
                continue
            if l_s == '0':
                for tl in reversed(tmp):
                    tll=tl.split()
                    tll[0]=str(last_step-int(tll[0]))
                    print ' '.join([str(sample)]+tll)
                sample+=1
                tmp=[]
            else:
                last_step=int(l_s)
            tmp.append(l)
        for tl in reversed(tmp):
            tll=tl.split()
            tll[0]=str(last_step-int(tll[0]))
            print ' '.join([str(sample)]+tll)


#make_Astar(heur=zeroh,entry=entry,is_stop=lambda x:False, shuffle=False,lapse_rate=0):
astar_solvers=[make_Astar(heur=zeroh),make_Astar(lapse_rate=.01),make_Astar(lapse_rate=.1),make_Astar(calcF=make_fCalc(0.9,1,1),heur=randh)]
for astar,inst in product(astar_solvers,instance_set):
    hist=instance_distribution(inst,astar,sample_size=100,include_location=True)
    write_distribuition_raw(inst,astar)

#test_astar_instance(2,make_Astar(lapse_rate=.1))
#for i in range(len(instance_set_easy)):
#    test_astar_instance(i,make_Astar(calcF=make_fCalc(0.9,1,1),heur=randh))
#
