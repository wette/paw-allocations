class Solver:
    ELM = "ELM"
    MBM = "MBM"
    WIM = "WIM"

    def __init__(self):
        self.students = {}
        self.projects = {}
        self.allocation = {}

    def addStudent(self, matNr, discipline, choiceA, choiceB, choiceC, lastname, name ):
        self.students[matNr] = [discipline, choiceA, choiceB, choiceC, lastname, name]

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

