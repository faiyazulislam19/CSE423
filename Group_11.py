from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import randint

glutInit()
glutInitDisplayMode(GLUT_RGBA)


def init():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1000.0, 1000, -1000.0, 1000, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def WritePixel(x, y):
    # glPointSize(2.0)
    glBegin(GL_POINTS)
    glVertex2d(x, y)
    glEnd()


def blue():
    glColor3f(88 / 255, 110 / 255, 181 / 255)


def brown():
    glColor3f(111 / 255, 78 / 255, 55 / 255)


def red():
    glColor3f(215 / 255, 0.0, 0.0)


def white():
    glColor3f(1.0, 1.0, 1.0)


def green():
    glColor3f(78 / 255, 100 / 255, 39 / 255)


def drawline(x1, y1, x2, y2):
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        # WritePixel(x, y);
        points.append([x, y])
        if (d > 0):
            d = d + incNE
            y = y + 1
        else:
            d = d + incE
    return points


def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if (abs(dx) >= abs(dy)):
        if dx > 0 and dy > 0:
            zone = 0
        if dx <= 0 and dy > 0:
            zone = 3
        if dx <= 0 and dy <= 0:
            zone = 4
        if dx > 0 and dy <= 0:
            zone = 7
    else:
        if dx > 0 and dy > 0:
            zone = 1
        if dx <= 0 and dy > 0:
            zone = 2
        if dx <= 0 and dy <= 0:
            zone = 5
        if dx > 0 and dy <= 0:
            zone = 6

    return zone


def convert20(x1, y1, zone):
    if (zone == 0):
        a, b = x1, y1
    if (zone == 1):
        a, b = y1, x1
    if (zone == 2):
        a, b = y1, -x1
    if (zone == 3):
        a, b = -x1, y1
    if (zone == 4):
        a, b = -x1, -y1
    if (zone == 5):
        a, b = -y1, -x1
    if (zone == 6):
        a, b = -y1, x1
    if (zone == 7):
        a, b = x1, -y1
    return a, b


def revert(x, y, zone):
    if (zone == 0):
        a, b = x, y
    if (zone == 1):
        a, b = y, x
    if (zone == 2):
        a, b = -y, x
    if (zone == 3):
        a, b = -x, y
    if (zone == 4):
        a, b = -x, -y
    if (zone == 5):
        a, b = -y, -x
    if (zone == 6):
        a, b = y, -x
    if (zone == 7):
        a, b = x, -y
    return a, b


def line(x1, y1, x2, y2):
    zone = findzone(x1, y1, x2, y2)
    x1, y1 = convert20(x1, y1, zone)
    x2, y2 = convert20(x2, y2, zone)
    points = drawline(x1, y1, x2, y2)
    for i in points:
        i[0], i[1] = revert(i[0], i[1], zone)
        WritePixel(i[0], i[1])


def circlepoints(x, y, c_x, c_y):
    glBegin(GL_POINTS)
    x0, y0 = y, x
    x1, y1 = x, y
    x2, y2 = -x, y
    x3, y3 = -y, x
    x4, y4 = -y, -x
    x5, y5 = -x, -y
    x6, y6 = x, -y
    x7, y7 = y, -x
    glVertex2f(x0 + c_x, y0 + c_y)
    glVertex2f(x1 + c_x, y1 + c_y)
    glVertex2f(x2 + c_x, y2 + c_y)
    glVertex2f(x3 + c_x, y3 + c_y)
    glVertex2f(x4 + c_x, y4 + c_y)
    glVertex2f(x5 + c_x, y5 + c_y)
    glVertex2f(x6 + c_x, y6 + c_y)
    glVertex2f(x7 + c_x, y7 + c_y)

    glEnd()


def Circ(radius, c_x, c_y):
    d = 1 - radius
    x = 0
    y = radius
    circlepoints(x, y, c_x, c_y)
    while (x < y):
        if (d <= 0):
            d = d + 2 * x + 3
            x += 1
        else:
            d = d + 2 * x - 2 * y + 5
            x += 1
            y -= 1
        circlepoints(x, y, c_x, c_y)


