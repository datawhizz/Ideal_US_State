import pandas as pd
import numpy as np
from sklearn import preprocessing

cost_of_living = pd.read_excel("C:/Users/mayur/Downloads/fbc_data_2022 (2).xlsx",sheet_name = "Metro")
#loading the excel sheet in python


print(cost_of_living)
#analyze the data, look at the number of rows and columns. Correct the header name, row zero should be the header.

cost_of_living.columns=cost_of_living.iloc[0]
#making row zero as the header
cost_of_living=cost_of_living[1:]
#Moving row 1 to row 0 and update the dataframe and the printing and reanalyzing the dataframe

# DIRECTION: removing columns and filtering for only the required columns in the next few lines

COL=cost_of_living.iloc[:,[1,3,12,13,14,15,16,17,18,19,20]].copy()
#Using DataFrame.iloc[] to create new DataFrame by df.copy() function. It copies all column numbers to a new dataframe.
COL
#COL is our new dataframe which contains only annual costs and not monthly costs

COL1=COL[(COL.Family=='2p0c')]
#filtering for specifically my scenario i.e two person families with no children(yet)
COL1=COL1.iloc[:,[0,2,3,4,5,6,7,8,9,10]].copy()
COL1.isna()
COL2 = COL1.dropna(axis = 0, how = 'any',thresh = None, inplace = False )

COL2.columns=COL2.columns.str.replace(' ', '_')
COL2.columns=COL2.columns.str.replace('.','')
COL2
#changing column names to remove the spaces and other special characters from the column name
COL3=COL2.groupby('State_abv').apply(np.mean)
COL3
#grouping by state and getting average costs per state for all states

## Analsyis of Education System using AP score, Math and Language assesments and Graduation Rates

#Direction: AP data is being cleaned and prepared
AP=pd.read_excel("C:/Users/mayur/Downloads/school-report-of-ap-exams-grades-11-12-2021-2022.xls")
#loading excel file into dataframe
AP=AP.iloc[:,[0,1,2,3,4,5,9,10]].copy()
#copying columns needed and remvoing the rest using df.copy() and iloc method
index=("State","total_students","Total_ap_students_2021","Total_ap_students_2022","Total_ap_exams_2021","Total_ap_exams_2022","Exam_scores_above_3_2021","Exam_scores_above_3_2022")
#creating a list of the columns we need
AP.columns=index
#changing column names using df.columns() function and using index as a list of column names 
#Moving row 2 to row 0 and also removing extra lines that are not required (after 52) 
AP=AP[2:53].copy()
#resetting indexes and multiple transformations in the dataframe using reset index function of pandas
AP=AP.reset_index()
#Our original data did not have total grade 11 and 12 students in illinois
#Adding the number of grade 11 and grade 12 students in Illinois from 2021-2022 Illinois state board website
#https://www.isbe.net/pages/fall-enrollment-counts.aspx
AP['total_students'].values[13]=296360
#calculating participation percentage per state
part_pct=AP['Total_ap_students_2022']/AP['total_students']
AP['part_pct']=part_pct
#calculating rating for AP score based on particiaption rate and exam scores above 3 as criteria. 
#THis rating is used in rating colleges based on education
ap_score=(AP['Exam_scores_above_3_2022']*0.75)+(AP['part_pct']*0.25)
#creating a numpy array of ratings in order to normalize it using the preprocessing function
ap_arr = ap_score.values #returns a numpy array
#reshaping matrix into a 2D array using the reshape function from numpy
#min_max scaler does not work with 1 dimensional array
ap_matrix=ap_arr.reshape(-1,1)
#using min max scaler from scikit learn to normalize the ap ratings between 0 and 1
min_max_scaler = preprocessing.MinMaxScaler()
ap_scaled = min_max_scaler.fit_transform(ap_matrix)
#converting into dataframe to join it to the main AP dataframe
ap_score_scaled = pd.DataFrame(ap_scaled)
#adding the AP rating column and data to the main dataframe
AP["AP_rating"]=ap_score_scaled
apr=AP[['State','AP_rating']]
apr

#Direction: Math assesment and Reading assessment  and graduation rates dataset cleanup and ready for analysis

math_assess=pd.read_csv("C:/Users/mayur/Downloads/SPCsv202304075238.csv")
#loading math assesment data into df
index_1=('State','avg_score','diff_natl_avg','sig_symbol','pct_at_above_basic','pct_at_above_profcnt')
#renaming columns
math_assess.columns=index_1
#resetting index to initial indexes
math_assess=math_assess.reset_index()
#dropping unrequired columns i.e the index column and the symbol column which has no values.
math_assess=math_assess.drop(columns=['index','sig_symbol'])
#dropping puerto rico, DoDEA and National public row data
math_assess=math_assess.drop([0,29,53])
math_assess.sort_values('diff_natl_avg')
#resetting index to initial indexes
math_assess=math_assess.reset_index()
#dropping unrequired columns i.e the index column
math_assess=math_assess.drop(columns=['index'])
#converting the pct_at_above_profcnt to a float type so we can carry out numeric operations on that column
math_assess['pct_at_above_profcnt']=math_assess['pct_at_above_profcnt'].astype('float')
#calculating rating for math score based on pct of students above proficient and percentage above basic score.
math_assess['math_rating']=(math_assess['pct_at_above_basic']*0.004)+(math_assess['pct_at_above_profcnt']*0.006)
#creating a numpy array of ratings in order to normalize it using the preprocessing function
math_arr = math_assess['math_rating'].values #returns a numpy array
#reshaping matrix into a 2D array using the reshape function from nump
#min_max scaler does not work with 1 dimensional array
math_matrix=math_arr.reshape(-1,1)
#using min max scaler from scikit learn to normalize the ap ratings between 0 and 1
min_max_scaler = preprocessing.MinMaxScaler()
math_scaled = min_max_scaler.fit_transform(math_matrix)
#converting into dataframe to join it to the main math score dataframe
math_score_scaled = pd.DataFrame(math_scaled)
#adding the math rating column and data to the main dataframe
math_assess["math_rating"]=math_score_scaled
ma=math_assess[['State','math_rating']]
ma

