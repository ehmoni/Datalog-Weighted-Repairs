from pyDatalog import pyDatalog as pd

#>> Terms of Dimension
#Person
pd.create_terms("person, specialty, contract, division, all_persons") 
pd.create_terms("personSpec, personContract, specDiv")

#Drug
pd.create_terms("drug, drtype, all_drugs")
pd.create_terms("drugType")

#>> Terms for Facts
pd.create_terms("admDrug, bills")

#>> Reading Dimension and Facts
dim = open("Dimension.txt", 'r').read()
pd.load(dim)
facts = open("Facts.txt", 'r').read()
print(facts)
pd.load(facts)

print()
print(facts)



pd.create_terms("A,B,C,D,E,F,G")

s1 = """+bills("14-Keb-18", "Pediatrician", "Restricted", "Ruby", 50)"""
s2 = """-bills("28-Mar-18", "Cardiologist", "GeneralSale", "Rafi", 200)"""
s = [s1,s2]

print(s1)

pd.load(s)

pd.create_terms("xyz, pqr, stu")



ss = """-bills("28-Mar-18", "Cardiologist", "GeneralSale", "Rafi", 200)"""
    


print(bills(A,B,C,D,E))
