from faker import Faker
import random
import numpy as np

n = 100

names = list()

docs = ["Cardiologist", "Pediatrician", "Medicine", "Gynecologist", "Surgeon", "Dermatologist", "Neurologist"]
nurses = ["Clinical", "Forensic", "Orthopedic"]
oldnames = ["Emdad","Tina", "Tom", "David", "Ali"]
contract = ["FullTime", "FullTime", "FullTime", "Intern"]
special = docs + nurses

resdrugs = ["Santonin", "Meclozine", "Ketamine"]
gsdrugs = ["Ibuprofen", "Plasmin", "Carprofen", "Histamine", "Lipitor", "Nexium", "Plavix", "Abilify", "Seroquel", "Singulair", "Crestor", "Actos", "Epogen"]


fake = Faker()

s = ""

for _ in range(n):
    fn = fake.first_name()
    while(fn in names):
        fn = fake.first_name()
    names.append(fn)

#print(sorted(names))

# print(docs)
# print(nurses)
# print(names)
# print(resdrugs)
# print(gsdrugs)

dimension =	{
    "Emdad": """Cardiologist""",
    "Tina": """Cardiologist""",
    "Tom": """Pediatrician""",
    "David": """Clinical""",
    "Ali": """Clinical""",
}

dimcon = {
    "Emdad": "FullTime",
    "Tina": "FullTime",
    "Tom": "Intern",
    "David": "Intern",
    "Ali": "Intern",
}

f = open("DimensionGen.txt", "w+")

for i in docs:
    dimension[i] = "Doctor"
    s = "+specDiv(\"" + str(i) + "\"" + ", " + "\"Doctor\"" + ")\n"
    f.write(s)
f.write("\n")

for i in nurses:
    dimension[i] = "Nurse"
    s = "+specDiv(\"" + str(i) + "\"" + ", " + "\"Nurse\"" + ")\n"
    f.write(s)
f.write("\n")

for i in resdrugs:
    dimension[i] = "Restricted"
    s = "+drugType(\"" + str(i) + "\"" + ", " + "\"Restricted\"" + ")\n"
    f.write(s)
f.write("\n")

for i in gsdrugs:
    dimension[i] = "GeneralSale"
    s = "+drugType(\"" + str(i) + "\"" + ", " + "\"GeneralSale\"" + ")\n"
    f.write(s)
f.write("\n")

#print(dimension)

for i in oldnames:
    s = "+personSpec(\"" + str(i) + "\"" + ", \"" + dimension[i] + "\")\n"
    f.write(s)
f.write("\n")


for i in oldnames:
    s = "+personContract(\"" + str(i) + "\"" + ", \"" + dimcon[i] + "\")\n"
    f.write(s)
f.write("\n")


for i in names:
    s = "+personSpec(\"" + str(i) + "\"" + ", \"" + random.choice(special) + "\")\n"
    f.write(s)
f.write("\n")

for i in names:
    s = "+personContract(\"" + str(i) + "\"" + ", \"" + random.choice(contract) + "\")\n"
    f.write(s)
f.write("\n")

Mat = np.random.randint(0, 15, (500, 6))
print(Mat)