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


## score_by_borough
##Return a list of tuples of the form:
##    (borough, mean score, stderr, number of restaurants)
##for each of the city's five boroughs. Sort the list in ascending order by grade.

print('starting task2')

grades=grades[pd.notnull(grades['ZIPCODE'])]
grades["ZIPCODE"] = grades["ZIPCODE"].astype(int)
all_zipcodes=list(grades["ZIPCODE"])

unique_boros=list(set(grades["BORO"]))

q2_ans=np.zeros((len(unique_boros),4,)) 
for index, curr_boro in enumerate(unique_boros): 
    if curr_boro!=0:
        temp=grades[grades["BORO"] == curr_boro]
        unique_CAMIS_at_boro=list(set(temp["CAMIS"])) 
        
        camis_latest=np.zeros(len(unique_CAMIS_at_boro))
        q2_ans[curr_boro,0]=curr_boro
        for index2, curr_CAMIS in enumerate(unique_CAMIS_at_boro):
            temp2=temp[temp['CAMIS']==curr_CAMIS]
            if len(temp2)>0:
                temp2["INSPDATE"] = pd.to_datetime(temp2.INSPDATE)

                temp2=temp2.sort_values(by="INSPDATE",ascending=False)
                latest=temp2.iloc[0]
                camis_latest[index2]=latest["SCORE"]

        camis_latest_masked=np.ma.masked_array(camis_latest,np.isnan(camis_latest))
        q2_ans[curr_boro,1]=np.mean(camis_latest_masked) 
        q2_ans[curr_boro,2]=np.std(camis_latest_masked)/np.sqrt(camis_latest_masked.count())
        q2_ans[curr_boro,3]=len(unique_CAMIS_at_boro)

np.savetxt("q2_ans.csv", q2_ans, delimiter=",")

