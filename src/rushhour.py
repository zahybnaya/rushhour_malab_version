from collections import defaultdict
from graphviz import Digraph
from operator import itemgetter
from copy import deepcopy
from try_pygame import *
from random import choice


class RHInstance:
    length,height=6,6
    def __init__(self,h,v,name=''):
        self.h=h
        self.v=v
        self.name=name
    def __eq__(self, other):
        if isinstance(other, RHInstance):
            return ((self.h == other.h) and (self.v== other.v))
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        fs=frozenset(self.h.items() + self.v.items())
        return hash(fs)

def is_goal(instance):
    return instance.h['r']==(instance.length-2,2,2)

def mag_pairs(mg):
    return set([(k,k1) for k,v in mg.iteritems() for k1 in v ])

def unblocking_successors(instance):
    unblocking=[]
    others=[]
    mag,nodes=constuct_mag(instance)
    all_succ=expand(instance)
    for s in all_succ:
        mag_s,nodes_s=constuct_mag(s)
        if mag_pairs(mag_s)==mag_pairs(mag):
            others.append(s)
        else:
            unblocking.append(s)
    return unblocking,others

def rand_move(instance,unblocking=True):
    ub,b=unblocking_successors(instance)
    if unblocking:
        return choice(ub)
    return choice(expand(instance))

def rand_play(instance,path_length=30,allow_repeats=False):
    insc=deepcopy(instance)
    path=[insc]
    while not is_goal(insc) and len(path)<path_length:
        ub,b=unblocking_successors(insc)
        insc_s=choice(ub)
        added=False
        if allow_repeats or insc_s not in path:
            path.append(insc_s)
            added=True
        if added:
            insc=insc_s
    return path

def expand(instance):
    """
    All possible moves from current instance
    """
    succs=[]
    b=ground_instance(instance)
    for car,(c,l,s) in instance.h.iteritems():
        possible_moves = expand_piece_moves_given(c,l,s,'h',instance.length,instance.height)
        for m_c,m_l,m_s in possible_moves:
            if len([1 for x,y in find_path_to_location((c,l,s),(m_c,m_l,m_s),'h') if b[y][x] != ' '])==0:
                suc=deepcopy(instance)
                do_move(suc,(car,m_c-c))
                succs.append(suc)
    for car,(c,l,s) in instance.v.iteritems():
        possible_moves = expand_piece_moves_given(c,l,s,'v',instance.length,instance.height)
        for m_c,m_l,m_s in possible_moves:
            if len([1 for x,y in find_path_to_location((c,l,s),(m_c,m_l,m_s),'v') if b[y][x] != ' '])==0:
                suc=deepcopy(instance)
                do_move(suc,(car,m_l-l))
                succs.append(suc)
    return succs


def ground_instance(instance):
    b=[[' ']*instance.length for _ in range(instance.height)]
    for piece,vals in instance.h.iteritems():
        h_char,h_line,h_size = vals
        for hs in range(h_size):
            b[h_line][h_char+hs]=piece
    for piece,vals in instance.v.iteritems():
        v_char,v_line,v_size = vals
        for vs in range(v_size):
            b[v_line+vs][v_char]=piece
    return b

def draw(instance):
    b= ground_instance(instance)
    print ' _'+"".join([str(_) for _ in range(instance.length)]) + '_'
    i=0
    for l in b:
        print str(i)+'|'+"".join(l)+'|'
        i+=1
    print ' -'+"".join([str(_) for _ in range(instance.length)]) + '-'


def find_piece(instance,piece):
    st_piece =instance.v.get(piece,None)
    oriantation='v'
    if st_piece is None:
        st_piece=instance.h[piece]
        oriantation='h'
    return st_piece,oriantation

def do_move_from_fixed(instance,move):
    piece,(nc,nl,ns)=move
    (c,l,s),o=find_piece(instance,piece)
    if o == 'v':
        instance.v[piece]=(nc,nl,s)
    else:
        instance.h[piece]=(nc,nl,s)


def do_move(instance,move):
    piece,shift=move
    (c,l,s),o=find_piece(instance,piece)
    if o == 'v':
        instance.v[piece]=(c,l+shift,s)
    else:
        instance.h[piece]=(c+shift,l,s)

def expand_piece_moves_given(c,l,s,o,L,H):
    if o=='h':
        return [(nc,l,s) for nc in range(L-s+1) if nc != c]
    return [(c,nl,s) for nl in range(H-s+1) if nl != l]


def expand_piece_moves(instance,n):
    (c,l,s),o=find_piece(instance,n)
    return expand_piece_moves_given(c,l,s,o,instance.length,instance.height),o


