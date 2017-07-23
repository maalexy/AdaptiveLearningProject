import pygame
import time
import pygame.draw
import random
from pygame.locals import *
from math import *

pln = 150.0 # length of the pole ( in cm, 1 px = 1 cm )
g = 10.0 # gravitational constant
a = 20.0 # max acceleration of the karts

phi = 0.5 # angle of the pole
anv = 0.0 # angular velocity of the pole
bet = 0.0 # angular acceleration of the pole
cen = 500.0
pos = cen # position of the cart (200 s the center)
vel = 0.0 # velocity of the cart
acc = 0.0 # current acceleration of the cart

pygame.init()
screen = pygame.display.set_mode((int(2*cen), 400))
lt = time.perf_counter()

while True:
	for ev in pygame.event.get():
		if ev.type == pygame.KEYDOWN:
			if ev.key == pygame.K_RETURN: # Enter stops the cart
				vel = 0
			if ev.key == pygame.K_SPACE: # Space resets the pole
				phi = random.uniform(-1, +1) * atan(1)
				vel = 0
				
	#modify the angle a bit, so the cart return to the center
	phit = phi + atan((pos-cen)/pln + vel)/3
	if anv * phit > 0:
		acc = copysign(a, phit)
	elif g*(1-cos(phit)) < (anv*pln/100)**2:
		acc = copysign(a, anv)
	elif g*(1-cos(phit)) > (anv*pln/100)**2:
		acc = copysign(a, -anv)
	
	# physics step
	nt = time.perf_counter()
	dt = nt - lt
	lt = nt
	vel += acc*dt
	pos += vel*dt*100
	bet = (g*sin(phi) - acc*cos(phi))/(pln/100)
	anv += bet*dt
	phi += anv*dt
	phi = fmod(phi, 2*pi)
	if phi > pi: phi = phi - 2*pi
	if phi < -pi: phi = phi + 2*pi
	
	
	# draw the picture
	nf = pygame.Surface(screen.get_size())
	nf = nf.convert()
	nf.fill((250, 250, 250))
	pygame.draw.line(nf, (0,0,0), (pos-10,200), (pos+10, 200), 3)
	pygame.draw.line(nf, (250, 0, 0), (pos, 200), (pos+sin(phi)*pln, 200-cos(phi)*pln), 1)
	pygame.draw.circle(nf, (250, 0, 250), (int(pos+sin(phi)*pln), int(200-cos(phi)*pln)), 10)
	screen.blit(nf, (0, 0))
	pygame.display.flip()

