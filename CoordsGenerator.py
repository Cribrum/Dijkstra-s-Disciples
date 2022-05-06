#!/usr/bin/env pypy3

import random
from random import randrange
import math

def main():
	N = 200
	coords = []
	for x in range(401):
		coords.append(x)
	#print(coords)
	print(N)
	for x in range(200):
		currCoordsX = random.choice(coords)
		coords.remove(currCoordsX)
		currCoordsY = random.choice(coords)
		coords.remove(currCoordsY)

		#o = random.randint(0, 1240)
		#c = random.randint(o, (o+200))

		#u = random.randint(1, 100)
		#u *= 10

		#t = random.randint(1, 25)

		euclidianDistance = math.ceil(math.sqrt(pow((currCoordsX - 200), 2) + pow((currCoordsY - 200), 2)))

		o = euclidianDistance
		c = euclidianDistance * 2

		u = euclidianDistance
		u *= 10

		t = random.randint(1, 30)

		#print(x, end = " ")
		print(currCoordsX, end = " ")
		print(currCoordsY, end = " ")
		print(o, end = " ")
		print(c, end = " ")
		print(u, end = " ")
		print(t)


	



if __name__ == '__main__':
    main()
