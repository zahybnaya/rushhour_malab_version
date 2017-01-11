import sys,pygame


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

def draw_screen(screen,instance,text_cont):
    height_top=40
    car_w = screen.get_width()/instance.length
    car_h = (screen.get_height()-height_top)/instance.height
    screen.fill(GRAY)
    screen.fill(BLACK, (0,0,screen.get_width(), height_top))
    for line_num in range(len(text_cont)):
        font = pygame.font.SysFont("comicsansms", 15-(line_num*3))
        text = font.render(text_cont[line_num], True, (0, 255, 0))
        screen.blit(text, (0,20*line_num))
    for i in range(7):
        pygame.draw.line(screen,SILVER,(0,i*car_h+height_top),((6*car_w),i*car_h+height_top))
        pygame.draw.line(screen,SILVER,(i*car_w,height_top),(i*car_w,6*car_h+height_top))

    for h_car,place in instance.h.iteritems():
        c,l,s=place
        pygame.draw.rect(screen, colors[h_car] , (c*car_w, (l*car_h)+height_top, car_w*s, car_h))

    for car,place in instance.v.iteritems():
        c,l,s=place
        pygame.draw.rect(screen, colors[car] , (c*car_w, (l*car_h)+height_top, car_w, car_h*s))


def show(path,texts):
    path.reverse()
    pygame.init()
    height_top=40
    size = width, height = 400+height_top, 400
    screen = pygame.display.set_mode(size)
    i=-1
    model_name=texts[0]
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 275:
                    if i<len(path):
                        i=min(i+1,len(path)-1)
                elif event.key == 276:
                        i=max(0,i-1)
                elif event.key == 113:
                    return
                else: continue
                texts[0]='move {}/{}  model:{}'.format(i,len(path)-1,model_name)
                draw_screen(screen,path[i],texts)
                pygame.display.update()
            pygame.display.update()