def triangle(ax, ay, bx, by, cx, cy):
    line(ax, ay, bx, by)
    line(ax, ay, cx, cy)
    line(cx, cy, bx, by)


def square(xmin, ymin, xmax, ymax):
    line(xmin, ymin, xmax, ymin)
    line(xmin, ymin, xmin, ymax)
    line(xmax, ymax, xmax, ymin)
    line(xmax, ymax, xmin, ymax)


def rect(ax, ay, bx, by, cx, cy, dx, dy):
    line(ax, ay, bx, by)
    line(bx, by, cx, cy)
    line(cx, cy, dx, dy)
    line(dx, dy, ax, ay)


def tree(xmin, ymin, xmax, ymax):
    # main wood
    glColor3f(111 / 255, 78 / 255, 55 / 255)
    l1bx = xmin + 0.45 * (xmax - xmin)
    l2bx = xmin + 0.55 * (xmax - xmin)
    l1by = ymin
    l2by = ymin
    l1tx = xmin + 0.5 * (xmax - xmin)
    l2tx = xmin + 0.5 * (xmax - xmin)
    l1ty = ymin + 0.7 * (ymax - ymin)
    l2ty = ymin + 0.7 * (ymax - ymin)
    triangle(l1bx, l1by, l2bx, l2by, l1tx, l2ty)
    # line(l1bx,l1by,l1tx,l1ty)
    # line(l2bx,l2by,l2tx,l2ty)
    # line(l2bx,l2by,l1bx,l1by)
    l11bx = l1bx + 0.7 * (l1tx - l1bx)
    l11by = l1by + 0.7 * (l1ty - l1by)
    l21bx = l2bx + 0.7 * (l2tx - l2bx)
    l21by = l2by + 0.7 * (l2ty - l2by)
    l11tx = xmin + 0.25 * (xmax - xmin)
    l21tx = xmin + 0.75 * (xmax - xmin)
    l11ty = l1ty
    l21ty = l2ty
    # branches
    line(l11bx, l11by, l11tx, l11ty)
    line(l21bx, l21by, l21tx, l21ty)

    # leaves
    green()
    cx = xmin + 0.5 * (xmax - xmin)
    cy = ymin + 0.65 * (ymax - ymin)
    r = 0.25 * (ymax - ymin)
    Circ(r, cx, cy)
    r = 0.3 * (ymax - ymin)
    Circ(r, cx, cy)
    r = 0.325 * (ymax - ymin)
    Circ(r, cx, cy)
    r = 0.275 * (ymax - ymin)
    Circ(r, cx, cy)


def house(xmin, ymin, xmax, ymax, floor):
    each = (ymax - ymin) / floor
    y = ymin
    dxmin = xmin + 0.45 * (xmax - xmin)
    dxmax = xmin + 0.55 * (xmax - xmin)
    dymin = ymin
    dymax = ymin + 0.85 * each
    glColor3f(40 / 255, 100 / 255, 167 / 255)
    square(dxmin, dymin, dxmax, dymax)
    # for y in range(ymin,ymax,each):
    while (y <= ymax - each):
        yt = y + each
        glColor3f(0.8, 0.8, 0.8)
        line(xmin, y, xmax, y)
        line(xmin, yt, xmax, yt)
        brown()
        w1xmin = xmin + 0.15 * (xmax - xmin)
        w1xmax = xmin + 0.35 * (xmax - xmin)
        w1ymin = y + 0.2 * (yt - y)
        w1ymax = y + 0.8 * (yt - y)
        square(w1xmin, w1ymin, w1xmax, w1ymax)
        w1xmin = xmin + 0.65 * (xmax - xmin)
        w1xmax = xmin + 0.85 * (xmax - xmin)
        w1ymin = y + 0.2 * (yt - y)
        w1ymax = y + 0.8 * (yt - y)
        square(w1xmin, w1ymin, w1xmax, w1ymax)

        y += each
    glColor3f(1.0, 1.0, 1.0)
    square(xmin, ymin, xmax, ymax)


