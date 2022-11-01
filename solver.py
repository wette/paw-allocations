class Solver:
    ELM = "ELM"
    MBM = "MBM"
    WIM = "WIM"

    def __init__(self):
        self.students = {}
        self.projects = {}
        self.allocation = {}

    def addStudent(self, studentName, discipline, choiceA, choiceB, choiceC):
        self.students[studentName] = [discipline, choiceA, choiceB, choiceC]

    def addProject(self, projectName, maxParticipants,  minELM, minMBM, minWIM):
        self.projects[projectName] = [maxParticipants,  minELM, minMBM, minWIM]

    def getAllocation(self):
        return self.allocation

    def getProjects(self):
        return self.projects

    def getStudents(self):
        return self.students

    def solve(self):
        pass