#repeating above steps for reading data

read_assess=pd.read_csv("C:/Users/mayur/Downloads/SPCsv202304080200.csv")
index_2=('State','avg_score','diff_natl_avg','sig_symbol','pct_at_above_basic','pct_at_above_profcnt')
#renaming columns
read_assess.columns=index_1
#sorting values by differnce with national score, which is our criteria of judging a state's performance
read_assess.sort_values('diff_natl_avg')
#removed column 3 which had no relevant data
read_assess=read_assess.iloc[:,[0,1,2,4,5]]
#dropping puerto rico, DoDEA and National public row data
read_assess=read_assess.drop([0,27,53])
#resetting index to initial indexes
read_assess=read_assess.reset_index()
#dropping unrequired columns i.e the index column
read_assess=read_assess.drop(columns=['index'])
#converting the pct_at_above_profcnt to a float type so we can carry out numeric operations on that column
read_assess['pct_at_above_profcnt']=read_assess['pct_at_above_profcnt'].astype('float')
read_assess['pct_at_above_basic']=read_assess['pct_at_above_basic'].astype('float')
#calculating rating for reading score based on pct of students above proficient and percentage above basic score.
read_assess['read_rating']=(read_assess['pct_at_above_basic']*0.004)+(read_assess['pct_at_above_profcnt']*0.006)
#creating a numpy array of ratings in order to normalize it using the preprocessing function
read_arr = read_assess['read_rating'].values #returns a numpy array
#reshaping matrix into a 2D array using the reshape function from nump
read_matrix=read_arr.reshape(-1,1)
#using min max scaler from scikit learn to normalize the ap ratings between 0 and 1
min_max_scaler = preprocessing.MinMaxScaler()
read_scaled = min_max_scaler.fit_transform(read_matrix)
#converting into dataframe to join it to the main math score dataframe
read_score_scaled = pd.DataFrame(read_scaled)
#adding the math rating column and data to the main dataframe
read_assess["read_rating"]=read_score_scaled
ra=read_assess[['State','read_rating']]
ra

#uploading Graduation rates data in a dataframe
grad_rate=pd.read_csv("C:/Users/mayur/Downloads/data.csv")
grad_rate=grad_rate.sort_values('HighSchool',ascending=False)
#copying columns needed and remvoing the rest using df.copy() and iloc method
index=("fips","State","densityMi","pop2023","pop2022","pop2020","pop2019","pop2010","growthRate","growth","growthSince2010","HighSchool")
#creating a list of the columns we need
grad_rate.columns=index
#changing column names using df.columns() function and using index as a list of column names
#converting the percentage values to decimals between 0 and 1
#these decimal values will be our graduation rating per state
grad_rate['HighSchool']=grad_rate['HighSchool']/100
#creating array of high shool grad rates in order to then normalize the values
grad_arr=grad_rate['HighSchool'].values
#reshaping matrix into a 2D array using the reshape function from nump
grad_matrix=grad_arr.reshape(-1,1)
#using minmaxscaler to scale the grad rate values
min_max_scaler=preprocessing.MinMaxScaler()
grad_scaled = min_max_scaler.fit_transform(grad_matrix)
#converting into dataframe to join it to the main math score dataframe
grad_score_scaled = pd.DataFrame(grad_scaled)
#adding the math rating column and data to the main dataframe
grad_rate["grad_rating"]=grad_score_scaled
gr=grad_rate[["State","grad_rating"]]
gr

#Giving a score to each state based on AP, math and reading asssesment and graduation rates
#The logic is 45% weightage to AP scores, 20% each to math and reading and 15% to graduation rate
#joining data frames to get a common dataframe that can be used for weightage based scoring
df1=pd.merge(apr,ra,how='outer',on='State')
df2=pd.merge(df1,ma,how='outer',on='State')
df3=pd.merge(df2,gr,how='outer',on='State')
df3['total_rating']=df3['AP_rating']*0.45+df3['read_rating']*0.2+df3['math_rating']*0.2+df3['grad_rating']*0.15
df3.sort_values(by=['total_rating'])

## Crime Data Analysis

crime_rating=pd.read_csv("C:/Users/mayur/Downloads/crime_data.csv")

crime_rating

## Healthcare Analysis based on per capita spend

healthcare_cost=pd.read_csv("C:/Users/mayur/Downloads/healthcare_expenditure_data.csv")

#creating array of healthcare cost in order to then normalize the values
healthcare_arr=healthcare_cost['spentPerCapita'].values
#reshaping matrix into a 2D array using the reshape function from nump
healthcare_matrix=healthcare_arr.reshape(-1,1)
#using min max scaler from scikit learn to normalize the healthcare ratings between 0 and 1
min_max_scaler = preprocessing.MinMaxScaler()
healthcare_matrix = min_max_scaler.fit_transform(healthcare_matrix)
#converting into dataframe to join it to the main math score dataframe
healthcare_cost_scaled=pd.DataFrame(healthcare_matrix)
healthcare_cost['healthcare_rating']=healthcare_cost_scaled
healthcare_rating=healthcare_cost[['state','healthcare_rating']]
healthcare_rating
#healthcare_rating

