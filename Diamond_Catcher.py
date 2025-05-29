from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

trapezoid ={'x':270, 'y':7, 'x1':440, 'width':230, 'height':28,"r":1.0,"g":1.0,"b":1.0}
diamond ={'x':random.randint(75, 300), 'y':800, 'width':28, 'height':35,"r":random.uniform(0.5, 1.0),"g":random.uniform(0.5, 1.0),"b":random.uniform(0.5, 1.0)}
score = 0
time_elasped = time.time()
speed = 200
freeze_button = False
end = False
game_started = False
start_time=0

def collision_checker(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1.0, 1.0, 1.0)  
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def zone_finder(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6 


def zone0_converter(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    else:
        return x, -y


def transforming_back_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    else:
        return x, -y

def midpoint_line_drawing(x,y,x1,y1,z):
    glPointSize(2)
    glBegin(GL_POINTS)

    dx = x1 - x
    dy = y1 - y
    d = 2 * dy - dx
    E = 2 * dy
    NE = 2* dy - 2* dx
    
    X, Y = transforming_back_from_zone0(x, y, z)
    glVertex2i(int(X), int(Y))
    for x in range(int(x), int(x1)):
        if d < 0:
            d += E
        else:
            y += 1
            d += NE
        X, Y = transforming_back_from_zone0(x, y, z)
        glVertex2i(int(X), int(Y))
    glEnd()

def line_drawer(x, y, x1, y1):
    
    z = zone_finder(x, y, x1, y1)
    n_x, n_y = zone0_converter(x, y, z)
    nw_x, nw_y = zone0_converter(x1, y1, z)
    if n_x > nw_x:
        n_x, n_y, nw_x, nw_y = nw_x, nw_y, n_x, n_y
    midpoint_line_drawing(n_x, n_y, nw_x, nw_y,z)


def draw_everything_else():
    global trapezoid, diamond
    #end button
    glColor3f(1.0, 0.0, 0.0)
    line_drawer(630, 639, 672, 665) 
    line_drawer(630, 665, 672, 639)


#trapezoid
    glColor3f(trapezoid['r'], trapezoid['g'], trapezoid['b'])
    line_drawer(trapezoid["x"], 7, trapezoid["x1"], 7)  
    line_drawer(trapezoid["x"] - 28, 35, trapezoid["x1"] + 28, 35)  
    line_drawer(trapezoid["x"] - 28.5, 35, trapezoid["x"], 7)  
    line_drawer(trapezoid["x1"] + 28.5, 35, trapezoid["x1"], 7)  

#diamond

    glColor3f(diamond['r'], diamond['g'], diamond['b']) 
    line_drawer(diamond['x'], diamond['y'], diamond['x'] + (diamond['width'] /2), diamond['y'] + (diamond['height'] /2))
    line_drawer(diamond['x'], diamond['y'], diamond['x'] + diamond['width'] /2, diamond['y'] - diamond['height'] /2)
    line_drawer(diamond['x'] + diamond['width'] /2, diamond['y'] - diamond['height'] /2, diamond['x'] + diamond['width'], diamond['y'])
    line_drawer(diamond['x'] + diamond['width']/2, diamond['y'] + diamond['height'] /2, diamond['x'] + diamond['width'], diamond['y'])
#refresh button
    glColor3f(0.0, 1.0, 1.0)
    line_drawer(14, 652, 70, 652) 
    line_drawer(14, 652, 42, 665)  
    line_drawer(14, 652, 42, 639) 

def draw_freeze_button():

    # press to pause
    glColor3f(1.0, 1.0, 0.0)
    line_drawer(336, 640, 336, 670) 
    line_drawer(351, 640, 351, 670)

def draw_unfreeze_button():
    glColor3f(1.0, 0.75, 0.0) 
    line_drawer(336, 640, 336, 670)
    line_drawer(336, 670, 366, 655) 
    line_drawer(336, 640, 366, 655)

def special_key_listener(key, x, y):
    global trapezoid, freeze_button, end
    if key == GLUT_KEY_RIGHT and not freeze_button and not end:
        if trapezoid['x1'] + 35 < 700:
            trapezoid['x'] += 30  
            trapezoid['x1']+= 30  

    elif key == GLUT_KEY_LEFT and not freeze_button and not end:
        if trapezoid['x'] - 35 > 0:
            trapezoid['x']-= 30
            trapezoid['x1'] -= 30

    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    global freeze_button, score, diamond, end,trapezoid, speed, time_elasped
    y = 700 - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 336 <= x <= 366 and 640 <= y <= 670 and not end:
            freeze_button = not freeze_button
        elif 630 <= x <= 672 and 639 <= y <= 665:
            print(f"Goodbye! Your Score: {score}")
            glutLeaveMainLoop()
        elif 14 <= x <= 70 and 639 <= y <= 665:

            
            diamond['x']=  random.randint(30, 660)
            if  14<=diamond['x'] <=70:
                 diamond['x'] = 80
            elif  630<=diamond['x']<= 672:
                 diamond['x'] =580
            elif  336<=diamond['x']<=366:
                 diamond['x'] =400
            diamond['r'], diamond['g'], diamond['b'] = random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)
            diamond['y'] =600
            trapezoid['r'], trapezoid['g'], trapezoid['b'] = 1.0, 1.0, 1.0
            freeze_button = False
            end = False
            speed = 200
            time_elasped = time.time()
            trapezoid['x'] = 270 
            trapezoid['x1'] = 440 
            score = 0
            print("Starting Over!") 

    glutPostRedisplay()


def animation():
    global diamond, score, freeze_button, trapezoid, end, time_elasped, speed, game_started, start_time
    t = time.time()   
    if not game_started and start_time == 0:
        start_time = t
        glutPostRedisplay()
        return   
    if not game_started:
        if t - start_time >= 0.15:  
            game_started = True
            time_elasped = t  
        glutPostRedisplay()
        return
    if end:
        return

    if freeze_button:
        time_elasped = t
        glutPostRedisplay()
        return
        
    d = t - time_elasped
    time_elasped = t
    diamond['y'] -= speed * d
    diamond_for_collision = {
    'x': diamond['x'], 
    'y': diamond['y'] - diamond['height'] * 0.5, 
    'width': diamond['width'],  
    'height': diamond['height']}
    trapezoid_for_collision = {
    'x': trapezoid['x'] - 28, 
    'y': trapezoid['y'], 
    'width': trapezoid['width'],  
    'height': trapezoid['height']}
    
    if collision_checker(diamond_for_collision, trapezoid_for_collision):                   
            score += 1
            print("Score:", score)
            diamond['r'], diamond['g'], diamond['b'] = random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)
            diamond['x']=random.randint(30, 660)
            diamond['y'] = 600 
            speed += 60
    elif diamond['y'] <= -28:
        end = True
        trapezoid['r'], trapezoid['g'], trapezoid['b'] = 1.0, 0.0, 0.0
        print("Game Over! Final Score:", score)

    glutPostRedisplay()

def viewport():
    glViewport(0, 0, 700, 700)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 700, 0.0, 700, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    viewport()

    if freeze_button:
        draw_unfreeze_button()
    else:
        draw_freeze_button()
    draw_everything_else()

    draw_text(10, 570, f"Score: {score}")

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(700, 700) 
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Diamond catching game-22201604")
glutDisplayFunc(display)
glutSpecialFunc(special_key_listener)
glutMouseFunc(mouse_listener)
glutIdleFunc(animation)
glutMainLoop()