def car(xmin, ymin, xmax, ymax):
    s1xmin = xmin
    s1xmax = xmax
    s1ymin = ymin + 0.2 * (ymax - ymin)
    s1ymax = ymin + 0.6 * (ymax - ymin)
    red()
    square(s1xmin, s1ymin, s1xmax, s1ymax)
    s2xmin = xmin + 0.2 * (xmax - xmin)
    s2xmax = xmin + 0.7 * (xmax - xmin)
    s2ymin = ymin + 0.6 * (ymax - ymin)
    s2ymax = ymin + 1 * (ymax - ymin)
    # square(s2xmin,s2ymin,s2xmax,s2ymax)
    line(s2xmin, s2ymax, s2xmax, s2ymax)
    line(s2xmin, s2ymax, xmin + 0.1 * (xmax - xmin), s1ymax)
    line(s2xmax, s2ymax, xmin + 0.9 * (xmax - xmin), s1ymax)
    glColor3f(0.0, 0.0, 0.0)
    line(s1xmin + 0.1 * (xmax - xmin), s1ymax, s1xmin + 0.9 * (xmax - xmin), s1ymax)
    blue()
    wx1 = xmin + 0.15 * (xmax - xmin)
    wy1 = ymin + 0.65 * (ymax - ymin)
    wx2 = xmin + 0.85 * (xmax - xmin)
    wy2 = ymin + 0.65 * (ymax - ymin)
    wx3 = xmin + 0.7 * (xmax - xmin)
    wy3 = ymin + 0.95 * (ymax - ymin)
    wx4 = xmin + 0.225 * (xmax - xmin)
    wy4 = ymin + 0.95 * (ymax - ymin)
    rect(wx1, wy1, wx2, wy2, wx3, wy3, wx4, wy4)

    x = s2xmin + 0.5 * (s2xmax - s2xmin)
    line(x, s1ymin, x, ymax)
    glColor3f(1.0, 1.0, 1.0)
    # wheels
    glColor3f(0.3, 0.3, 0.3)

    cx = xmin + 0.2 * (xmax - xmin)
    cy = s1ymin
    r = 0.125 * (xmax - xmin)
    Circ(r, cx, cy)
    cx = xmin + 0.8 * (xmax - xmin)
    cy = s1ymin
    r = 0.125 * (xmax - xmin)
    Circ(r, cx, cy)
    cx = xmin + 0.2 * (xmax - xmin)
    cy = s1ymin
    r = 0.1 * (xmax - xmin)
    Circ(r, cx, cy)
    cx = xmin + 0.8 * (xmax - xmin)
    cy = s1ymin
    r = 0.1 * (xmax - xmin)
    Circ(r, cx, cy)


