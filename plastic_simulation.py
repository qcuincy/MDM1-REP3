import math
import numpy as np
import turtle as t
import tkinter as TK
from turtle import *
from plastic import *

width = 1280
height = 1000
ocean_density = 1.0273
N = 1
total_N = N
init_year = 1975 # Starting year
final_year = 2100
yearDiff = final_year-init_year
years = 0
mass = 0
timeData = []

def get_color():
    r = lambda: np.random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

plastics = []
densities = [(0.85, 0.92), (1.1, 1.4), (0.89, 0.98), (1.04, 1.04), (0.86, 2)]
weights = [0.13, 0.20, 0.23, 0.04, 0.4]
sizes = [0.75, 1.5, 1, 1.25, round(np.random.uniform(0.75, 2), 2)]
plastic_width = 15
names = ['PP', 'PPA', 'PE', 'PS', 'OTHER']
colours = ['#4837e1', '#6F7285', '#0d8c7b', '#9A9CAA', '#ab8e26']
plastics_dict = {
        'PP':[densities[0], colours[0], weights[0], sizes[0]],
        'PPA':[densities[1], colours[1], weights[1], sizes[1]],
        'PE':[densities[2], colours[2], weights[2], sizes[2]],
        'PS':[densities[3], colours[3], weights[3], sizes[3]],
        'OTHER':[densities[4], colours[4], weights[4], sizes[4]]
    }

initial_x = []

root = TK.Tk()
root.geometry(f'{width}x{height}+250+0')
env = Environment(root)
screen = Setup(env)
TEXT = RawTurtle(screen)
TEXT.ht()

def is_taken(point):
    for p in np.linspace(int(point)-20, int(point)+20, 100):
        return int(p) in initial_x

def assign(names: list, plastics: dict, weights: list):
    plasticType = np.random.choice(names, p=weights)
    density = get_density(plastics[plasticType][0])
    return (plasticType, density)

def initialize():
    for i in range(N):
        ptype, density = assign(names, plastics_dict, weights)
        plastics.append(Plastic(screen, ptype=ptype, density=density))
        while True:
            init_x = int(np.random.uniform(plastics[i].leftBound+10, plastics[i].rightBound-10))
            if not is_taken(init_x):
                initial_x.append(init_x)
                plastics[i].init_pos(init_x)
                break
        plastics[i].get_targs()
    for p in plastics:
        p.up()



def get_density(dist):
    n1, n2 = dist
    return np.random.uniform(n1, n2)

def getDumpRate(years):
    dumping_R = 1.956352*math.exp(0.0428*years)
    return dumping_R

def get_percent():
    floaters = 0
    sinkers = 0
    for i in range(total_N):
        if plastics[i].density < ocean_density:
            floaters += 1
        else:
            sinkers += 1
    return ((floaters / total_N)*100, (sinkers / total_N)*100)

def get_type_percent():
    dic = {
        'PE':0,
        'PPA':0,
        'PP':0,
        'PS':0,
        'OTHER':0
    }
    for i in range(total_N):
        dic[plastics[i].ptype]+=1
    pe, ppa, pp, ps, other = dic['PE'], dic['PPA'], dic['PP'], dic['PS'], dic['OTHER'] 
    return (pe, ppa, pp, ps, other)

def addBall():
    global total_N
    ptype, density = assign(names, plastics_dict, weights)
    plastic = Plastic(screen, ptype=ptype, density=density)
    plastic.up()
    plastic.color(plastics_dict[plastic.ptype][1])
    if plastic.ptype == 'OTHER':
        if plastic.density > ocean_density:
            plastic.shapesize(1.75)
        else:
            plastic.shapesize(0.75)
    else:
        plastic.shapesize(plastics_dict[plastic.ptype][3])
    while True:
        init_x = int(np.random.uniform(plastic.leftBound+10, plastic.rightBound-10))
        if not is_taken(init_x):
            initial_x.append(init_x)
            plastic.init_pos(init_x)
            break
    plastic.get_targs()
    plastics.append(plastic)
    total_N += 1
    screen.ontimer(addBall,1000)



def update_year():
    year+=1
    return years

def update_states():
    global years, mass
    dumping_R = getDumpRate(years)
    p_floaters, p_sinkers = get_percent()
    pe, ppa, pp, ps, others = get_type_percent()
    mass += dumping_R
    TEXT.clear()
    TEXT.color('white')
    TEXT.ht()
    TEXT.up()
    TEXT.goto(-550, 400)
    TEXT.write(f'Year: {int(init_year+years)}',font=('Arial', '20', 'bold'))
    TEXT.up()
    TEXT.goto(200, 400)
    TEXT.write(f'Total Mass: {int(mass)} Million tonnes',font=('Arial', '18', 'bold'))
    TEXT.up()
    TEXT.goto(200, 375)
    TEXT.write(f'Floating: {int(p_floaters)}%',font=('Arial', '16', 'bold'))
    TEXT.up()
    TEXT.goto(200, 350)
    TEXT.write(f'Sunk: {int(p_sinkers)}%',font=('Arial', '16', 'bold'))
    TEXT.up()
    TEXT.goto(200, 325)
    TEXT.color(colours[2])
    TEXT.write(f'PE: {int((pe/total_N)*100)}%',font=('Arial', '12', 'bold'))
    TEXT.up()
    TEXT.goto(200, 300)
    TEXT.color(colours[1])
    TEXT.write(f'PPA: {int((ppa/total_N)*100)}%',font=('Arial', '12', 'bold'))
    TEXT.up()
    TEXT.goto(200, 275)
    TEXT.color(colours[0])
    TEXT.write(f'PP: {int((pp/total_N)*100)}%',font=('Arial', '12', 'bold'))
    TEXT.up()
    TEXT.goto(200, 250)
    TEXT.color(colours[3])
    TEXT.write(f'PS: {int((ps/total_N)*100)}%',font=('Arial', '12', 'bold'))
    TEXT.up()
    TEXT.goto(200, 225)
    TEXT.color(colours[4])
    TEXT.write(f'OTHERS: {int((others/total_N)*100)}%',font=('Arial', '12', 'bold'))
    if years == yearDiff:
        root.destroy()
    years += 1
    screen.ontimer(update_states, 1000)



def draw():
    for i in range(total_N):
        plastics[i].clear()
        if plastics[i].ptype == 'OTHER':
            if plastics[i].density > ocean_density:
                plastics[i].color('#ab8e26')
                plastics[i].shapesize(1.75)
            else:
                plastics[i].color('#ebdba3')
                plastics[i].shapesize(0.75)
        else:
            plastics[i].color(plastics_dict[plastics[i].ptype][1])
            plastics[i].shapesize(plastics_dict[plastics[i].ptype][3])
        plastics[i].move()
    screen.update()
    screen.ontimer(draw, 10)


initialize()
update_states()
addBall()
draw()

screen.mainloop()