import pickle
import streamlit as st
import pandas as pd
Data=pickle.load(open(r'C:\Users\TREIKA\Desktop\diabetis deployment\model.pkl','rb'))
 
st.title('Diabetes Prediction Web App')
st.info('Easy Application for Diabetes Prediction')
st.sidebar.header('Feature Selection')


Pregnancies=st.text_input('Pregnancies')
Glucose=st.text_input('Glucose')
BloodPressure=st.text_input('BloodPressure')
SkinThickness=st.text_input('SkinThickness')
Insulin=st.text_input('Insulin')
BMI=st.text_input('BMI')
DiabetesPedigreeFunction=st.text_input('DiabetesPedigreeFunction')
Age=st.text_input('Age')

df=pd.DataFrame({
'Pregnancies':[Pregnancies],
'Glucose':[Glucose],
'BloodPressure':[BloodPressure],
'SkinThickness' :[SkinThickness],
'Insulin' :[Insulin],
'BMI' :[BMI],
'DiabetesPedigreeFunction' :[DiabetesPedigreeFunction],
'Age' :[Age]
},index=[0])
sub=st.sidebar.button('confirm')
if sub :
 result= Data.predict(df)
 if result==0:
  st.sidebar.write('the patient is Not diabetic')
 else:
  st.sidebar.write('the patient isdiabetes.py diabetic')