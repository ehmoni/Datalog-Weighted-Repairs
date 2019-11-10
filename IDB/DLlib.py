from pyDatalog import pyDatalog as pd
import random

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

def load_dim():
    #dim = open("Dimension.txt", 'r').read()
    dim = open("DimensionGen.txt", 'r').read()
    pd.load(dim)

def load_facts():
    #facts = open("Facts.txt", 'r').read()
    facts = open("FactGen.txt", 'r').read()
    pd.load(facts)


#>>Rule

pd.create_terms("Date, Specialist, DrType, Patient, Amount, PrescribedBy, Drug, Age")
pd.create_terms("Gen, billsT, admDrug1, admDrugT")

def run_rule():
    admDrug1(Date, PrescribedBy, Drug, Patient) <= bills(Date, Specialist, DrType, Patient, Amount) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)

    admDrugT(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & ~(admDrug1(Date, PrescribedBy, Drug, Patient))

    #>> Generation (Rule ID: G_01)
    billsT(Date, Specialist, DrType, Patient, "G_01", Gen) <= (admDrugT(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType) & (Gen=="G_01"))

    billsT(Date, Specialist, DrType, Patient, Amount, Gen) <= bills(Date, Specialist, DrType, Patient, Amount) & (Gen==0)

   # bills(Date, Specialist, DrType, Patient, Amount) <= billsT(Date, Specialist, DrType, Patient, Amount)
    IDB = billsT(Date, Specialist, DrType, Patient, Amount, Gen)
    return IDB

#>> RuleRecord (Dictionary)

RuleRecordBody = {}
RuleRecordBody["G_01"] = "admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)"

#>>

#>> Constraint

pd.create_terms("Con, NotCon")
pd.create_terms("Division, Contract")

def neg_con(IDB):

    # NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & drugType(Drug, DrType) & personSpec(PrescribedBy, Specialist) & specDiv(Specialist, Division) & personContract(PrescribedBy, Contract) & (DrType=="Restricted") & (Division!="Doctor")
    # NotCon(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division, Contract) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & drugType(Drug, DrType) & personSpec(PrescribedBy, Specialist) & specDiv(Specialist, Division) & personContract(PrescribedBy, Contract) & (DrType=="Restricted") & (Contract!="FullTime")

    # NotCon1(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & drugType(Drug, DrType) & personSpec(PrescribedBy, Specialist) & specDiv(Specialist, Division) & (DrType=="Restricted") & (Division!="Doctor")
    # NotCon2(Date, PrescribedBy, Drug, Patient, Age, DrType, Contract) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & drugType(Drug, DrType) & personContract(PrescribedBy, Contract) & (DrType == "Restricted") & (Contract != "FullTime")

    #NotCon(Date, Specialist, DrType, Patient, Amount, Division, Gen) <= billsT(Date, Specialist, DrType, Patient, Amount, Gen) & specDiv(Specialist, Division) & (DrType=="Restricted") & (Division!="Doctor")
    NotCon(Date, Specialist, DrType, Patient, Amount, Division, Gen) <= IDB & specDiv(Specialist, Division) & (DrType=="Restricted") & (Division!="Doctor")

    NC = NotCon(Date, Specialist, DrType, Patient, Amount, Division, Gen)

    # NC1 = NotCon1(Date, PrescribedBy, Drug, Patient, Age, DrType, Specialist, Division)
    # NC2 = NotCon2(Date, PrescribedBy, Drug, Patient, Age, DrType, Contract)

    # NC = (NC1, NC2)

    return NC


#>> Source of Inconsistency

pd.create_terms("billsI, billsI2, IDBIC, admDrugI, personSpecI, drugTypeI, specDivI, personContractI")

def incon(NC, IDB):
    inconD = dict()

    nc = NC

    #billsI(Date, Specialist, DrType, Patient, Amount, Gen) <= billsT(Date, Specialist, DrType, Patient, Amount, Gen) & nc
    billsI(Date, Specialist, DrType, Patient, Amount, Gen) <= IDB & nc
    billsI2(Date, Specialist, DrType, Patient, Amount) <= billsI(Date, Specialist, DrType, Patient, Amount, Gen)

    #print("Just Printed")
    #print(billsI(Date, Specialist, DrType, Patient, Amount, Gen))

    if(billsI(Date, Specialist, DrType, Patient, Amount, Gen) & (Gen=="G_01")):
        #print("Got GEN")
        rl = admDrug(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)
        blsi = billsI(Date, Specialist, DrType, Patient, Amount, Gen)
        admDrugI(Date, PrescribedBy, Drug, Patient, Age) <=  blsi & rl
        personSpecI(PrescribedBy, Specialist) <= blsi & rl
        drugTypeI(Drug, DrType) <= blsi & rl

        inconD["admDrug"] = admDrugI(Date, PrescribedBy, Drug, Patient, Age)
        inconD["personSpec"] = personSpecI(PrescribedBy, Specialist)
        inconD["drugType"] = drugTypeI(Drug, DrType)

    #admDrugI(Date, PrescribedBy, Drug, Patient, Age) <= admDrug(Date, PrescribedBy, Drug, Patient, Age) & nc
    #personSpecI(PrescribedBy, Specialist) <= personSpec(PrescribedBy, Specialist) & nc
    specDivI(Specialist, Division) <= specDiv(Specialist, Division) & nc
    #personContractI(PrescribedBy, Contract) <= personContract(PrescribedBy, Contract) & nc
    #drugTypeI(Drug, DrType) <= drugType(Drug, DrType) & nc

    inconD["bills"] = billsI2(Date, Specialist, DrType, Patient, Amount)
    #inconD["admDrug"] = admDrugI(Date, PrescribedBy, Drug, Patient, Age)
    #inconD["personSpec"] = personSpecI(PrescribedBy, Specialist)
    inconD["specDiv"] = specDivI(Specialist, Division)
    #inconD["personContract"] = personContractI(PrescribedBy, Contract)
    #inconD["drugType"] = drugTypeI(Drug, DrType)

    return inconD


#>> Inconsistent atom List

def inconlist(inconD):
    inconL = list()
    t = 1

    for key, value in inconD.items():
        for i in range(0, len(value)):
            inconL.append((t, key+str(value[i])))
            t += 1

    return inconL



#>> Generate Weights

def genweight(inconL):

    slwt = list()

    for i in range(1, len(inconL) + 1):
        slwt.append((i, random.randint(1, 300)))

    slwt.sort(key=lambda tup: tup[1])

    return slwt


#>> Fix Order of the Weights

def fixWtorder(inconL, slwt):
    inconLT = list()
    slwtT = list()
    for i in range(1, len(inconL) + 1):
        inconLT.append((i, inconL[slwt[i - 1][0] - 1][1]))
        slwtT.append((i, slwt[i - 1][1]))

    return [(0, "")] + inconLT, [(0, 0)] + slwtT


#>> Check minimum weight which satisfies the constraint
#
# def checkmin(Lst, inconL):
#     L = Lst[1:]
#     nAtoms = [('-' + inconL[i][1]) for i in L]
#     print(nAtoms)
#     pd.load(nAtoms)
#     nc = neg_con()
#     print(nc)
#     if not nc:
#         return 1
#     icd = incon(nc)
#     for v in icd.values():
#         if v:
#             print(v)
#             pAtoms = [('+' + inconL[i][1]) for i in L]
#             pd.load(pAtoms)
#             return 0
#     return 1
