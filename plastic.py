from turtle import Turtle, TurtleScreen, TK, RawTurtle
import numpy as np
import turtle

class Plastic(RawTurtle):

	size = 1.5
	colour = '#99FFCC'
	ocean_density = 1.0273
	#gravity = 0.01

	def __init__(self, screen, ptype, density):
		super().__init__(screen)
		self.shape('circle')
		self.ptype = ptype
		self.density = density
		self.direction = -90
		self.seth(self.direction)
		self.init_x = ()
		self.init_y = ()
		self.targ_y = []
		self.gravity = abs(self.ocean_density - self.density)/10
		self.x = 0
		self.y = 0
		self.dx = 0
		self.dy = 0
		self.leftBound   = -self.screen.window_width() / 2
		self.rightBound  = self.screen.window_width() / 2
		self.topBound    = self.screen.window_height() / 2
		self.oceanBound  = self.topBound - 230 - (50*np.sqrt(2))
		self.bottomBound = -self.screen.window_height() / 2
		self.width = self.shapesize()[0]*10
		self.height = self.shapesize()[0]*10

	def init_pos(self, x):
		self.init_x = (x,)
		self.init_y = (self.oceanBound,)
		self.x, = self.init_x
		self.y, = self.init_y
		self.goto(self.x, self.y)

	def get_targs(self):
		self.targ_y.clear()
		if self.is_less_dense():
			self.targ_y.append(np.random.uniform(self.oceanBound,self.oceanBound-20))
		elif self.is_closely_dense():
			self.targ_y.append(np.random.uniform(self.oceanBound-50,self.oceanBound-100))
		else:
			self.targ_y.append(self.bottomBound+10)

	def calc_move(self):
		if not self.at_targ():
			self.dy-=self.gravity
		else:
			self.dy *= -0.5

	def move(self):
		self.calc_move()
		self.goto(self.xcor()+self.dx, self.ycor()+self.dy)

	def at_targ(self):
		return self.ycor() < self.targ_y[0]

	def is_less_dense(self):
		return self.density < self.ocean_density

	def is_closely_dense(self):
		if self.ptype == 'PE':
			return (self.ocean_density - self.density) < 0.1

	def angle_to_other(self, other):
		x1,x2 = self.x, other.x
		y1,y2 = self.y, other.y
		smaller_y = min(y1, y2)
		greater_y = max(y1, y2)
		if smaller_y == y1:
			smaller_x = x1
			greater_x = x2
		else:
			smaller_x = x2
			greater_x = x1
		angle = np.arctan2(smaller_y-greater_y, smaller_x-greater_x)*180/np.pi
		return angle

class Environment(TK.Canvas):
	width = 1280
	height = 1000
	def __init__(self, master=None):
		super().__init__(master)
		self.config(width=self.width,height=self.height)
		self.pack()


class Setup(TurtleScreen):
	colour_map = {
		'seablue':'#0099cc',
		'skyblue':'lightskyblue',
		'brown':'#745037',
		'tan':'#D4AB83',
		'white':'#e5eaf0'
	}
	
	def __init__(self, canvas):
		super().__init__(canvas)
		self.tracer(0,0)
		self.bgcolor(self.colour_map['skyblue'])
		self.graphics()


	def graphics(self):
		pen = RawTurtle(self)
		pen.speed('fastest')
		pen.color(self.colour_map['seablue'])
		pen.up()
		pen.goto(-640, 200)
		pen.down()
		pen.begin_fill()
		for i in range(2):
			pen.fd(1280)
			pen.rt(90)
			pen.fd(700)
			pen.rt(90)
		pen.end_fill()

		# Boat
		pen.up()
		pen.goto(-200, 270)
		pen.down()
		pen.color(self.colour_map['brown'])
		pen.begin_fill()
		pen.rt(45)
		pen.fd(100)
		pen.lt(45)
		pen.fd(250)
		pen.lt(45)
		pen.fd(100)
		pen.end_fill()

		# Mast
		pen.up()
		pen.goto(0, 270)
		pen.down()
		pen.color(self.colour_map['tan'])
		pen.begin_fill()
		pen.lt(45)
		for i in range(2):
			pen.fd(200)
			pen.lt(90)
			pen.fd(10)
			pen.lt(90)
		pen.end_fill()

		# Right Sail
		pen.up()
		pen.goto(0,470)
		pen.down()
		pen.color(self.colour_map['white'])
		pen.begin_fill()
		pen.rt(135)
		pen.fd(175*np.sqrt(2))
		pen.rt(135)
		pen.fd(175)
		pen.end_fill()
		# Left Sail
		pen.up()
		pen.fd(10)
		pen.begin_fill()
		pen.fd(175)
		pen.rt(135)
		pen.fd(175*np.sqrt(2))
		pen.end_fill()
		pen.ht()
