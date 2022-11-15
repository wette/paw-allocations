import pandas as pd


class IliasInterface:
    def __init__(self):
        self.students = []
        self.projects = []
    def readStudents(self, filename, sheet):
        df = pd.read_excel(io=filename, sheet_name=sheet)
        for i in range(0, df.shape[0]):
            name = df.iat[i, 0].strip()
            vorname = df.iat[i, 1].strip()
            matNr = str(df.iat[i, 2])
            studiengang = df.iat[i, 3].strip()
            choice1 = df.iat[i, 4].strip()
            choice2 = df.iat[i, 5].strip()
            choice3 = df.iat[i, 6].strip()

            self.students.append([matNr, studiengang, choice1, choice2, choice3, name, vorname])

    def readProjects(self, filename, sheet):
        df = pd.read_excel(io=filename, sheet_name=sheet)
        for i in range(0, df.shape[0]):
            projectName = df.iat[i, 0].strip()
            maxParticipants = int(df.iat[i, 1])
            minELM = int(df.iat[i, 2])
            minMBM = int(df.iat[i, 3])
            minWIM = int(df.iat[i, 4])

            self.projects.append([projectName, maxParticipants, minELM, minMBM, minWIM])

    def writeAllocation(self, filename, sheet, solver):
        allocation = solver.getAllocation()
        students = solver.getStudents()

        data = {        "Matrikelnummer": list(), 
                        "Name": list(), 
                        "Vorname": list(), 
                        "Projekt": list()
                }
        for p in allocation.keys():
            for mnr in allocation[p]:
                data["Matrikelnummer"].append(mnr)
                data["Name"].append(students[mnr][4])
                data["Vorname"].append(students[mnr][5])
                data["Projekt"].append(p)

        df = pd.DataFrame(data=data)
        writer = pd.ExcelWriter(filename, mode="a", if_sheet_exists="replace")
        df.to_excel(writer, sheet_name=sheet, index=False)
        writer.close()
