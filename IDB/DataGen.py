from faker import Faker
import random
import numpy as np

n = 100

names = list()

docs = ["Cardiologist", "Pediatrician", "Medicine", "Gynecologist", "Surgeon", "Dermatologist", "Neurologist"]
nurses = ["Clinical", "Forensic", "Orthopedic"]
oldnames = ["Emdad","Trina", "Tomu", "Davix", "Alim"]
contract = ["FullTime", "FullTime", "FullTime", "Intern"]
special = docs + nurses

resdrugs = ["Santonin", "Meclozine", "Ketamine"]
gsdrugs = ["Ibuprofen", "Plasmin", "Carprofen", "Histamine", "Lipitor", "Nexium", "Plavix", "Abilify", "Seroquel", "Singulair", "Crestor", "Actos", "Epogen"]
alldrugs = resdrugs + gsdrugs
random.shuffle(alldrugs)

fake = Faker()

s = ""

for _ in range(n):
    fn = fake.first_name()
    while(fn in names):
        fn = fake.first_name()
    names.append(fn)

allnames = oldnames + names
random.shuffle(allnames)
#print(sorted(names))

# print(docs)
# print(nurses)
# print(names)
# print(resdrugs)
# print(gsdrugs)

dimension =	{
    "Emdad": """Cardiologist""",
    "Trina": """Cardiologist""",
    "Tomu": """Pediatrician""",
    "Davix": """Clinical""",
    "Alim": """Clinical""",
}

dimcon = {
    "Emdad": "FullTime",
    "Trina": "FullTime",
    "Tomu": "Intern",
    "Davix": "Intern",
    "Alim": "Intern",
}

f = open("DimensionGen.txt", "w+")
ff = open("FactGen.txt", "w+")

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



for i in oldnames:
    s = "+personSpec(\"" + str(i) + "\"" + ", \"" + dimension[i] + "\")\n"
    f.write(s)
f.write("\n")


for i in oldnames:
    s = "+personContract(\"" + str(i) + "\"" + ", \"" + dimcon[i] + "\")\n"
    f.write(s)
f.write("\n")


for i in names:
    dimension[str(i)] = random.choice(special)
    #s = "+personSpec(\"" + str(i) + "\"" + ", \"" + random.choice(special) + "\")\n"
    s = "+personSpec(\"" + str(i) + "\"" + ", \"" + dimension[str(i)] + "\")\n"
    f.write(s)
f.write("\n")

for i in names:
    s = "+personContract(\"" + str(i) + "\"" + ", \"" + random.choice(contract) + "\")\n"
    f.write(s)
f.write("\n")


print(dimension)
#Mat = np.random.randint(0, 15, (500, 6))
#print(Mat)

N = 1500
pnames = []
dates = []
ages = []
tk = []
spnms = []
spspc = []
drg = []
drgrp = []

for i in range(N):
    pnames.append("Name" + str(i))
    dt = fake.date_time_between(start_date='-2y', end_date='now')
    dates.append(dt.strftime('%b-%d-%Y'))
    ages.append(random.randint(5,100))
    tk.append(random.randint(2,150))
    nm = random.choice(allnames)
    spnms.append(nm)
    spspc.append(dimension[nm])
    d = random.choice(alldrugs)
    drg.append(d)
    drgrp.append(dimension[d])


# print(pnames)
# print(dates)
# print(ages)
# print(tk)
# print(spnms)
# print(spspc)

#+admDrug("28-Mar-18", "Emdad", "Ibuprofen", "Rafi", 80)
for i in range(N):
    s = "+admDrug(\"" + dates[i] + "\"" + ", \"" + spnms[i] + "\"" + ", \"" + drg[i] + "\"" + ", \"" + pnames[i] + "\"" + ", " + str(ages[i]) + ")"+ "\n"
    ff.write(s)
print(s)
ff.write('\n')
#+bills("28-Mar-18", "Cardiologist", "GeneralSale", "Rafi", 200)
for i in range(N):
    s = "+bills(\"" + dates[i] + "\"" + ", \"" + spspc[i] + "\"" + ", \"" + drgrp[i] + "\"" + ", \"" + pnames[i] + "\"" + ", " + str(tk[i]) + ")"+ "\n"
    ff.write(s)
print(s)

f.close()
ff.close()
