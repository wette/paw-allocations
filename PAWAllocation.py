#!/usr/bin/python3

import random
import matplotlib.pyplot as plt
from solver import Solver
from ILPSolver import ILPSolver
from MontecarloSolver import MontecarloSolver
from IliasInterface import IliasInterface
import sys


#which solver to use?
solver = ILPSolver()
#solver = MontecarloSolver()

inputFile = "/Users/wette/Documents/FHBielefeld/tools/pawZuordnung/1667482745__complete_2022-11-03_14-39.xlsx"

ilias = IliasInterface()
ilias.readProjects(inputFile, "Projekte")
ilias.readStudents(inputFile, "Wahlverfahren PAW")

print(f"Read {len(ilias.students)} Students and {len(ilias.projects)} Projects from Excel.")

#Available projects:
for project in ilias.projects:
    solver.addProject(projectName=project[0], maxParticipants=project[1], minELM=project[2], minMBM=project[3], minWIM=project[4])

#Available students:
for student in ilias.students:
    solver.addStudent(student[0], student[1], student[2], student[3], student[4], student[5], student[6])


#solve the allocation problem
success = solver.solve()


if not success:
    #not possible to find a solution!
    sys.exit(1)


ilias.writeAllocation(inputFile, "Allocation", solver)

#analyze and print the found solution
#####################################
allocation = solver.getAllocation()
students = solver.getStudents()

#print solution
for p in allocation:
    print(f"Project {p}:")
    for s in allocation[p]:
        print(f"\t{students[s][0]} {[name[0:5] for name in  students[s][1:4]]}")

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
ax.bar("No Choices",  numRealized[3]/len(students)*100.0, 0.35)

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
shortNames = [name[0:5] for name in allocation.keys()]
ax.bar(shortNames, elms, 0.35, label='ELM')
ax.bar(shortNames, mbms, 0.35, label='MBM', bottom=elms)
ax.bar(shortNames, wims, 0.35, label='WIM', bottom=[sum(x) for x in zip(mbms, elms)])

ax.set_ylabel('Participants')
ax.set_title('Project Allocations by Disciplines')
ax.legend()

plt.show()