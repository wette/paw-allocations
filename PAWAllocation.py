#!/usr/bin/python3

import random
import matplotlib.pyplot as plt
from solver import Solver
from ILPSolver import ILPSolver
from MontecarloSolver import MontecarloSolver
import sys

random.seed(284594534951)

#which solver to use?
solver = ILPSolver()
#solver = MontecarloSolver()


#Available projects:
#######################
solver.addProject(projectName="P1",  maxParticipants=16, minELM=4, minMBM=4, minWIM=4)
solver.addProject(projectName="P2",  maxParticipants=16, minELM=4, minMBM=4, minWIM=4)
solver.addProject(projectName="P3",  maxParticipants=16, minELM=4, minMBM=4, minWIM=4)
solver.addProject(projectName="P4",  maxParticipants=16, minELM=4, minMBM=4, minWIM=4)
solver.addProject(projectName="P5",  maxParticipants= 8, minELM=2, minMBM=2, minWIM=2)
solver.addProject(projectName="P6",  maxParticipants= 8, minELM=2, minMBM=2, minWIM=2)
solver.addProject(projectName="P7",  maxParticipants= 8, minELM=2, minMBM=2, minWIM=2)
solver.addProject(projectName="P8",  maxParticipants= 8, minELM=2, minMBM=2, minWIM=2)
#######################


#create random students with random preferences for testing
#######################
disciplines = [Solver.ELM, Solver.MBM, Solver.WIM]
projectlist = solver.getProjects().keys()
projectlist = [*projectlist] #convert from set to list (to use it in random.sample)
for i in range(0, 96):
    choices = random.sample(projectlist, k=3)
    solver.addStudent(f"Student {i}", random.choice(disciplines), choices[0], choices[1], choices[2])
#######################

#solve the allocation problem
success = solver.solve()


if not success:
    #not possible to find a solution!
    sys.exit(1)


#analyze and print the found solution
#####################################
allocation = solver.getAllocation()
students = solver.getStudents()

#print solution
for p in allocation:
    print(f"Project {p}:")
    for s in allocation[p]:
        print(f"\t{students[s]}")

#successrate: number of 1st, 2nd, 3rd, 4th choices realized:
numRealized = [0, 0, 0, 0]
for p in allocation:
    for s in allocation[p]:
        numRealized[0] += 1 if students[s][1] == p else 0
        numRealized[1] += 1 if students[s][2] == p else 0
        numRealized[2] += 1 if students[s][3] == p else 0
numRealized[3] = len(students) - numRealized[0] - numRealized[1] - numRealized[2]

print("##################################")
print("#### Fullfillment of choices: ####")
print(f"Rate of fulfilled 1st choice: {numRealized[0]/len(students)*100.0}")
print(f"Rate of fulfilled 2nd choice: {numRealized[1]/len(students)*100.0}")
print(f"Rate of fulfilled 3rd choice: {numRealized[2]/len(students)*100.0}")
print(f"Rate of fulfilled 4th choice: {numRealized[3]/len(students)*100.0}")

fig, ax = plt.subplots()
ax.bar("1st Choices", numRealized[0]/len(students)*100.0, 0.35)
ax.bar("2nd Choices", numRealized[1]/len(students)*100.0, 0.35)
ax.bar("3rd Choices", numRealized[2]/len(students)*100.0, 0.35)
ax.bar("No Choices", numRealized[3]/len(students)*100.0, 0.35)

ax.set_ylabel('Percent of Participants')
ax.set_title('Granted Choices')

plt.show()


#mixing of student's diciplines in projects:
mix = dict()
for p in allocation:
    mix[p] = {Solver.ELM : 0, Solver.MBM: 0, Solver.WIM: 0}
    for s in allocation[p]:
        mix[p][ students[s][0] ] += 1


#plot mixing
elms = []
mbms = []
wims = []
for p in mix:
    elms.append(mix[p][Solver.ELM])
    mbms.append(mix[p][Solver.MBM])
    wims.append(mix[p][Solver.WIM])

fig, ax = plt.subplots()
ax.bar(allocation.keys(), elms, 0.35, label='ELM')
ax.bar(allocation.keys(), mbms, 0.35, label='MBM', bottom=elms)
ax.bar(allocation.keys(), wims, 0.35, label='WIM', bottom=[sum(x) for x in zip(mbms, elms)])

ax.set_ylabel('Participants')
ax.set_title('Project Allocations by Disciplines')
ax.legend()

plt.show()