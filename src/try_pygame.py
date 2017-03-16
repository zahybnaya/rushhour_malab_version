import sys,pygame
from rushhour import do_move_from_fixed,find_piece,piece_possible_moves,opt_solution_instances


BLACK	=(0,0,0)
WHITE	=(255,255,255)
RED     =(255,0,0)
LIME	=(0,255,0)
BLUE	=(0,0,255)
YELLOW	=(255,255,0)
CYAN    =(0,255,255)
MAGENTA	=(255,0,255)
SILVER	=(192,192,192)
GRAY	=(128,128,128)
MAROON	=(128,0,0)
OLIVE	=(128,128,0)
GREEN	=(0,128,0)
PURPLE	=(128,0,128)
TEAL	=(0,128,128)
NAVY	=(0,0,128)


colors={'w':WHITE, 'l':LIME, 'B':BLACK, 'c':CYAN, 'M':MAGENTA, 's':SILVER, 'G':GRAY, 'm':MAROON, 't':TEAL, 'n':NAVY,'r':RED, 'g':GREEN, 'b':BLUE, 'y':YELLOW, 'p':PURPLE, 'o':OLIVE}

def draw_screen(screen,instance,text_cont,bold_piece=None,piece_selected=False):
    height_top=40
    car_w = screen.get_width()/instance.length
    car_h = (screen.get_height()-height_top)/instance.height
    screen.fill(GRAY)
    screen.fill(BLACK, (0,0,screen.get_width(), height_top))
    for line_num in range(len(text_cont)):
        font = pygame.font.Font('/Library/Fonts/Verdana.ttf', 15-(line_num*3))
        text = font.render(text_cont[line_num], True, (0, 255, 0))
        screen.blit(text, (0,20*line_num))
    for i in range(7):
        pygame.draw.line(screen,SILVER,(0,i*car_h+height_top),((6*car_w),i*car_h+height_top))
        pygame.draw.line(screen,SILVER,(i*car_w,height_top),(i*car_w,6*car_h+height_top))

    for h_car,place in instance.h.iteritems():
        c,l,s=place
        width=0
        if h_car==bold_piece:
            if piece_selected:
                pygame.draw.rect(screen, colors[h_car] , (c*car_w, (l*car_h)+height_top, car_w*s, car_h),width)
                pygame.draw.rect(screen, BLACK , (c*car_w+20, (l*car_h)+height_top+20, car_w*s-40, car_h-40))
            else:
                width=8
                pygame.draw.rect(screen, colors[h_car] , (c*car_w, (l*car_h)+height_top, car_w*s, car_h),width)
        else:
            pygame.draw.rect(screen, colors[h_car] , (c*car_w, (l*car_h)+height_top, car_w*s, car_h),width)

    for car,place in instance.v.iteritems():
        c,l,s=place
        width=0
        if car==bold_piece:
            if piece_selected:
                pygame.draw.rect(screen, colors[car] , (c*car_w, (l*car_h)+height_top, car_w, car_h*s),width)
                pygame.draw.rect(screen, BLACK , (c*car_w+20, (l*car_h)+height_top+20, car_w-40, car_h*s-40))
            else:
                width=8
                pygame.draw.rect(screen, colors[car] , (c*car_w, (l*car_h)+height_top, car_w, car_h*s),width)
        else:
            pygame.draw.rect(screen, colors[car] , (c*car_w, (l*car_h)+height_top, car_w, car_h*s),width)

def make_move(state,piece,move):
    m=piece,move
    do_move_from_fixed(state,m)
    return state

def select_piece(state,key):
    if key == pygame.K_r:
        piece='r'
    (c,l,s),o=find_piece(state,piece)
    print (c,l,s),o
    return piece,state

def play(state):
    pygame.init()
    height_top=40
    size = width, height = 700+height_top, 600
    screen = pygame.display.set_mode(size)
    i=0
    piece_selected=False
    piece=None
    pieces = [x for x in state.v] + [x for x in state.h]
    possible_moves=[None]
    move_ind=0
    piece_ind = 0
    o=None
    event_name=''
    log_msg='start: {}'.format(state.name)
    while 1:
        if state.is_goal():
            log_msg='EVENT:[{}] instance:[{}]'.format('win',state.name)
            print log_msg
            try:
                opt_sol = opt_solution_instances[state.name]-1 #because it includes the initial state
                sol_q = float(i)/opt_sol
            except:
                opt_sol = 'NA'
                sol_q = 'NA'
            info_msg='total moves:{} optimal_moves:{} solution_quality:{} . press q to continue'.format(i,opt_sol,sol_q)
            texts=[log_msg,info_msg]
            draw_screen(screen,state,texts,piece,piece_selected)
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
        texts=[log_msg,'']
        draw_screen(screen,state,texts,piece,piece_selected)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
                if not piece_selected:
                    if event.key == pygame.K_RIGHT:
                        piece_ind=(piece_ind+1)%len(pieces)
                        piece = pieces[piece_ind]
                        event_name='choose_piece'
                    elif event.key == pygame.K_LEFT:
                        piece_ind=(piece_ind-1)%len(pieces)
                        piece = pieces[piece_ind]
                        event_name='choose_piece'
                    elif event.key==pygame.K_SPACE:
                        piece_selected=True
                        possible_moves=piece_possible_moves(state,piece)
                        loc,o=find_piece(state,piece)
                        move_ind = possible_moves.index(loc)
                        event_name='select_piece'
                else:
                    if event.key == pygame.K_RIGHT and o == 'h' or event.key == pygame.K_DOWN and o == 'v':
                        move_ind=min((move_ind+1),len(possible_moves)-1)
                        state=make_move(state,piece,possible_moves[move_ind])
                        event_name='choose_move'
                    elif event.key == pygame.K_LEFT and o == 'h' or event.key == pygame.K_UP and o == 'v':
                        move_ind=max((move_ind-1),0)
                        state=make_move(state,piece,possible_moves[move_ind])
                        event_name='choose_move'
                    elif event.key==pygame.K_SPACE:
                        i+=1
                        piece_selected=False
                        possible_moves=[None]
                        piece=None
                        move_ind=0
                        event_name='commit_move'
            log_msg='EVENT:[{}] PIECE:[{}] MOVE_NUM:[{}] MOVE:[{}] instance:[{}]'.format(event_name,piece,i,possible_moves[move_ind],state.name)
            print log_msg

def show(path,texts=['unknown','unknown']):
    pygame.init()
    height_top=40
    size = width, height = 700+height_top, 600
    screen = pygame.display.set_mode(size)
    i=-1
    model_name=texts[0]
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if i<len(path):
                        i=min(i+1,len(path)-1)
                elif event.key == pygame.K_LEFT:
                        i=max(0,i-1)
                elif event.key == pygame.K_q:
                    return
                else: continue
                texts[0]='move {}/{}  model:{}'.format(i,len(path)-1,model_name)
                print texts
                draw_screen(screen,path[i],texts)
                pygame.display.update()
            pygame.display.update()

