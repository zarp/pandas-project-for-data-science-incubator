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

#### score_by_cuisine
##Return a list of the 75 tuples of the form
##
##    (cuisine, mean score, stderr, number of reports)
##
##for each of the 75 cuisine types with at least 100 violation reports. Sort the
##list in ascending order by score. Are the least sanitary and most sanitary
##cuisine types surprising?
##
##**Note:** It's interesting to think again about what this analysis is trying
##to say and how it differs from the analysis by zipcode. How should this
##affect the calculation in your opinion?


print('starting task4')
      
grades=grades[pd.notnull(grades["CUISINECODE"])]
grades["CUISINECODE"] = grades["CUISINECODE"].astype(int)
all_zipcodes=list(grades["CUISINECODE"])

unique_cuisinecodes=list(set(grades["CUISINECODE"]))
unique_cuisines_w_over100viols=0
q3_ans=np.zeros((75,4,))  
for index, curr_cuisinecode in enumerate(unique_cuisinecodes): 
    temp=grades[grades["CUISINECODE"] == curr_cuisinecode]
    temp2=temp[temp["VIOLCODE"].notnull()] 
    if len(temp2)>100: 
        q3_ans[unique_cuisines_w_over100viols,0]=curr_cuisinecode
        all_scores_for_quisine=temp["SCORE"] 
        q3_ans[unique_cuisines_w_over100viols,1]=np.mean(all_scores_for_quisine) 
        q3_ans[unique_cuisines_w_over100viols,2]=np.std(all_scores_for_quisine)/np.sqrt(all_scores_for_quisine.count())
        q3_ans[unique_cuisines_w_over100viols,3]=len(all_scores_for_quisine) 
        unique_cuisines_w_over100viols+=1


q3_ans=q3_ans[q3_ans[:,1].argsort()]

format_fix=q3_ans[:,0].astype(int)
format_fix=format_fix[:].astype(str)



print 'translating...'
for index,it in enumerate(format_fix): 
    format_fix[index]=str(cuisines.loc[cuisines["CUISINECODE"] == int(it)]["CODEDESC"].values[0])
  
ans=[]

for ind,item in enumerate(q3_ans[0:len(unique_cuisinecodes)]):
    ans.append((format_fix[ind],q3_ans[ind,1],q3_ans[ind,2],int(q3_ans[ind,3])))

np.savetxt("q3_ans_temp.csv", q3_ans, delimiter=",")