def man(xmin, ymin, xmax, ymax, type=0):
    brown()
    # head
    cx = xmin + 0.5 * (xmax - xmin)
    cy = ymin + 0.85 * (ymax - ymin)
    r = 0.15 * (ymax - ymin)
    Circ(r, cx, cy)
    # nose
    y1 = ymin + 0.85 * (ymax - ymin)
    y2 = ymin + 0.8 * (ymax - ymin)
    line(cx, y1, cx, y2)
    # eyes
    x1 = xmin + 0.3 * (xmax - xmin)
    x2 = xmin + 0.4 * (xmax - xmin)
    y = ymin + 0.9 * (ymax - ymin)
    line(x1, y, x2, y)
    x1 = xmin + 0.6 * (xmax - xmin)
    x2 = xmin + 0.7 * (xmax - xmin)
    line(x1, y, x2, y)

    if type == 0:
        # body
        green()
        x = xmin + 0.5 * (xmax - xmin)
        y1 = ymin + 0.4 * (ymax - ymin)
        y2 = ymin + 0.7 * (ymax - ymin)
        line(x, y1, x, y2)
        # legs
        blue()
        x = xmin + 0.5 * (xmax - xmin)
        y = ymin + 0.4 * (ymax - ymin)
        line(x, y, xmin, ymin)
        line(x, y, xmax, ymin)
        # hands
        brown()
        y = ymin + 0.55 * (ymax - ymin)
        line(xmin, y, xmax, y)
    if type == 1:
        # body
        green()
        x = xmin + 0.5 * (xmax - xmin)
        y1 = ymin + 0.4 * (ymax - ymin)
        y2 = ymin + 0.7 * (ymax - ymin)
        line(xmax, y1, x, y2)
        # hands
        brown()
        x1 = x + 0.5 * (xmax - x)
        y1 = y1 + 0.5 * (y2 - y1)
        line(x1, y1, xmin, y2)
        line(x1, y1, xmin, y1)
        # legs
        blue()
        x = xmax
        y = ymin + 0.4 * (ymax - ymin)
        line(x, y, xmin, ymin)
        line(x, y, xmax, ymin)
    if type == 2:
        # body
        green()
        x = xmin + 0.5 * (xmax - xmin)
        y1 = ymin + 0.4 * (ymax - ymin)
        y2 = ymin + 0.7 * (ymax - ymin)
        line(xmin, y1, x, y2)
        # hands
        brown()
        x1 = xmin + 0.5 * (x - xmin)
        y1 = y1 + 0.5 * (y2 - y1)
        line(x1, y1, xmax, y2)
        line(x1, y1, xmax, y1)
        # legs
        blue()
        x = xmin
        y = ymin + 0.4 * (ymax - ymin)
        line(x, y, xmin, ymin)
        line(x, y, xmax, ymin)
    if type == 3:
        # muscleman
        # body
        green()
        x1 = xmin + 0.35 * (xmax - xmin)
        ymx = ymin + 0.7 * (ymax - ymin)
        x2 = xmin + 0.65 * (xmax - xmin)
        x3 = xmin + 0.7 * (xmax - xmin)
        ymn = ymin + 0.4 * (ymax - ymin)
        x4 = xmin + 0.3 * (xmax - xmin)
        rect(x1, ymn, x2, ymn, x3, ymx, x4, ymx)
        # shoulder
        brown()
        cx = xmin + 0.15 * (xmax - xmin)
        cy = ymin + 0.65 * (ymax - ymin)
        r = (xmax - xmin) * 0.15
        Circ(r, cx, cy)
        cx = xmin + 0.85 * (xmax - xmin)
        Circ(r, cx, cy)
        # arms
        x = xmin + 0.15 * (xmax - xmin)
        y1 = ymin + 0.4 * (ymax - ymin)
        y2 = ymin + 0.575 * (ymax - ymin)
        line(x, y1, x, y2)
        x = xmin + 0.85 * (xmax - xmin)
        line(x, y1, x, y2)
        # legs
        blue()
        x1 = xmin + 0.45 * (xmax - xmin)
        x2 = xmin + 0.55 * (xmax - xmin)
        y = ymin + 0.4 * (ymax - ymin)
        line(x1, y, xmin, ymin)
        line(x2, y, xmax, ymin)


