from solver import Solver

class MontecarloSolver(Solver):
    def solve(self):
        #create solution:
        self.allocation = dict()

        #init empty project allocations
        for p in self.projects.keys():
                self.allocation[p] = []

        allocatedStudents = [] #bookkeeping to check if a student is already allocated

        #first, grant as many 1st choices, then as many 2nd choices, then 3rd. 
        for choice in [1,2,3]:  #1st, 2nd, 3rd choice of the students
            for project in self.projects.keys():
                for s in self.students.keys():
                    if s not in allocatedStudents and \
                       self.students[s][choice] == project and \
                       len(self.allocation[project]) < self.projects[project][0]:
                        self.allocation[project].append(s)
                        allocatedStudents.append(s)

        #if there are remaining, non-allocated students: allocated them to non-full projects:
        for project in self.projects.keys():
            for s in self.students.keys():
                if s not in allocatedStudents and \
                    len(self.allocation[project]) < self.projects[project][0]:
                    self.allocation[project].append(s)
                    allocatedStudents.append(s)

        return True
