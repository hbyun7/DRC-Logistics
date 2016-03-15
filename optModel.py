from pymprog import *
import csv
import numpy as np

#data and index
with open("data/kPath.csv","rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        row1 = next(reader)

temp = row1[1:]
indexDict = {}

for i in range(len(temp)):

        indexDict[temp[i]] =i 



distm = np.loadtxt(open("data/kMat.csv","rb"),delimiter=',')
cm = np.loadtxt(open("data/kConditionMat.csv","rb"),delimiter=",")

iid,jid = range(len(distm)),range(len(distm))
seasonality = 1
if seasonality ==1:
        for i in iid:
            for j in jid:
                if cm[i][j]==1:
                    distm[i][j] = distm[i][j]*1.05
                elif cm[i][j]==2:
                    distm[i][j] = distm[i][j]*1.2
                elif cm[i][j]==3:
                    distm[i][j] = distm[i][j]*1.3
                elif cm[i][j]==4:
                    distm[i][j] = distm[i][j]*1.4
                else:
                    pass
                

E= [(i,j) for i in iid for j in jid if i!=j]

cities=[]
with open("data/kStarting.csv","rb") as csvfile:
    read = csv.reader(csvfile,delimiter=",")
    for item in read:
        cities.extend(item)
 


source = [indexDict["Nyunzu"]]
sink =[indexDict["Lubumbashi"]]
itm = [source[0],sink[0]]
season = "d"
#Modeling
beginModel("katanga")
x=var(E,'x', bool) #decision variable

#Objective function
minimize( sum(distm[i][j]*x[i,j] for i,j in E),"Total Time")

#constraints

#source
st([sum( x[i,j] for j in jid if i!=j)==1 for i in source],"leave")
st([(x[i,j])==0  for j in source for i in iid if i!=j],'no enter')

#sink
st([sum( x[i,j] for i in iid if j!=i)==1 for j in sink],"enter") 
st([(x[i,j])==0 for i in sink for j in jid if i!=j])

#conservation of flow
st([sum( x[i,j] for i in iid if i!=j)== sum( x[j,i] for i in iid if i!=j) for j in jid if j not in itm])

solve()
print("Total Cost = %g"%(vobj()))

routeList = []

for item in E:
	if x[item].primal > 0:
	 	routeList.append(item)

print "\nOriginal order:"
print(routeList)

sortedRoute = []

#the index of the node containing the origin
oindex = [sr[0] for sr in routeList].index(source[0])

#add the first node to the sortedRoute list
sortedRoute.append(routeList[oindex])

index = 0
#go until j of the last node in the sortedRoute list is equal to the destination; maybe add something later so that it removes the item from routeList, so it's easier to find index of item?
while sortedRoute[index][1] != sink[0]:
	loc = [sr[0] for sr in routeList].index(sortedRoute[index][1])
	sortedRoute.append(routeList[loc])
	index = index + 1
	
print "\nOrdered:"
print(sortedRoute)
print "\n"
for i in sortedRoute:
	print temp[i[0]],"-->",temp[i[1]],": ",distm[i[0]][i[1]]

brevRoute = []
start = 0
end = 0

while start < len(sortedRoute):
	distance = 0
	while "-" in temp[sortedRoute[end][1]]:
		distance = distance + distm[sortedRoute[end][0]][sortedRoute[end][1]]
		end = end + 1
	distance = distance + distm[sortedRoute[end][0]][sortedRoute[end][1]]

	brevRoute.append((sortedRoute[start][0],sortedRoute[end][1],distance))

	start = end + 1
	end = end + 1

print "\nAbbreviated:"
print(brevRoute)
print "\n"
for i in brevRoute:
	print temp[i[0]],"-->",temp[i[1]],": ",i[2]

			
			
			
			
