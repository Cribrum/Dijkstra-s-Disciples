import math

def distance(coord1, coord2):
    return math.sqrt((pow(coord1[0] - coord2[0]), 2) + (pow(coord1[1] - coord2[1]), 2))

def rideTime(attraction, currTime):
    if(attraction[3] <= currTime):
        return math.inf
    if(attraction[2] > currTime):
        return attraction[5] + (attraction[2] - currTime)
    return attraction[5]

def totalTime(currAttraction, visitAttraction, currTime):
    return rideTime(visitAttraction, currTime) + distance([currAttraction[0], currAttraction[1]], [visitAttraction[0], visitAttraction[1]])

def solve(N, attractions, currPos, currTime):
    if(N < 1 or (currPos[0] == 200 and currPos[1] == 200 and currTime < 1440)):
        return [], 0
    values = []
    notAllNegative = False
    for i in range(N):
        tempAtt = attractions
        attraction = attractions[i]
        altTime = currTime - distance(currPos, attraction)
        if(altTime - distance([attraction[0], attraction[1]], [200, 200]) >= 0):
            notAllNegative = True
            tempSolve = solve(N - 1, tempAtt.remove(attraction), attraction, altTime)
            values[i] = (attraction[4] / totalTime(currPos, attraction, altTime)) + tempSolve[1]
        else:
            values[i] = -math.inf
    if(notAllNegative):
        best = max(values)
        bestAtt = attractions[values.index(best)]
        tempAtt = attractions
        bestTime = currTime - distance(currPos, bestAtt)
        bestSolve = solve(N - 1, tempAtt.remove(bestAtt), bestAtt, bestTime)
        bestVis = bestSolve[0].append(bestAtt)
    else:
        best = 0
        bestVis = []
    return bestVis, best

def read_input():
    N = int(input())
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
    bestAttractions = solve(N, attractions, currPos, 1440)[0]
    print(bestAttractions)

if __name__ == '__main__':
    main()