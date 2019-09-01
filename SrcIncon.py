from DLlib import *
#>> Identify Inconsistency

# print("NotCondition: ")
# print(NotCon1(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division))
# print("==========================================================================")
# print(NotCon2(Date, PrescribedBy, Drug, Patient, Age, DrType, Contract))

#print(NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract))
#print(NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract))
#print(NC)
print("=================================START=========================================")

pd.create_terms("billsI, IDBIC, admDrugI, personSpecI, drugTypeI, specDivI, personContractI")



def incon(NC):
    inconD = dict()
    # admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & NC
    # personSpecI(PrescribedBy, Specialist) <= personSpec(PrescribedBy, Specialist) & NC
    # specDivI(Specialist, Division) <= specDiv(Specialist, Division) & NC
    # personContractI(PrescribedBy, Contract) <= personContract(PrescribedBy, Contract) & NC
    # drugTypeI(Drug, DrType) <= drugType(Drug, DrType) & NC

    keysL = ["admDrug", "personSpec", "specDiv", "personContract", "drugType"]

    inconD.fromkeys(keysL)

    inconD["admDrug"] = admDrug(Date, PrescribedBy, Drug, Patient, Age) & NC
    inconD["personSpec"] = personSpec(PrescribedBy, Specialist) & NC
    inconD["specDiv"] = specDiv(Specialist, Division) & NC
    inconD["personContract"] = personContract(PrescribedBy, Contract) & NC
    inconD["drugType"] = drugType(Drug, DrType) & NC

    print(inconD.items())

    return inconD

# admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & NC1
# drugTypeI(Drug, DrType) <= drugTypeI(Drug, DrType) & NC1
# personSpecI(PrescribedBy, Specialist) <= personSpec(PrescribedBy, Specialist) & NC1
# specDivI(Specialist, Division) <= specDiv(Specialist, Division) & NC1
# personContractI(PrescribedBy, Contract) <= personContract(PrescribedBy, Contract) & NC1
#
# # admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & NC2
# # drugTypeI(Drug, DrType) <= drugTypeI(Drug, DrType) & NC2
# # personSpecI(PrescribedBy, Specialist) <= personSpec(PrescribedBy, Specialist) & NC2
# # specDivI(Specialist, Division) <= specDiv(Specialist, Division) & NC2
# # personContractI(PrescribedBy, Contract) <= personContract(PrescribedBy, Contract) & NC2

# admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
# drugTypeI(Drug, DrType) <= drugTypeI(Drug, DrType) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
# personSpecI(PrescribedBy, Specialist) <= personSpec(PrescribedBy, Specialist) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
# specDivI(Specialist, Division) <= specDiv(Specialist, Division) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
# personContractI(PrescribedBy, Contract) <= personContract(PrescribedBy, Contract) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)



#>> Grounding IDB

#billsI(Date, Specialist, DrType, Patient, Amount, Gen) <= billsT(Date, Specialist, DrType, Patient, Amount, Gen) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)
#billsI(Date, Specialist, DrType, Patient, Amount, Gen) <= billsT(Date, Specialist, DrType, Patient, Amount, Gen) & NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract)

# billsI(Date, Specialist, DrType, Patient, Amount, Gen) <= billsT(Date, Specialist, DrType, Patient, Amount, Gen) & NC1
# billsI(Date, Specialist, DrType, Patient, Amount, Gen) <= billsT(Date, Specialist, DrType, Patient, Amount, Gen) & NC2

# admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= billsI(Date, Specialist, DrType, Patient, Amount, Gen) & admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)
# personSpecI(PrescribedBy, Specialist) <= billsI(Date, Specialist, DrType, Patient, Amount, Gen) & admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)
# drugTypeI(Drug, DrType) <= billsI(Date, Specialist, DrType, Patient, Amount, Gen) & admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)

print()
#print(billsI(Date, Specialist, DrType, Patient, Amount, Gen))
print("==========================================================================")
print()
print(admDrugI(Date, PrescribedBy, Drug, Patient, Age))
print("==========================================================================")
print()
print(personSpecI(PrescribedBy, Specialist))
print("==========================================================================")
print()
print(specDivI(Specialist, Division))
print("==========================================================================")
print()
print(personContractI(PrescribedBy, Contract))
print("==========================================================================")
print()
print(drugTypeI(Drug, DrType))
print("==============================DATA============================================")
#print(str(drugTypeI(Drug, DrType))[0:50])

print(drugTypeI(Drug, DrType).data[0])
print(personContractI(PrescribedBy, Contract).data)

#>> Checking Condition

pd.create_terms("ConI")

ConI(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract) <= admDrugI(Date, PrescribedBy, Drug, Patient, Age) & drugTypeI(Drug, DrType) & personSpecI(PrescribedBy, Specialist) & specDivI(Specialist, Division) & personContractI(PrescribedBy, Contract) & (DrType=="Restricted") & (Division=="Doctor")


#print(ConI(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract))






