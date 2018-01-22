import csv
import pandas as pd
import numpy as np
import os

actiondt_filename=os.path.join('nyc_inspection_data','Action.txt')
#Fields: "STARTDATE","ENDDATE","ACTIONCODE","ACTIONDESC"
cuisinedt_filename=os.path.join('nyc_inspection_data','Cuisine.txt')
#Fields:"CUISINECODE","CODEDESC"
violationdt_filename=os.path.join('nyc_inspection_data','Violation.txt')
#Fields:"STARTDATE","ENDDATE","CRITICALFLAG","VIOLATIONCODE","VIOLATIONDESC"
webextractdt_filename=os.path.join('nyc_inspection_data','WebExtract.txt')
#Fields:"CAMIS","DBA","BORO","BUILDING","STREET","ZIPCODE","PHONE","CUISINECODE","INSPDATE","ACTION","VIOLCODE","SCORE","CURRENTGRADE","GRADEDATE","RECORDDATE"

actions=pd.read_csv(actiondt_filename)
cuisines=pd.read_csv(cuisinedt_filename, encoding = 'latin-1') 
violations=pd.read_csv(violationdt_filename, encoding = 'latin-1', delimiter = ",", quotechar = '"')
grades=pd.read_csv(webextractdt_filename, encoding = 'latin-1', low_memory=False)
boroughs={1:'Mahnhattan', 2:'The Bronx', 3:'Brooklyn',4:'Queens',5:'Staten Island'}
print('all datafiles loaded')


##q4 violation_by_cuisine
##Which cuisines tend to have a disproportionate number of what which violations?
##Answering this question isn't easy becuase you have to think carefully about
##normalizations.
##The right quantity is to look at is the conditional probability of a specific
##type of violation given a specific cuisine type and divide it by the
##unconditional probability of the violation for the entire population. Taking
##this ratio gives the right answer.  Return the 20 highest ratios of the form:
##
##    ((cuisine, violation), ratio, count)
##**Hint:**
##1. The definition of a violation changes with time.  For example, 10A can mean
##   two different things "Toilet facility not maintained ..." or "Vermin or
##   other live animal present ..." when things were prior to 2003. To deal with
##   this, you should limit your analysis to violation codes with end date after
##   Jan 1, 2014. (This end date refers to the validity time ranges in
##   Violation.txt).
##2. The ratios don't mean much when the number of violations of a given type and
##   for a specific category are not large (why not?).  Be sure to filter these
##   out.  We chose 100 as our cutoff.
   

print('starting task5')
grades=grades[pd.notnull(grades["CUISINECODE"])]
grades["CUISINECODE"] = grades["CUISINECODE"].astype(int)


unique_camis=list(set(grades["CAMIS"]))
total_number_of_violations=len(grades) 

unique_cuisinecodes=list(set(grades["CUISINECODE"]))
unique_violcodes=list(set(grades["VIOLCODE"]))
no_of_cuisine_viol_pairs=len(unique_cuisinecodes)*len(unique_violcodes)


violations=violations.groupby("VIOLATIONCODE").last() 
q4_data= pd.DataFrame({"COUNT" : grades.groupby( [ "VIOLCODE", "CUISINECODE"] ).size()}).reset_index()
q4_data["CUISINECODE"] = q4_data["CUISINECODE"].astype(int)
q4_data["VIOLDESC"] = q4_data["VIOLCODE"].map(violations["VIOLATIONDESC"])
cuisines=cuisines.groupby("CUISINECODE").last() 
q4_data["CUISINEDESC"]=q4_data["CUISINECODE"].map(cuisines["CODEDESC"])
violations.to_csv("violations_short.csv", sep=",")
q4_data=q4_data.sort_values(by="COUNT",ascending=False)
q4_data=q4_data[q4_data["COUNT"]>=100]

remaining_unique_cuisines=list(set(q4_data["CUISINECODE"]))
helperdf=pd.DataFrame({"CUISINECODE":remaining_unique_cuisines,"VIOLSNUMBER":'nonesofar',"CAMISNUMBER":'nonesofar'})

for index, row in helperdf.iterrows():
    temp=grades[grades["CUISINECODE"] == row["CUISINECODE"]]
    helperdf.set_value(index,"NUM_ALLVIOLS_PER_CUISINETYPE",len(temp))

helperdf=helperdf.set_index(["CUISINECODE"]) 
q4_data["NUM_ALLVIOLS_PER_CUISINETYPE"] = q4_data["CUISINECODE"].map(helperdf["NUM_ALLVIOLS_PER_CUISINETYPE"])

remaining_unique_violcodes=list(set(grades["VIOLCODE"]))
helperdf2=pd.DataFrame({"VIOLCODE":remaining_unique_violcodes,"VIOLCODE_COUNT_IN_WHOLE_DB":'nonesofar'})
for index, row in helperdf2.iterrows():
    temp=grades[grades["VIOLCODE"] == row["VIOLCODE"]]
    helperdf2.set_value(index,"VIOLCODE_COUNT_IN_WHOLE_DB",len(temp))

helperdf2=helperdf2.set_index(["VIOLCODE"])
q4_data["VIOLCODE_COUNT_IN_WHOLE_DB"] = q4_data["VIOLCODE"].map(helperdf2["VIOLCODE_COUNT_IN_WHOLE_DB"])


q4_data["RATIO"]=(q4_data.COUNT/q4_data.NUM_ALLVIOLS_PER_CUISINETYPE) / (q4_data.VIOLCODE_COUNT_IN_WHOLE_DB / total_number_of_violations) #careful with VIOLSNUMBER - it's per cuisine number, not (cuisine,violtype) pair
q4_data=q4_data.sort_values(by="RATIO",ascending=False)
q4_data=q4_data[:20]
q4_data = q4_data[['CUISINEDESC', 'VIOLDESC', 'RATIO', 'COUNT']] #getting rid of all extra columns and rearrnging the remaining ones

q4_data.to_csv("q4_temp.csv", sep=",")

