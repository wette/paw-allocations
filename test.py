#!/usr/bin/python3

import gurobipy as gp
from gurobipy import GRB
import sys
import random

ELM = "ELM"
MBM = "MBM"
WIM = "WIM"


#inputs: Projekte, Plätze, min. ELM, min. MBM, minWIM
projects, maxParticipants,  minELM, minMBM, minWIM = gp.multidict({
    "1": [16,               2,      1,      0],
    "2": [8,                0,      0,      0],
    "3": [8,                0,      0,      0],
    "4": [16,               1,      0,      1]
})

#inputs: Studenten, Fachrichtung, 1. Wahl, 2. Wahl, 3. Wahl
students, discipline, choiceA, choiceB, choiceC = gp.multidict({
    '1234567': [ELM, "1", "2", "3"],
    '1234568': [MBM, "2", "3", "1"],
    '1234569': [ELM, "4", "3", "1"],
    '1234560': [WIM, "1", "4", "3"],
    '1234561': [ELM, "3", "2", "4"]
})



model = gp.Model("mapping")

ELMstudents = {}
MBMstudents = {}
WIMstudents = {}
mapping = []
choiceWeights = {}
for s in students:
    mapping.append( (s, choiceA[s]) )
    mapping.append( (s, choiceB[s]) )
    mapping.append( (s, choiceC[s]) )

    choiceWeights[s] = dict()
    choiceWeights[s][choiceA[s]] = 1
    choiceWeights[s][choiceB[s]] = 100
    choiceWeights[s][choiceC[s]] = 10000

    ELMstudents[s] = 1 if discipline[s] == ELM else 0
    MBMstudents[s] = 1 if discipline[s] == MBM else 0
    WIMstudents[s] = 1 if discipline[s] == WIM else 0

#create decision variables:
m = model.addVars(mapping, name="mapping")

#each student has to be assigned to exactly one project:
req1 = model.addConstrs((m.sum(s, '*') == 1
                      for s in students), "_")

#no project must exceed its limit of students
req2 = model.addConstrs((m.sum('*', p) <= maxParticipants[p]
                      for p in projects), "_")

#jedes Projekt muss Mindestanzahl an ELM besitzen
for p in projects:
    terms = []
    for s in students:
        if (s,p) in m:
            terms.append(ELMstudents[s] * m[s, p])
    model.addRange(sum(terms), minELM[p], maxParticipants[p], p)


#jedes Projekt muss Mindestanzahl an MBM besitzen
for p in projects:
    terms = []
    for s in students:
        if (s,p) in m:
            terms.append(MBMstudents[s] * m[s, p])
    model.addRange(sum(terms), minMBM[p], maxParticipants[p], p)


#jedes Projekt muss Mindestanzahl an WIM besitzen
for p in projects:
    terms = []
    for s in students:
        if (s,p) in m:
            terms.append(WIMstudents[s] * m[s, p])
    model.addRange(sum(terms), minWIM[p], maxParticipants[p], p)

#objective function
model.setObjective(gp.quicksum(choiceWeights[s][p] * m[s, p] for s, p in mapping), GRB.MINIMIZE)

model.optimize()

status = model.Status
if status == GRB.UNBOUNDED:
    print('The model cannot be solved because it is unbounded')
    sys.exit(0)
if status == GRB.OPTIMAL:
    print('The optimal objective is %g' % model.ObjVal)
if status != GRB.UNBOUNDED and status != GRB.OPTIMAL and status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
    print('Optimization was stopped with status %d' % status)
    sys.exit(0)

#print solution:
for p in projects:
    print(f"Project team {p}:")
    for s in students:
        if (s,p) in m:
            if m[s, p].X > 0.0001:
                print(f"\t{s}")