def constuct_mag(instance):
    mag = defaultdict(dict)
    nodes = defaultdict(dict)
    mag['dummy']={'r':((0,2),(1,2),(2,2),(3,2))}
    closed = set([])
    q = ['r']
    while len(q)>0:
        n=q.pop()
        #print mag
        #print "Examining node "+n
        if n in closed:
            continue
        closed.add(n)
        locations = find_satisfying_locations(n,instance,mag)
        locations = dict([(k,v) for k,v in locations.iteritems() if v>0])
        #print 'found locations: {}'.format(locations)
        constraints=[]
        for l in locations:
            B = find_constraints(n,instance,l)  #(n,(x,y))
            #print 'finding constaints for location ' + str(l) + ': '+ str(B)
            constraints.append(B)
            locations[l]=(locations[l],[bn for bn,_ in B])
            nodes[n]=locations
        if len([_ for _ in constraints if len(_)==0])>0:
            continue
        for B in constraints:
            for nn,nconst in B:
                if nn not in mag[n]:
                    closed.discard(nn)
                    mag[n][nn]=[nconst]
                elif nconst not in mag[n][nn]:
                    mag[n][nn].append(nconst)
                if nn not in q:
                    q.append(nn)
    return mag,nodes


def move2occupiedtiles(move_m,oriantation):
    if oriantation=='h':
        return [(move_m[0]+i,move_m[1]) for i in range(move_m[2])]
    else:
        return [(move_m[0],move_m[1]+i) for i in range(move_m[2])]


def find_satisfying_locations(n,instance,mag):
    locs={}
    constraint_sets = [v[n] for k,v in mag.iteritems() if n in v]
    moves,o=expand_piece_moves(instance,n)
    for move_m in moves:
        locs[move_m]=0
        for cs in constraint_sets:
            if len(set(move2occupiedtiles(move_m,o)) & set(cs))==0:
                locs[move_m]+=1.0/len(constraint_sets)
    return locs


#def find_satis_locations(n,instance,mag):
#    locs=[]
#    if n=='r':
#        locs.append((instance.length-2,2,2)) #for the red
#    constraints = set([cc for k,v in mag.iteritems() if n in v for cc in v[n] ])
#    print "constratins for "+n+":" + str(constraints)
#    if len(constraints)==0:
#        return locs
#    moves,o=expand_piece_moves(instance,n)
#    print "all expanded moves for "+n +" :"+ str(moves)
#    for move_m in moves:
#        if len(set(move2occupiedtiles(move_m,o)) & constraints)==0:
#            locs.append(move_m)
#    print "satisfying moves  "+n +" :"+ str(locs)
#    return locs
#
def find_path_to_location(current_location,move_loc,oriantation):
    c,l,s=current_location
    move_loc_c, move_loc_l,_ = move_loc
    if oriantation=='h':
        if move_loc_c > c:
            path = [(i,l) for i in range(c+s,move_loc_c+s)]
        else:
            path = [(i,l) for i in range(move_loc_c,c)]
    else:
        if move_loc_l > l:
            path = [(c,i) for i in range(l+s,move_loc_l+s)]
        else:
            path = [(c,i) for i in range(move_loc_l,l)]
    #print 'found path for piece from '+str(current_location)+ ' to ' +str(move_loc)+ ': '+str(path)
    return path


def find_constraints(n,instance,loc):
    """
    return a set of (n,(x,y)) pairs, where x,y is the constraint that needs to be satisfied and n is the piece id that prevents it
    """
    constraints=[]
    st_piece,o=find_piece(instance,n)
    b=ground_instance(instance)
    path=find_path_to_location(st_piece,loc,o)
    for x,y in path:
        #print 'b['+str(x)+']['+str(y)+']='+b[x][y]
        if b[y][x] != ' ':
            constraints.append((b[y][x],(x,y)))
    return constraints


def mag2dot(mag):
    dot = Digraph()
    for n in mag:
        dot.node(n,n)
        for n1,c in mag[n].iteritems():
            dot.edge(n,n1,label=str(c))
    dot.render('tmp.gv', view=True)


