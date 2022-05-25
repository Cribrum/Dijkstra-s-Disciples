import math
from typing import final
from operator import itemgetter
import os
import numpy as np
import random

def solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList):
	while (globalTime <= 1440):
		utilPerTimes = []
		for i in range(N):
			Time = math.ceil(math.sqrt(pow((currPos[0] - attractions[i][0]), 2) + pow((currPos[1] - attractions[i][1]), 2))) + attractions[i][5]
			if ((Time + globalTime - attractions[i][5]) < attractions[i][2]):
				Time += (attractions[i][2] - (Time + globalTime - attractions[i][5]))
			#print(Time)
			#print(i)
			attractions[i][6] = Time
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
			if (((globalTime + utilPerTimes[i][1] - attractions[utilPerTimes[i][2]][5]) <= attractions[utilPerTimes[i][2]][3]) and (attractions[utilPerTimes[i][2]][7] == False) and ((globalTime + utilPerTimes[i][1] + TimeBackToEnd) < 1440)):
				#simulated annealing stuff (globalTime is overall time in journey)
				nextJob = [attractions[utilPerTimes[i][2]], utilPerTimes[i], i]
				attractions[utilPerTimes[i][2]][7] = True
				attractions[utilPerTimes[i][2]][8] = globalTime
				break
		if (len(nextJob) == 0):
			break
		globalTime += nextJob[1][1]
		#globalTime += nextJob[0][5]
		if (globalTime <= 1440): # might have to account for this in simulated_annealing if running into issues
			#print(globalTime)
			finalAttractionList.append(nextJob[1][2] + 1)
			finalUtilVal += nextJob[0][4]
			#print(finalUtilVal)
			currPos = (nextJob[0][0], nextJob[0][1])
	return len(finalAttractionList), finalAttractionList, finalUtilVal, attractions
	
def simulated_annealing(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList, epoch, attraction_util_dict, numBestAttractions, listBestAttractions):
	# numBestAttractions, listBestAttractions, finalUtilVal, attractions = solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList)
	temp_list = [1/(numBestAttractions * (.2*i+1)) for i in range(numBestAttractions)]
	total = 0
	for i in range(len(temp_list)):
		total += temp_list[i]
	p_list = [elem/total for elem in temp_list]
	curr_edge = np.random.choice(listBestAttractions, p=p_list) # The random edge we are breaking greedy from
	curr_edge_best_attraction_index = listBestAttractions.index(curr_edge)
	if curr_edge == listBestAttractions[-1]: # if there are no edges after the current_edge (ex. if we only visit one edge), return the greedy output
		return numBestAttractions, listBestAttractions, finalUtilVal, attractions, epoch, attraction_util_dict
	else:
		# print(utilPerTimes)
		print(curr_edge)
		print(listBestAttractions)
		# print(attractions)
		# print(attractions[curr_edge-1])
		curr_attraction = attractions[curr_edge-1]
		globalTime = curr_attraction[8] # updates global time to reflect we are at curr_attraction

		attractions_visited = []
		for best_attraction in listBestAttractions:
			if listBestAttractions.index(best_attraction) > curr_edge_best_attraction_index:
				# attractions[utilPerTimes[best_attraction-1][2]][7] = False
				attractions[best_attraction-1][7] = False
			else:
				attractions_visited.append(best_attraction)
		
		# print(attractions)

		# print(globalTime)


		# for i in range(listBestAttractions.index(curr_edge), len(listBestAttractions)):
		# 	attractions[]

		# valid_next_attractions = []
		valid_next_indices = []
		for i in range(N):
			TimeBackToEnd = math.ceil(math.sqrt(pow((200 - attractions[i][0]), 2) + pow((200 - attractions[i][1]), 2)))
			# print(attractions[i][5])
			# print(attractions[i][3])
			if (((globalTime + attractions[i][6] - attractions[i][5]) <= attractions[i][3]) and (attractions[i][7] == False) and ((globalTime + attractions[i][6] + TimeBackToEnd) < 1440)):
				#simulated annealing stuff (globalTime is overall time in journey)
				attractions[i][8] = globalTime
				valid_next_indices.append(i)
				# valid_next_attractions.append(attractions[i]) # if I am getting weird ouput, mayb this should just be i? I have no idea how the indexing works
		
		# print(valid_next_attractions)

		if valid_next_indices == []: # TODO: Figure out why this would be empty (shouldn't be since Greedy finds val)
			return numBestAttractions, listBestAttractions, finalUtilVal, attractions, epoch, attraction_util_dict

		# new_edge = random.choice(valid_next_attractions)

		new_edge = random.choice(valid_next_indices)

		attractions_visited.append(new_edge)

		print(new_edge)


		attractions[new_edge-1][7] = True

		globalTime += attractions[new_edge-1][6]

		new_numBestAttractions, new_listBestAttractions, new_finalUtilVal, attractions = solve(N, attractions, [attractions[new_edge-1][0], attractions[new_edge-1][1]], globalTime, finalUtilVal, attractions_visited)

		if new_finalUtilVal > finalUtilVal:
			return new_numBestAttractions, new_listBestAttractions, new_finalUtilVal, attractions, epoch, attraction_util_dict
		else:
			thresh = random.uniform(0,1)
			temperature = 100000 - .01 * epoch
			exp_val = (finalUtilVal - new_finalUtilVal)/temperature
			p = math.exp(exp_val)
			if p > thresh:
				attraction_util_dict[finalUtilVal] = numBestAttractions, listBestAttractions
				return new_numBestAttractions, new_listBestAttractions, new_finalUtilVal, attractions, epoch, attraction_util_dict
			else:
				return numBestAttractions, listBestAttractions, finalUtilVal, attractions, epoch, attraction_util_dict



		

		# print(numBestAttractions, listBestAttractions, finalUtilVal, attractions)
		return 0

