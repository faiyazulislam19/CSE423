from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

def plot_point(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_circle(xc, yc, x, y):
    plot_point(xc + x, yc + y)
    plot_point(xc - x, yc + y)
    plot_point(xc + x, yc - y)
    plot_point(xc - x, yc - y)
    plot_point(xc + y, yc + x)
    plot_point(xc - y, yc + x)
    plot_point(xc + y, yc - x)
    plot_point(xc - y, yc - x)

def midpoint_circle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r
    draw_circle(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        draw_circle(xc, yc, x, y)

def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def ZoneZeroConversion(zone, x, y):
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
        return -y, x
    elif zone == 7:
        return x, -y

def MidPointLine(zone, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    d_init = 2 * dy - dx
    d_e = 2 * dy
    d_ne = 2 * (dy - dx)
    x = x0
    y = y0
    while x <= x1:
        a, b = ZeroToOriginal(zone, x, y)
        plot_point(a, b)
        if d_init <= 0:
            x += 1
            d_init += d_e
        else:
            x += 1
            y += 1
            d_init += d_ne

def ZeroToOriginal(zone, x, y):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y

def eight_way_symmetry(x0, y0, x1, y1):
    zone = findZone(x0, y0, x1, y1)
    x_0, y_0 = ZoneZeroConversion(zone, x0, y0)
    x_1, y_1 = ZoneZeroConversion(zone, x1, y1)
    MidPointLine(zone, x_0, y_0, x_1, y_1)

def draw_bottle(x, y, r, h): #draw_bottle(480, 700, 15, 60)
    for i in range(0, r):
        midpoint_circle(x, y + r, r - i)
    eight_way_symmetry(x - r - 5, y - h, x + r + 5, y - h)  # Bellow line
    eight_way_symmetry(x, y + r, x + r + 5, y - h)  # Right line
    eight_way_symmetry(x, y + r, x - r - 5, y - h)  # Left Line

def draw_ramp(x1, y1, x2, y2):
    glColor3f(1.0, 1.0, 1.0)
    eight_way_symmetry(x1, y1, x2, y2)

def draw_ball(x, y, r, flag):
    if flag:
        for i in range(r):
            glColor3f(1.0, 0.0, 0.0)
            midpoint_circle(x, y + r, r - i)
    else:
        for i in range(r):
            glColor3f(0.0, 0.0, 0.0)
            midpoint_circle(x, y + r, r - i)

def iterate():
    glViewport(0, 0, 1280, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1280, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

drawing_in_progress = False
def idle():
    global input, drawing_in_progress
    glColor3f(0.0, 0.0, 0.0)
    if not drawing_in_progress:
        drawing_in_progress = True
        if input == 1:
            draw_bottle(480, 700, 15, 60)
        elif input == 2:
            draw_bottle(480 + 80, 700, 15, 60)
        elif input == 3:
            draw_bottle(480, 700, 15, 60)
            draw_bottle(480 + 80, 700, 15, 60)
            draw_bottle(480 + 80 * 2, 700, 15, 60)
            draw_bottle(480 + 80 * 3, 700, 15, 60)
            draw_bottle(480 + 80 * 4, 700, 15, 60)
        elif input == 4:
            draw_bottle(480 + 80 * 3, 700, 15, 60)
        elif input == 5:
            draw_bottle(480 + 80 * 4, 700, 15, 60)
        glColor3f(1.0, 1.0, 1.0)
        eight_way_symmetry(0, 700, 1280, 700)
        drawing_in_progress = False
        glutSwapBuffers()

def showScreen():
    global input
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0)
    eight_way_symmetry(0, 700, 1280, 700)  # line going through the bottle
    temp = 480
    x = temp

    for i in range(5):
        draw_bottle(x, 700, 15, 60)
        x += 80
    x = temp
    for i in range(6):
        if i <= 2:
            draw_ramp(x - 40, 700, x - 80, 0)  # Left lines of ramp
        else:
            draw_ramp(x - 40, 700, x, 0)  # Right lines of ramp
        x += 80
    y = 40
    r = 20
    if input in range(1, 6):
        for i in range(13):
            if input == 1:
                if i == 0:
                    draw_ball(temp-40+4, y, r-i//2, True)
                elif i == 12:
                    draw_ball(temp-40+i*3+4, y, r -i//2, False)
                    draw_ball(temp-40+(i-1)*3+4, y-50, r-(i-1)//2, False)
                else:
                    draw_ball(temp-40+i*3+4, y, r-i//2, True)
                    draw_ball(temp-40+(i-1)*3+4, y-50, r-(i-1)//2, False)
            elif input == 2:
                if i == 0:
                    draw_ball(temp+(80*(input-1))-40+4, y, r-i//2, True)
                elif i == 12:
                    draw_ball(temp+(80*(input-1))-40+i*3+4, y, r-i//2, False)
                    draw_ball(temp+(80*(input-1))-40+(i-1)*3+4, y-50, r-(i-1)//2, False)
                else:
                    draw_ball(temp+(80*(input-1))-40+i*3+4, y, r-i//2, True)
                    draw_ball(temp+(80*(input-1))-40+(i-1)*3+4, y-50, r-(i-1)//2, False)
            elif input == 3:
                if i == 0:
                    draw_ball(temp+(80*(input-1)), y, r-i//2, True)
                elif i == 12:
                    draw_ball(temp+(80*(input-1)), y, r-i//2, False)
                    draw_ball(temp+(80*(input-1)), y-50, r-(i-1)//2, False)
                else:
                    draw_ball(temp+(80*(input-1)), y, r-i//2, True)
                    draw_ball(temp+(80*(input-1)), y-50, r-(i-1)//2, False)
            elif input == 4:
                if i == 0:
                    draw_ball(temp+(80*(input-1))+40-4, y, r-i//2, True)
                elif i == 12:
                    draw_ball(temp+(80*(input-1))+40-i*3-4, y, r-i//2, False)
                    draw_ball(temp+(80*(input-1))+40-(i-1)*3-4, y-50, r-(i-1)//2, False)
                else:
                    draw_ball(temp+(80*(input-1))+40-i*3-4, y, r-i//2, True)
                    draw_ball(temp+(80*(input-1))+40-(i-1)*3-4, y-50, r-(i-1)//2, False)
            elif input == 5:
                if i == 0:
                    draw_ball(temp+(80*(input-1))+40-4, y, r-i//2, True)
                elif i == 12:
                    draw_ball(temp+(80*(input-1))+40-i*3-4, y, r-i//2, False)
                    draw_ball(temp+(80*(input-1))+40-(i-1)*3-4, y-50, r-(i-1)//2, False)
                else:
                    draw_ball(temp+(80*(input-1))+40-i*3-4, y, r-i//2, True)
                    draw_ball(temp+(80*(input-1))+40-(i-1)*3-4, y-50, r-(i-1)//2, False)
            y += 50
            glColor3f(1.0, 1.0, 0.0)
            glRasterPos2f(550, 755)  # Set position for the text
            text = "The Bowling Game"
            for character in text:
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))  # Draw each character

            glutSwapBuffers()
            time.sleep(0.5)  # Introduce a delay of 0.5 seconds between each ball

input = int(input("Position of the Bowl: "))
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1280, 800)  # window size
glutInitWindowPosition(125, 0)
wind = glutCreateWindow(b"The Bowling Game")
glutDisplayFunc(showScreen)
glutIdleFunc(idle)
glutMainLoop()