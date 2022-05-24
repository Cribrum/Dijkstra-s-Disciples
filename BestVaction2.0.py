import math
from typing import final
from operator import itemgetter
import os

def solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList):
	while (globalTime <= 1440):
		utilPerTimes = []
		for i in range(N):
			Time = math.ceil(math.sqrt(pow((currPos[0] - attractions[i][0]), 2) + pow((currPos[1] - attractions[i][1]), 2))) + attractions[i][5]
			if ((Time + globalTime - attractions[i][5]) < attractions[i][2]):
				Time += (attractions[i][2] - (Time + globalTime - attractions[i][5]))
			#print(Time)
			#print(i)
			if (Time > 0):
				utilPerTimes.append([attractions[i][4]/Time, Time, i])
			else:
				utilPerTimes.append([attractions[i][4], Time, i])
		#utilPerTimes.sort()
		utilPerTimes.sort(key=lambda x: x[0])
		utilPerTimes.reverse()
		#print(utilPerTimes)
		nextJob = []
		for i in range(N):
			TimeBackToEnd = math.ceil(math.sqrt(pow((200 - attractions[utilPerTimes[i][2]][0]), 2) + pow((200 - attractions[utilPerTimes[i][2]][1]), 2)))
			if (((globalTime + utilPerTimes[i][1] - attractions[utilPerTimes[i][2]][5]) <= attractions[utilPerTimes[i][2]][3]) and (attractions[utilPerTimes[i][2]][6] == False) and ((globalTime + utilPerTimes[i][1] + TimeBackToEnd) < 1440)):
				nextJob = [attractions[utilPerTimes[i][2]], utilPerTimes[i], i]
				attractions[utilPerTimes[i][2]][6] = True
				break
		if (len(nextJob) == 0):
			break
		globalTime += nextJob[1][1]
		#globalTime += nextJob[0][5]
		if (globalTime <= 1440):
			#print(globalTime)
			finalAttractionList.append(nextJob[1][2] + 1)
			finalUtilVal += nextJob[0][4]
			#print(finalUtilVal)
			currPos = (nextJob[0][0], nextJob[0][1])
	return len(finalAttractionList), finalAttractionList 
	



def read_input():
    N = int(input())
    #teleporters = [[int(i) for i in input().split()] for _ in range(K)]
    attractions = []
    for i in range(N):
        x, y, o, c, u, t = [int(i) for i in input().split()]
        attractions.append([x, y, o, c, u, t, False])
    return N, attractions

def read_data(f):
	N = int(f.readline())
	#teleporters = [[int(i) for i in input().split()] for _ in range(K)]
	attractions = []
	for i in range(N):
		x, y, o, c, u, t = [int(i) for i in f.readline().split()]
		attractions.append([x, y, o, c, u, t, False])
	return N, attractions


def main():
	#N, attractions = read_input()

	#print(N)
	#print(attractions)
	#currPos = [200, 200]
	#globalTime = 0
	#finalUtilVal = 0
	#finalAttractionList = []
	#numBestAttractions, listBestAttractions = solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList)
	#print(numBestAttractions, end = "\n")
	#for i in range(numBestAttractions):
	#	print(listBestAttractions[i], end = " ")

	directory = os.fsencode("/Users/christian.urbanek/Downloads/all_inputs")
    
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".in"): 
			#print(os.path.join(directory, filename))
			print(filename)
			combined = "/Users/christian.urbanek/Downloads/all_inputs" + str("/") + str(filename)
			f = open(combined, "r")
			N, attractions = read_data(f)
			#print(N)
			#print(attractions)

			currPos = [200, 200]
			globalTime = 0
			finalUtilVal = 0
			finalAttractionList = []
			numBestAttractions, listBestAttractions = solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList)

			combined2 = "/Users/christian.urbanek/Downloads/all_outputs" + str("/") + str(filename)
			combined2 = combined2.replace(".in", ".out")
			#combined2 = combined2.substring(0, str.length() - 3)
			#combined2 = combined2 + str(".out")
			f2 = open(combined2, "x")
			f2.write(str(numBestAttractions))
			f2.write("\n")
			for i in range(numBestAttractions):
				if (i < (numBestAttractions-1)):
					f2.write(str(listBestAttractions[i]))
					f2.write(" ")
				else:
					f2.write(str(listBestAttractions[i]))
			#print(f.readlines())
		else:
			continue


if __name__ == '__main__':
    main()