def run_simulated_annealing(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList):
	epoch = 1
	attraction_util_dict = {}
	numBestAttractions, listBestAttractions, finalUtilVal, attractions = solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList)


	while epoch < 100:
		numBestAttractions, listBestAttractions, finalUtilVal, attractions, epoch, attraction_util_dict = simulated_annealing(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList,epoch, attraction_util_dict, numBestAttractions, listBestAttractions)
		epoch += 1
	print(attraction_util_dict)
	if attraction_util_dict == {}:
		return numBestAttractions, listBestAttractions
	elif finalUtilVal >= max(attraction_util_dict):
		return numBestAttractions, listBestAttractions
	else:
		return attraction_util_dict[max(attraction_util_dict)]
	# return max(new_finalUtilVal, max(attraction_util_dict))



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
		attractions.append([x, y, o, c, u, t, False, 0, 0])
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

	# directory = os.fsencode("/Users/christian.urbanek/Downloads/all_inputs")




	# UNCOMMENT WHEN READY TO SUBMIT:
	directory = os.fsencode("/Users/ariwilson/Desktop/Algorithms/Dijkstra-s-Disciples/all_inputs")
    
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".in"): 
			#print(os.path.join(directory, filename))
			print(filename)
			# combined = "/Users/christian.urbanek/Downloads/all_inputs" + str("/") + str(filename)
			combined = "/Users/ariwilson/Desktop/Algorithms/Dijkstra-s-Disciples/all_inputs" + str("/") + str(filename)
			f = open(combined, "r")
			N, attractions = read_data(f)
			#print(N)
			#print(attractions)

			currPos = [200, 200]
			globalTime = 0
			finalUtilVal = 0
			finalAttractionList = []
			numBestAttractions, listBestAttractions, finalUtilVal, attractions = solve(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList)
			# print(numBestAttractions)
			# print(listBestAttractions)
			# print(finalUtilVal)
			# print(attractions)
			run_simulated_annealing(N, attractions, currPos, globalTime, finalUtilVal, finalAttractionList)

			# UNCOMMENT WHEN READY TO RUN:
			# combined2 = "/Users/ariwilson/Desktop/Algorithms/Dijkstra-s-Disciples/all_outputs" + str("/") + str(filename)
			# combined2 = combined2.replace(".in", ".out")
			# #combined2 = combined2.substring(0, str.length() - 3)
			# #combined2 = combined2 + str(".out")
			# f2 = open(combined2, "x")
			# f2.write(str(numBestAttractions))
			# f2.write("\n")
			# for i in range(numBestAttractions):
			# 	if (i < (numBestAttractions-1)):
			# 		f2.write(str(listBestAttractions[i]))
			# 		f2.write(" ")
			# 	else:
			# 		f2.write(str(listBestAttractions[i]))
			#print(f.readlines())
		else:
			continue


if __name__ == '__main__':
    main()