#!/usr/bin/env pypy3

import random
from random import randrange
import math

def inputs(N):
        coords = []
        for x in range(401):
                coords.append(x)
	#print(coords)
        print(N)
        tfactor = (200 / N)
        for x in range(N):
                currCoordsX = random.choice(coords)
                currCoordsY = random.choice(coords)
                coords.remove(currCoordsY)
                if(currCoordsX in coords):
                        coords.remove(currCoordsX)

		#o = random.randint(0,1240)
		#c = random.randint(o, (o+200))

		#u = random.randint(1, 100)
		#u *= 10

		#t = random.randint(1, 25)

                euclidianDistance = math.ceil(math.sqrt(pow((currCoordsX - 200), 2) + pow((currCoordsY - 200), 2)))

                o = euclidianDistance
                c = euclidianDistance * 2

                u = euclidianDistance
                u *= 10

                t = math.floor(random.randint(1, 30) * tfactor)

                #print(x, end = " ")
                print(currCoordsX, end = " ")
                print(currCoordsY, end = " ")
                print(o, end = " ")
                print(c, end = " ")
                print(u, end = " ")
                print(t)

def main():
        inputs(200)
        inputs(200)
        inputs(200)
        inputs(60)
        inputs(60)
        inputs(60)
        inputs(25)
        inputs(25)
        inputs(25)


	



if __name__ == '__main__':
        main()
