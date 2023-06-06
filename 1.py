import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
from statistics import mean
import math

def GM11(x0):
    n = len(x0)
    print(x0)
    x1=[]            
    x=0

    for i in range(n):
        x=x0[i]+x
        x1.append(x)
    print(x1)
    
    
    # Build the AGO sequence
    z = np.zeros(n)
    for k in range(1, n):
        z[k] = round(0.5*x1[k-1] + 0.5*x1[k])

    # Estimate the parameters a and Z1 using the differential equation of AGO
    z1 = z[1:]
    print(z1)
    
    B = np.column_stack((-(z1), np.ones(n-1)))
    print(B)
    
    x=x0[1:]
    Y = x.T
    print(Y)
    
    a, u = np.dot(np.linalg.inv(np.dot(B.T, B)), np.dot(B.T, Y))
    print(a)
    print(u)

    y_pred1 =[]
    for k in range(1,n+3):
        y_pred = (x0[0] - u/a)*np.exp(-a*(k-1))+u/a
        y_pred1.append(y_pred)
    # y_pred1 =y_pred1[1:]
    print(y_pred1)
    
    
    y_pred0=[]
    for k in range(1,n+2):
        y_pred = round(y_pred1[k] - y_pred1[k-1])
        y_pred0.append(y_pred)
    print(y_pred0)
    
    
    # RPE=[]
    # for i in range(n):
    #     rpe = round((abs(x0[i] - y_pred0[i])/x0[i])*100)
    #     RPE.append(rpe)
    # print(RPE)    
    
    # for i in range(n):
    #     pri_acc = 100-RPE[i]
    #     Pridiction_accuracy.append(pri_acc)
    # print(Pridiction_accuracy)
    
    RMSE =[]
    for i in range(n):
        rmse = math.sqrt((x0[i] - y_pred0[i])**2)
        RMSE.append(rmse)
    # Pridiction_accuracy=[]
    
    
    MAPE = mean(RMSE)
    print(MAPE)


# Pre-processing of data
xls = pd.ExcelFile("all_output (1).xlsx")

years = ["2012","2013","2014","2015","2016","2017","2018","2019","2020", "2021", "2022", "2023"]

df_obj = dict()
for i in years:
    df_obj[i] = pd.read_excel(xls, i)
    df_obj[i] = df_obj[i].drop(["Unnamed: 0"],axis=True)

# print(df_obj['2023'].columns)

df = df_obj['2012']
# df = df.append(df_obj['2016'])
for i in range(2013,2023):
    df.append(df_obj[str(i)])
    
df1 = df.drop(["1104500527", "1104500529", "1.104501e+09", "7802195.0", "2100570073/ 2100567820/ 2100567898", "Aggregate Meter Reading (KWH)", "Difference", "SEEDs data (KWH)",  
               "PR (%)", "Any Issues/Problems Observed", "WO#"], axis=1)

df1['Insolation'] = df1['Insolation'].fillna(df1['Insolation'].mean())
# df1 = df1.fillna(0)

df1['NO-OFF-CLEAN MODULES'] = df1['NO-OFF-CLEAN MODULES'].replace(r'^\s*$', np.nan, regex=True)
df1['NO-OFF-CLEAN MODULES'] = df1['NO-OFF-CLEAN MODULES'].fillna(0)

df1['NO-OFF-CLEAN MODULES'] = pd.to_numeric(df1['NO-OFF-CLEAN MODULES'])


# print(df1)


df1['Date'] = pd.to_datetime(df1['Date'])

df1 = df1.set_index('Date')
df1 = df1.drop(["Unnamed: 15"],axis=True)

df1['Total Generation (KWH)'] = pd.to_numeric(df1['Total Generation (KWH)'])
# print(df1['Total Generation (KWH)'].dtype)

df1 = df1.drop(["Cable and Fuse maintenance","NO-OFF-CLEAN MODULES", "No Module Cleaning","Rainy day", "Insolation" ,"Transformer replacement and maintenance","Plant Shutdown","Internet","Battery","Module Cleaning by rains"], axis=1)
print(df1)


target =df1['Total Generation (KWH)']
print(target.shape)
# y_pred = GM11(target)

