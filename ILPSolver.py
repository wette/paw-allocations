from solver import Solver
import gurobipy as gp
from gurobipy import GRB
import sys

class ILPSolver(Solver):
    def check_for_correct_input(self):
        #check if all students voted for unique projects
        students, _, choiceA, choiceB, choiceC, _, _ = gp.multidict(self.students)
        for s in students:
            if choiceA[s] == choiceB[s] or \
               choiceA[s] == choiceC[s] or \
               choiceB[s] == choiceC[s]:
                raise Exception(f"Student {s} did NOT select 3 distinct PAWs!")


    def solve(self):
        self.check_for_correct_input()
        
        projects, maxParticipants,  minELM, minMBM, minWIM = gp.multidict(self.projects)
        students, discipline, choiceA, choiceB, choiceC, _, _ = gp.multidict(self.students)

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
            choiceWeights[s][choiceC[s]] = 1000

            for p in self.projects.keys():
                if p not in choiceWeights[s].keys():
                    #add p as non-preferred project to the student:
                    mapping.append( (s, p) )
                    choiceWeights[s][p] = 1000000

            #add students discipline to the vectors:
            ELMstudents[s] = 1 if discipline[s] == Solver.ELM else 0
            MBMstudents[s] = 1 if discipline[s] == Solver.MBM else 0
            WIMstudents[s] = 1 if discipline[s] == Solver.WIM else 0

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
            self.allocation = None
            return False
        if status == GRB.INFEASIBLE:
            print('The model cannot be solved because it is too contraint')
            self.allocation = None
            return False
        if status == GRB.OPTIMAL:
            print('The optimal objective is %g' % model.ObjVal)
        if status != GRB.UNBOUNDED and status != GRB.OPTIMAL and status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
            print('Optimization was stopped with status %d' % status)
            self.allocation = None
            return False

        #create solution:
        self.allocation = dict()
        for p in projects:
            self.allocation[p] = []
            for s in students:
                if (s,p) in m:
                    if m[s, p].X > 0.0001:
                        self.allocation[p].append(s)

        return True
