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
pd.load(facts)

print(facts)
print("==========================================================================")

#>>Rule
pd.create_terms("Date, Specialist, DrType, Patient, Amount, Age, Drug, PrescribedBy, Gen, billsT, admDrug1, admDrugT")

admDrug1(Date, PrescribedBy, Drug, Patient) <= bills(Date, Specialist, DrType, Patient, Amount) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)

admDrugT(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & ~(admDrug1(Date, PrescribedBy, Drug, Patient))

#>> Generation (Rule ID: G_01)
billsT(Date, Specialist, DrType, Patient, "G_01", Gen) <= (admDrugT(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType) & (Gen=="G_01"))

billsT(Date, Specialist, DrType, Patient, Amount, Gen) <= bills(Date, Specialist, DrType, Patient, Amount) & (Gen==0)

print(billsT(Date, Specialist, DrType, Patient, Amount, Gen))

#>>RuleRecord (Dictionary)
RuleRecord = {}
RuleRecord["G_01"] = "(admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)"

#>> Constraint

pd.create_terms("Con, NotCon")
pd.create_terms("Division, Contract")

Con(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & drugType(Drug, DrType) & personSpec(PrescribedBy, Specialist) & specDiv(Specialist, Division) & personContract(PrescribedBy, Contract) & (DrType=="Restricted") & (Division=="Doctor")
NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & drugType(Drug, DrType) & personSpec(PrescribedBy, Specialist) & specDiv(Specialist, Division) & personContract(PrescribedBy, Contract) & (DrType=="Restricted") & (Division!="Doctor")
NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & drugType(Drug, DrType) & personSpec(PrescribedBy, Specialist) & specDiv(Specialist, Division) & personContract(PrescribedBy, Contract) & (DrType=="Restricted") & (Contract!="FullTime")

#print(NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract))

#>> Identify Inconsistency

pd.create_terms("billsI, IDBIC, admDrugI, personSpecI, drugTypeI, specDivI, personContractI")

admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
drugTypeI(Drug, DrType) <= drugTypeI(Drug, DrType) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
personSpecI(PrescribedBy, Specialist) <= personSpec(PrescribedBy, Specialist) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
specDivI(Specialist, Division) <= specDiv(Specialist, Division) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
personContractI(PrescribedBy, Contract) <= personContract(PrescribedBy, Contract) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)

#>> Grounding IDB

billsI(Date, Specialist, DrType, Patient, Amount, Gen) <= billsT(Date, Specialist, DrType, Patient, Amount, Gen) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)

admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= billsI(Date, Specialist, DrType, Patient, Amount, Gen) & admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)
personSpecI(PrescribedBy, Specialist) <= billsI(Date, Specialist, DrType, Patient, Amount, Gen) & admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)
drugTypeI(Drug, DrType) <= billsI(Date, Specialist, DrType, Patient, Amount, Gen) & admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)

print()
print(billsI(Date, Specialist, DrType, Patient, Amount, Gen))
print()
print(admDrugI(Date, PrescribedBy, Drug, Patient, Age))
print()
print(personSpecI(PrescribedBy, Specialist))
print()
print(specDivI(Specialist, Division))
print()
print(personContractI(PrescribedBy, Contract))
print()
print(drugTypeI(Drug, DrType))
print(str(drugTypeI(Drug, DrType)))


#>> Checking Condition

pd.create_terms("ConI")

ConI(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract) <= admDrugI(Date, PrescribedBy, Drug, Patient, Age) & drugTypeI(Drug, DrType) & personSpecI(PrescribedBy, Specialist) & specDivI(Specialist, Division) & personContractI(PrescribedBy, Contract) & (DrType=="Restricted") & (Division=="Doctor")


print(ConI(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract))






