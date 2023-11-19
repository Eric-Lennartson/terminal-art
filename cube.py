import curses
from curses import wrapper
from time import sleep
import random
import math

class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

def rotate(vec, ax, ay, az):
    a = math.cos(ax)
    b = math.sin(ax)
    c = math.cos(ay)
    d = math.sin(ay)
    e = math.cos(az)
    f = math.sin(az)

    nx = c * e * vec.x - c * f * vec.y + d * vec.z
    ny = (a * f + b * d * e) * vec.x + (a * e - b * d * f) * vec.y - b * c * vec.z
    nz = (b * f - a * d * e) * vec.x + (a * d * f + b * e) * vec.y + a * c * vec.z

    return vec3(nx, ny, nz)

def scale(vec, x=1, y=1, z=1):
    return vec3(vec.x * x, vec.y * y, vec.z * z)

def translate(vec, x, y, z):
    nx = vec.x + x
    ny = vec.y + y
    nz = vec.z + z
    return vec3(nx, ny, nz)

def line(screen, vec1, vec2):
    xdist = math.ceil(abs(vec1.x - vec2.x))
    ydist = math.ceil(abs(vec1.y - vec2.y))

    dist = max(xdist, ydist)

    for i in range(dist):
        xpos = (map(i, 0, dist, vec1.x, vec2.x))
        ypos = (map(i, 0, dist, vec1.y, vec2.y))
        screen[int(ypos)][int(xpos)] = MAX_BRIGHT

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def clamp(value, minval, maxval):
    return max(min(value, maxval), minval)

def draw_cube(screen, cube):
    line(screen, cube[0], cube[1])
    line(screen, cube[1], cube[2])
    line(screen, cube[2], cube[3])
    line(screen, cube[3], cube[0])
    line(screen, cube[4], cube[5])
    line(screen, cube[5], cube[6])
    line(screen, cube[6], cube[7])
    line(screen, cube[7], cube[4])
    line(screen, cube[0], cube[4])
    line(screen, cube[1], cube[5])
    line(screen, cube[2], cube[6])
    line(screen, cube[3], cube[7])

def create_cube(x, y, size=10):
    a = vec3(x - size, y + size * 0.45, x + size)
    b = vec3(x + size, y + size * 0.45, x + size)
    c = vec3(x + size, y - size * 0.45, x + size)
    d = vec3(x - size, y - size * 0.45, x + size)
    e = vec3(x - size, y + size * 0.45, x - size)
    f = vec3(x + size, y + size * 0.45, x - size)
    g = vec3(x + size, y - size * 0.45, x - size)
    h = vec3(x - size, y - size * 0.45, x - size)
    return [a, b, c, d, e, f, g, h]

# globals
bright = [' ','.',':','-','=','+','*','#','%','@']
bcolors = [100, 101, 102, 103, 104, 105, 106]
MAX_BRIGHT = len(bright)-1
refresh_rate = 0.06

def map_color(rgb_value):
    return int(map(rgb_value, 0, 255, 0, 1000))

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0) # remove the cursor

    curses.init_color(100, map_color(96), map_color(214), map_color(108))
    curses.init_color(101, map_color(96), map_color(214), map_color(179))
    curses.init_color(102, map_color(96), map_color(136), map_color(214))
    curses.init_color(103, map_color(171), map_color(96), map_color(214))
    curses.init_color(104, map_color(214), map_color(96), map_color(157))
    curses.init_color(105, map_color(214), map_color(96), map_color(96))
    curses.init_color(106, map_color(214), map_color(122), map_color(96))
    curses.init_color(107, map_color(214), map_color(155), map_color(96))
    curses.init_color(108, map_color(214), map_color(206), map_color(96))
    curses.init_color(109, map_color(173), map_color(214), map_color(96))
    # color number, foreground, background
    curses.init_pair(10, 100, curses.COLOR_BLACK)
    curses.init_pair(9, 101, curses.COLOR_BLACK)
    curses.init_pair(8, 102, curses.COLOR_BLACK)
    curses.init_pair(7, 103, curses.COLOR_BLACK)
    curses.init_pair(6, 104, curses.COLOR_BLACK)
    curses.init_pair(5, 105, curses.COLOR_BLACK)
    curses.init_pair(4, 106, curses.COLOR_BLACK)
    curses.init_pair(3, 107, curses.COLOR_BLACK)
    curses.init_pair(2, 108, curses.COLOR_BLACK)
    curses.init_pair(1, 109, curses.COLOR_BLACK)

    rows = curses.LINES
    cols = curses.COLS-1 #idk why this is necessary

    screen = [[0 for x in range(cols)] for y in range(rows)]
    colors = [[0 for x in range(cols)] for y in range(rows)]

    centerx = cols/2
    centery = rows/2

    cube = create_cube(centerx, centery, 20)

    decay_rate = 0.8
    idx = 0.0

    while(True):
        stdscr.clear()

        # square(screen, sqr)
        draw_cube(screen, cube)

        # fill update the colors array
        for y in range(0, rows):
            for x in range(0, cols):
                colors[y][x] = int(idx)+1
                idx += 0.0045
                idx %= 10

        for v in range(len(cube)):
            cube[v] = translate(cube[v], -centerx, -centery, -centerx)
            cube[v] = scale(cube[v], 1, 1 / 0.45, 1)
            cube[v] = rotate(cube[v], 0.015, 0.015, 0.001)
            cube[v] = scale(cube[v], 1, 0.45, 1) # adjusting back
            cube[v] = translate(cube[v], centerx, centery, centerx) # adjusting back

        # read over the entire screen and display based on brightness
        for y in range(0, rows):
            for x in range(0, cols):
                b = bright[ math.ceil(screen[y][x]) ]
                # stdscr.addstr(y, x, b, curses.A_BOLD if b == '@' else curses.A_NORMAL)
                stdscr.addstr(y, x, b, curses.color_pair(colors[y][x]))
                if screen[y][x] > 0:
                    screen[y][x] = max(0, screen[y][x] - decay_rate)

        # if curses.can_change_color():
        #     stdscr.addstr(0,0, str(curses.COLORS))
        # stdscr.addstr(0, 0, "decay_rate: " + str(decay_rate))

        stdscr.refresh()
        sleep(refresh_rate)

wrapper(main)