def stop_dfs(instance,mag,nodes,n,visits,in_plan):
    options = [(move,(coverage,blocked_by)) for move,(coverage,blocked_by) in nodes[n].iteritems() if len(blocked_by)==0]
    l1 = [(move,(coverage,blocked_by)) for move,(coverage,blocked_by) in options if coverage==1.0]
    if len(l1)>0:
        #print 'stop_dfs on {} with coverage:{} and visits: {} returning {}'.format(n,coverage,visits[n],l1[0])
        return l1[0][0]
    l2 = [(move,(coverage,blocked_by)) for move,(coverage,blocked_by) in options if coverage==1/2.0 and visits[n]==2]
    if len(l2)>0:
        #print 'stop_dfs on {} with coverage:{} and visits: {} returning {}'.format(n,coverage,visits[n],l2[0])
        return l2[0][0]
    return None

def plan_location(n,nodes,in_plan):
    #print 'planning location for node {} according to {}'.format(n,nodes[n])
    for move,(coverage,blocked_by) in sorted([(k,v) for k,v in nodes[n].iteritems()],key=lambda x: x[1][0], reverse=True):
        #print 'checking {}'.format(move)
        if set(blocked_by) <= in_plan:
            return move


def dfs(instance,mag,nodes,n,visits,in_plan):
    visits[n]+=1
    plan_move=stop_dfs(instance,mag,nodes,n,visits,in_plan)
    #print 'DFS on {} with {} visits and a plan_move of {}'.format(n,visits[n],plan_move)
    if plan_move is not None:
        in_plan.add(n)
        return [(n,plan_move)]
    plan=[]
    for s in mag[n]:
        plan = dfs(instance,mag,nodes,s,visits,in_plan) + plan
    in_plan.add(n)
    return [(n,plan_location(n,nodes,in_plan))]+plan


def mag2plan(instance,mag,nodes):
    return dfs(instance,mag,nodes,'r',dict((n,0) for n in nodes),set())

def verify_plan(instance, tmp_plan):
    partial_plan=[]
    insc=deepcopy(instance)
    for m in reversed(tmp_plan):
        print 'verifing move '+str(m)
        if verify_move_for_plan(insc,m):
            do_move_from_fixed(insc,m)
            partial_plan.append(m)
            print 'Partial plan:'+str(partial_plan)
            draw(insc)
        else: return insc,partial_plan
    return None,partial_plan


def verify_move_for_plan(instance,piece_move):
    piece,(c,l,s)=piece_move
    return len(find_constraints(piece,instance,(c,l,s)))==0

def verify_move(instance,move):
    piece,shift=move
    (c,l,s),o=find_piece(instance,piece)
    if o=='h':
        if (c+shift+s) >= instance.length or c+shift<0: return False
        move_loc=(c+shift,l,s)
    else:
        if ((l+shift+s) >= instance.height or l+shift<0): return False
        move_loc=(c,l+shift,s)
    return len(find_constraints(piece,instance,move_loc))==0


def plan(instance):
    solving_instance=deepcopy(instance)
    returned_plan=[]
    while 1:
        mag,nodes=constuct_mag(solving_instance)
        tmp_plan=mag2plan(solving_instance,mag,nodes)
        solving_instance,partial_plan=verify_plan(solving_instance,tmp_plan)
        returned_plan.extend(partial_plan)
        if solving_instance is None:
            return returned_plan

def make_path_for_plan_model(ins,path_moves):
    path=[ins]
    insc=deepcopy(ins)
    for m in path_moves:
        insc=deepcopy(insc)
        do_move_from_fixed(insc,m)
        path.append(insc)
    path.reverse()
    return path


def test_mag(i):
    draw(i)
    mag,nodes=constuct_mag(i)
    mag2dot(mag)
    print nodes


def test():
    i1 = RHInstance({'r':(2,2,2),'g':(4,5,2)},{'y':(4,0,3),'p':(2,3,3)})
    i2 = RHInstance({'r':(3,2,2),'y':(2,0,3),'o':(4,4,2)},{'p':(5,0,3),'g':(3,4,2)})
    i3 = RHInstance({'r':(2,2,2),'g':(4,3,2),'b':(4,5,2)},{'o':(2,4,2),'y':(4,0,3),'p':(3,3,3)})
    i4 = RHInstance({'r':(0,2,2),'b':(0,3,3),'g':(4,4,2)},{'y':(2,0,3),'p':(5,1,3)})
    i5 = RHInstance({'r':(0,2,2),'b':(2,5,3),'o':(3,4,2)},{'g':(1,4,2),'y':(3,0,3),'p':(5,3,3)})
    i6 = RHInstance({'r':(2,2,2),'g':(0,2,2),'o':(1,4,2), 'b':(3,4,3)},{'y':(5,0,3),'p':(0,3,3)})
    # Test trivial case
    #mag={'r':{'a':(0,0),'b':(0,0)},'b':{'c':(),'d':()},'a':{},'c':{},'d':{}}
    #mag2dot(mag)
    #print mag2plan(i3,mag)
    #draw(i3)
    #mag=constuct_mag(i3)
    #mag['p']={}
    #mag2dot(mag)
    #print mag2plan(i3,mag)
    draw(i1)
    mag,nodes=constuct_mag(i1)
    print mag
    print nodes
    print mag2plan(i1,mag,nodes)
    #test_mag(i3)
    #find constraints
    #print find_constraints('y',i,(4,3))
    #print find_constraints('r',i,(4,2))

