#!/usr/bin/env python

from time import sleep

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

UNIVERSE_WIDTH = 8
UNIVERSE_HEIGHT = 8

start_universe = [
	[0,0,0,0,0,0,0,0],
	[0,1,0,1,0,0,0,0],
	[0,0,0,1,0,1,0,0],
	[0,0,0,1,0,1,1,0],
	[0,0,0,0,0,0,0,0],
	[0,1,1,0,0,0,1,1],
	[0,0,0,0,0,0,0,1],
	[0,0,0,0,0,1,1,0]
]

def isAlive( c ):
	return c == 1

def drawMatrix( device, universe ):
	with canvas(device) as draw:
		for y in range(UNIVERSE_WIDTH):
			for x in range(UNIVERSE_HEIGHT):
				fill = 'white' if isAlive(universe[x][y]) else 'black'
				draw.point((x,y), fill=fill)
			

def showMatrix( universe ):
	for y in range(UNIVERSE_WIDTH):
		for x in range(UNIVERSE_HEIGHT):
			print( universe[x][y], end=' ')
		print()
	print()


def countNeighbours( universe, cellX, cellY):
	count = 0
	radius = [-1, 0, 1]
	for x in radius:
		posX = cellX + x
		if posX >= UNIVERSE_WIDTH or posX < 0:
			continue
		
		for y in radius:
			posY = cellY + y
			if posY >= UNIVERSE_HEIGHT or posY < 0:
				continue
				
			if cellX != posX or cellY != posY:
				count += universe[posX][posY]
	return count

def gameOfLife(universe):
	# make copy
	u = [row[:] for row in universe]
	
	for x in range(UNIVERSE_WIDTH):
		for y in range(UNIVERSE_HEIGHT):
			n = countNeighbours(universe, x, y)
			
			if isAlive( u[x][y] ):
				# cell with fewer than 2 neighbouirs dies : under populatino
				# cell with more than three neighbours dies : overpopoulation
				if n < 2 or n > 3:
					u[x][y] = 0

				# cell with 2 or 3 neighbours lives on
				elif n == 2 or n == 3:
					u[x][y] = 1
				
				
			elif n == 3:
				# become alive only of 3 neighbours
				u[x][y] = 1
				
	return u


if __name__ == '__main__':
	
	try:
		# led lights intensity [0-15]
		intensity = 4
				
		# create serial interface
		sr = spi( port=0, device=0, gpio=noop())
    
		# create led device
		dev = max7219(sr, cascaded=1, rotate=3)    
		dev.contrast( intensity * 16 )
		
		#initial universe
		universe = start_universe
		
		while 1:
			drawMatrix( dev, universe )
			showMatrix(universe)
			sleep(1)
			universe = gameOfLife( universe )
		
	except KeyboardInterrupt:
		print("Interrupted by user...")
		pass
	finally:
		print("Program stopped..")
