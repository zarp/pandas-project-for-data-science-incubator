import csv
import pandas as pd
import numpy as np
import os

#"Violation.txt" was modified by:
#1. deleting anything matching the following regex: <a.*a>
#   Text between <a> and </a> tags was deleted because it contained quotechar and delimiter chars making parsing difficult. Also, it's not useful for this model anyway
#2. removing manually the few nested doublequotes

actiondt_filename=os.path.join('nyc_inspection_data','Action.txt')
#Fields: "STARTDATE","ENDDATE","ACTIONCODE","ACTIONDESC"
cuisinedt_filename=os.path.join('nyc_inspection_data','Cuisine.txt')
#Fields:"CUISINECODE","CODEDESC"
violationdt_filename=os.path.join('nyc_inspection_data','Violation.txt')
#Fields:"STARTDATE","ENDDATE","CRITICALFLAG","VIOLATIONCODE","VIOLATIONDESC"
webextractdt_filename=os.path.join('nyc_inspection_data','WebExtract.txt')
#Fields:"CAMIS","DBA","BORO","BUILDING","STREET","ZIPCODE","PHONE","CUISINECODE","INSPDATE","ACTION","VIOLCODE","SCORE","CURRENTGRADE","GRADEDATE","RECORDDATE"

actions=pd.read_csv(actiondt_filename)
cuisines=pd.read_csv(cuisinedt_filename, encoding = 'latin-1') #utf-8'
violations=pd.read_csv(violationdt_filename, encoding = 'latin-1', delimiter = ",", quotechar = '"')
grades=pd.read_csv(webextractdt_filename, encoding = 'latin-1', low_memory=False)
boroughs={1:'Mahnhattan', 2:'The Bronx', 3:'Brooklyn',4:'Queens',5:'Staten Island'}
print('all datafiles loaded')

## Q1:
##(zipcode, mean score, standard error, number of restaurants)
##for each of the 92 zipcodes in the city with over 100 restaurants. Use the
##score from the latest inspection date for each restaurant. 
print('starting task Q1')

grades=grades[pd.notnull(grades['ZIPCODE'])]
grades["ZIPCODE"] = grades["ZIPCODE"].astype(int)
all_zipcodes=list(grades["ZIPCODE"])

unique_zipcodes=list(set(grades["ZIPCODE"]))
unique_zipcodes_w_over100camis = 0
q1_ans=np.zeros((len(unique_zipcodes),4,))  
for index, curr_zipcode in enumerate(unique_zipcodes): 
    temp = grades[grades["ZIPCODE"] == curr_zipcode]
    if len(temp)>100: #a required but not sufficient condition. E.g. can have 50 CAMIS with 2 inspections => len=100 but only 50 distinct CAMIS
        unique_CAMIS_at_curzip=list(set(temp["CAMIS"]))
        camis_latest=np.zeros(len(unique_CAMIS_at_curzip))
        if len(unique_CAMIS_at_curzip)>100:
            q1_ans[unique_zipcodes_w_over100camis,0] = curr_zipcode
            for index2, curr_CAMIS in enumerate(unique_CAMIS_at_curzip):
                temp2=temp[temp['CAMIS'] == curr_CAMIS]
                if len(temp2)>0:
                    temp2["INSPDATE"] = pd.to_datetime(temp2.INSPDATE)

                    temp2=temp2.sort_values(by="INSPDATE",ascending=False)
                    latest=temp2.iloc[0]
                    camis_latest[index2]=latest["SCORE"]

            camis_latest_masked=np.ma.masked_array(camis_latest,np.isnan(camis_latest))
            q1_ans[unique_zipcodes_w_over100camis,1]=np.mean(camis_latest_masked)
            q1_ans[unique_zipcodes_w_over100camis,2]=np.std(camis_latest_masked)/np.sqrt(camis_latest_masked.count())
            q1_ans[unique_zipcodes_w_over100camis,3]=len(unique_CAMIS_at_curzip) 
            unique_zipcodes_w_over100camis+=1
            
np.savetxt("q1_ANS.csv", q1_ans[0:92], delimiter=",")

