import streamlit as st
import numpy as np
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer 
import re

st.title('Will you survive if you were among Titanic passengers or not :ship:')
passengerid = st.text_input("Input Passenger ID", '8585')
pclass = st.selectbox("Choose class", [1,2,3])
name  = st.text_input("Input Passenger Name", 'Soheil Tehranipour')
sex = st.select_slider("Choose sex", ['male', 'female'])
age = st.slider("Choose age", 0, 100)
sibsp = st.slider("Choose siblings",0,10)
parch = st.slider("Choose parch",0,10)
ticket = st.text_input("Input Ticket Number", "8585") 
fare = st.number_input("Input Fare Price", 0,1000)
cabin = st.text_input("Input Cabin", "C52")
embarked = st.selectbox("Did they Embark?", ['S','C','Q'])
columns = ['PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch','Ticket', 'Fare', 'Cabin', 'Embarked']
class PrepProcesor(BaseEstimator, TransformerMixin): 
    def fit(self, X, y=None): 
        self.ageImputer = SimpleImputer()
        self.ageImputer.fit(X[['Age']])        
        return self 
        
    def transform(self, X, y=None):
        X['Age'] = self.ageImputer.transform(X[['Age']])
        X['CabinClass'] = X['Cabin'].fillna('M').apply(lambda x: str(x).replace(" ", "")).apply(lambda x: re.sub(r'[^a-zA-Z]', '', x))
        X['CabinNumber'] = X['Cabin'].fillna('M').apply(lambda x: str(x).replace(" ", "")).apply(lambda x: re.sub(r'[^0-9]', '', x)).replace('', 0) 
        X['Embarked'] = X['Embarked'].fillna('M')
        X = X.drop(['PassengerId', 'Name', 'Ticket','Cabin'], axis=1)
        return X
#model = joblib.load('C:\\Users\\Mojtaba\\Downloads\\Compressed\\Streamlit-Titanic\\Streamlit-Titanic\\xgbpipe.joblib')
model = joblib.load('C:\\Users\\Mojtaba\\xgbpipe.joblib')
def predict():
    row = np.array([passengerid,pclass,name,sex,age,sibsp,parch,ticket,fare,cabin,embarked])
    X = pd.DataFrame([row], columns=columns)
    prediction = model.predict(X)
    if prediction[0] == 1: 
        st.success('Passenger Survived :material/thumb_up:')
    else: 
        st.error('Passenger did not Survive :material/thumb_down:')
trigger = st.button('Predict', on_click=predict)