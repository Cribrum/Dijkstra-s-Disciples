import math
from typing import final
from operator import itemgetter

def solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList):
	while (globalTime <= 1440):
		utilPerTimes = []
		for i in range(N):
			Time = math.ceil(math.sqrt(pow((currPos[0] - attractions[i][0]), 2) + pow((currPos[1] - attractions[i][1]), 2))) + attractions[i][5]
			#print(Time)
			#print(i)
			utilPerTimes.append([attractions[i][4]/Time, Time, i])
		#utilPerTimes.sort()
		utilPerTimes.sort(key=lambda x: x[0])
		utilPerTimes.reverse()
		#print(utilPerTimes)
		nextJob = []
		for i in range(N):
			TimeBackToEnd = math.ceil(math.sqrt(pow((200 - attractions[utilPerTimes[i][2]][0]), 2) + pow((200 - attractions[utilPerTimes[i][2]][1]), 2)))
			if (((globalTime + utilPerTimes[i][1] - attractions[utilPerTimes[i][2]][5]) >= attractions[utilPerTimes[i][2]][2]) and ((globalTime + utilPerTimes[i][1] - attractions[utilPerTimes[i][2]][5]) <= attractions[utilPerTimes[i][2]][3]) and (attractions[utilPerTimes[i][2]][6] == False) and ((globalTime + utilPerTimes[i][1] + TimeBackToEnd) < 1440)):
				nextJob = [attractions[utilPerTimes[i][2]], utilPerTimes[i], i]
				attractions[utilPerTimes[i][2]][6] = True
				break
		if (len(nextJob) == 0):
			break
		globalTime += nextJob[1][1]
		#globalTime += nextJob[0][5]
		if (globalTime <= 1440):
			print(globalTime)
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

def main():
	N, attractions = read_input()
	print(N)
	print(attractions)
	currPos = [200, 200]
	globalTime = 0
	finalUtilVal = 0
	finalAttractionList = []
	bestAttractions = solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList)
	print(bestAttractions)


if __name__ == '__main__':
    main()