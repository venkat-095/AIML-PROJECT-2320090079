
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler 
 
data={ 
    'StudentID':[1,2,3,4,5], 
    'Age':[16,17,18,19,20], 
    'Grade':[55,85,90,95,100] 
} 
 
df=pd.DataFrame(data) 
scaler=MinMaxScaler() 
df[['Age','Grade']]=scaler.fit_transform(df[['Age','Grade']]) 
print(df)