def sun(r, cx, cy):
    glColor3f(245/255, 159/255, 61/255)
    Circ(r, cx, cy)
    Circ(r-2, cx, cy)
    Circ(r-4, cx, cy)
    Circ(r-6, cx, cy)
    Circ(r-8, cx, cy)
    Circ(r-10, cx, cy)
    Circ(r-12, cx, cy)
    Circ(r-14, cx, cy)
    Circ(r-16, cx, cy)
    Circ(r-18, cx, cy)
    #Circ(r-20, cx, cy)
    #Circ(r-22, cx, cy)

    v = 30
    #triangle(cx - v, cy + r + 5, cx, cy + r + v, cx + v, cy + r + 5)
    #triangle(cx - v, cy - r - 5, cx, cy - r - v, cx + v, cy - r - 5)
    #triangle(cx + r + 5, cy - v, cx + r + v, cy, cx + r + 5, cy + v)
    #triangle(cx - r - 5, cy - v, cx - r - v, cy, cx - r - 5, cy + v)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # road1
    glColor3f(1.0, 1.0, 1.0)
    line(-1000, 200, 1000, 200)
    line(-1000, -100, 1000, -100)
    line(-600, -100, -1000, -1000)
    # colony
    house(-950, 200, -750, 600, 4)
    tree(-750, 200, -650, 400)
    house(-650, 200, -450, 500, 3)
    house(-450, 200, -250, 700, 5)
    tree(-250, 200, -150, 600)
    tree(-200, 200, -100, 400)
    tree(-150, 200, -50, 500)
    house(-50, 200, 150, 400, 2)
    tree(150, 200, 250, 600)
    house(250, 200, 400, 500, 3)
    house(400, 200, 600, 700, 5)
    tree(600, 200, 700, 400)
    house(700, 200, 900, 500, 3)
    tree(900, 200, 1000, 1000)

    sun(100, 0, 780)

    # cars
    v = 0
    car(-950 + v, 0, -800 + v, 100)
    car(-900 + v, -100, -750 + v, 0)
    car(-730 + v, -30, -570 + v, 70)
    car(-700 + v, 100, -500 + v, 200)

    v = 500
    car(-950 + v, 0, -800 + v, 100)
    car(-900 + v, -100, -750 + v, 0)
    car(-730 + v, -30, -570 + v, 70)
    car(-700 + v, 100, -500 + v, 200)

    v = 1000
    car(-950 + v, 0, -800 + v, 100)
    car(-900 + v, -100, -750 + v, 0)
    car(-730 + v, -30, -570 + v, 70)
    car(-700 + v, 100, -500 + v, 200)

    v = 1500
    car(-950 + v, 0, -800 + v, 100)
    car(-900 + v, -100, -750 + v, 0)
    car(-730 + v, -30, -570 + v, 70)
    car(-700 + v, 100, -500 + v, 200)

    # people
    v = 0
    man(800 + v, -1000, 1000 + v, -600, 3)
    v -= 200
    man(800 + v, -1000, 1000 + v, -600, 3)
    v -= 200
    man(700, -1000 + 400, 900, -600 + 400, 3)

    X = -800
    Y = -400

    for i in range(4):
        x = X
        y = Y
        for j in range(4):
            v = 0
            man(0 + v + x, -600 + y, 50 + v + x, -500 + y, randint(0, 2))
            v += 60
            man(0 + v + x, -600 + y, 50 + v + x, -500 + y, randint(0, 2))
            v += 60
            man(0 + v + x, -600 + y, 50 + v + x, -500 + y, randint(0, 2))
            v += 60
            man(0 + v + x, -600 + y, 50 + v + x, -500 + y, randint(0, 2))
            v += 60
            tree(0 + v + x, -600 + y, 50 + v + x, -400 + y)
            x += 80
            y += 180
        X += 300

    # side trees
    x1 = 0
    y = 0
    x2 = 0
    tree(-600 + x1, -200 + y, -500 + x1, 0 + y)
    for i in range(10):
        if i == 8:
            x2 += 150
            continue
        x1 -= 75
        y -= 150
        x2 += 150
        #side line tree
        tree(-600 + x1, -200 + y, -500 + x1, 0 + y)
        #horizontal line tree
        tree(-600 + x2, -300, -500 + x2, -100)

    # tree(100,100,400,400)
    # house(500,600,800,800,3)
    # car(-500,-400,0,0)
    # man(0,-500,250,0,3)
    # sun(50,-200,500)
    glutSwapBuffers()

def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global ballx, bally, create_new
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):    # 		// 2 times?? in ONE click? -- solution is checking DOWN or UP
            print(x,y)
            c_X, c_y = convert20(x,y)
            ballx, bally = c_X, c_y
        
    if button==GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN: 	
            create_new = convert20(x,y)
    # case GLUT_MIDDLE_BUTTON:
    #     //........

    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(900, 0)
glutCreateWindow(b"OpenGL Template")
glutDisplayFunc(showScreen)

init()

glutMainLoop()