def test_stop():
    nodes={'y': {(4, 3, 3): (1.0, ['g'])}, 'p': {(2, 2, 3): (1.0, ['r']), (2, 0, 3): (1.0, ['r']), (2, 1, 3): (1.0, ['r'])}, 'r': {(3, 2, 2): (0.5, ['y']), (4, 2, 2): (1.0, ['y']), (0, 2, 2): (0.5, [])}, 'g': {(2, 5, 2): (1.0, ['p']), (1, 5, 2): (1.0, ['p']), (0, 5, 2): (1.0, ['p'])}}
    visits = dict((n,0) for n in nodes)
    mag = []
    i1 = RHInstance({'r':(2,2,2),'g':(4,5,2)},{'y':(4,0,3),'p':(2,3,3)})
    in_plan=set()
    print stop_dfs(i1,mag,nodes,'y',visits,in_plan)
    print stop_dfs(i1,mag,nodes,'p',visits,in_plan)
    print stop_dfs(i1,mag,nodes,'r',visits,in_plan)
    print stop_dfs(i1,mag,nodes,'g',visits,in_plan)
    visits['r']=2
    print stop_dfs(i1,mag,nodes,'r',visits,in_plan)

def test_verify_move():
    i1 = RHInstance({'r':(2,2,2),'g':(4,5,2)},{'y':(4,0,3),'p':(2,3,3)})
    draw(i1)
    print 'True: {}'.format(verify_move(i1,('r',-2)))
    print 'False: {}'.format(verify_move(i1,('r',-3)))
    print 'True: {}'.format(verify_move(i1,('y',+1)))
    print 'False: {}'.format(verify_move(i1,('y',-1)))
    print 'False: {}'.format(verify_move(i1,('y',+4)))
    print 'False: {}'.format(verify_move(i1,('r',+1)))
    print 'False: {}'.format(verify_move(i1,('r',+2)))
    print 'True: {}'.format(verify_move(i1,('g',-1)))
    print 'False: {}'.format(verify_move(i1,('g',-2)))
    print 'False: {}'.format(verify_move_for_plan(i1,('r',(3,2,2))))
    print 'True: {}'.format(verify_move_for_plan(i1,('r',(1,2,2))))
    print 'True: {}'.format(verify_move_for_plan(i1,('y',(4,1,3))))
    print 'False: {}'.format(verify_move_for_plan(i1,('y',(4,3,3))))


def make_instance(lines):
    colors='bwlBycMgmoptnsG'
    h,v={},{}
    name=lines[0].rstrip()
    size=lines[1].rstrip()
    red_car = lines[2].rstrip().split()
    h['r']=(int(red_car[0]),int(red_car[1]),int(red_car[3]))
    i=0
    for line in lines[3:]:
        car = line.rstrip().split()
        ((h,v)[car[2]=='v'])[colors[i]]=(int(car[0]),int(car[1]),int(car[3]))
        i+=1
    return RHInstance(h,v,name)

def read_instances(filename='./princeton_AI/code/jams.txt'):
    """
    read instances according to the format in https://www.cs.princeton.edu/courses/archive/fall11/cos402/assignments/programs/rushhour/
    """
    instance_set=[]
    with open(filename,'r') as insf:
        contents=insf.readlines()
    ins_begin=0
    for i in range(len(contents)):
        if contents[i].rstrip()=='.':
            instance_set.append(make_instance(contents[ins_begin:i]))
            ins_begin=i+1
    return instance_set


opt_solution_instances={ 0:9, 1:10, 2:15, 3:10, 4:10, 5:11, 6:14, 7:14, 8:13, 9:21, 10:27, 11:19, 12:24, 13:18, 14:24, 15:28, 16:28, 17:27, 18:23, 19:13, 20:22, 21:29, 22:30, 23:29, 24:41, 25:32, 26:34, 27:33, 28:34, 29:38, 30:39, 31:39, 32:49, 33:45, 34:48, 35:46, 36:49, 37:50, 38:58, 39:58}

