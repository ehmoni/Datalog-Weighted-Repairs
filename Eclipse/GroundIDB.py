RuleRecord = {}
RuleRecord["G_01"] = "(admDrugT(Date, PrescribedBy, Drug, Patient, Age) & personSpec(PrescribedBy, Specialist) & drugType(Drug, DrType)"

def GroundIDB(di):
    ditk = di[-6:-2]
    print(ditk)
    body = RuleRecord[ditk]
    
    return 0




# def GroundIDB(di):
#     ditk = di[di.find("G_"):di.find("G_")+4]
#     dit = di[-6:-2]
#     print(di.find("G_"))
#     print(dit)
#     body = RuleRecord[ditk]
#     print(body)
    
    0
    








s1 = """+bills("14-Keb-18", "Pediatrician", "Restricted", "G_23", 50)"""
s2 = """-bills("28-Mar-18", "Cardiologist", "GeneralSale", val, "G_01")"""
s = [s1,s2]

GroundIDB(s2)

