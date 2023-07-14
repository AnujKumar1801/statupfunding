import streamlit as st
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/campusx-official/streamlit-basics/master/startup_funding.csv")


# cleaning the dataset
df.drop(columns=['Remarks'],inplace=True)

df.set_index('Sr No',inplace=True)

df.rename(columns={
    'Date dd/mm/yyyy':'date',
    'Startup Name':'startup',
    'Industry Vertical':'vertical',
    'SubVertical':'subvertical',
    'City  Location':'city',
    'Investors Name':'investors',
    'InvestmentnType':'round',
    'Amount in USD':'amount'    
    
},inplace=True)

df.head()

df['amount'] = df['amount'].fillna('0')

df['amount'] = df['amount'].str.replace(',','')
df['amount'] = df['amount'].str.replace('undisclosed','0')
df['amount'] = df['amount'].str.replace('unknown','0')
df['amount'] = df['amount'].str.replace('Undisclosed','0')

df = df[df['amount'].str.isdigit()]

df['amount'] = df['amount'].astype('float')

def to_inr(dollar):
    inr = dollar * 82.5
    return inr/10000000


df['amount'] = df['amount'].apply(to_inr)
df['date'] = df['date'].str.replace('05/072018','05/07/2018')
df['date'] = pd.to_datetime(df['date'],errors='coerce')

df = df.dropna(subset=['date','startup','vertical','city','investors','round','amount'])

df.to_csv('subset_cleaned.csv',index = False)




allstartups = df['startup'].unique().tolist()
allinvestors = sorted(set(df['investors'].str.split(',').sum()))

st.sidebar.title('Startup funding analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis','startup','investors'])

if option.lower() == 'overall analysis':
    st.title('Overall Analysis')
elif option.lower() == 'startup':
    st.sidebar.selectbox('Select Startup', allstartups)
    st.sidebar.button('Find Startup Details')
    st.title('StartUp Analysis')
else:
    st.sidebar.selectbox('Select StartUp', allinvestors)
    st.sidebar.button('Find Investor Details')
    st.title('Investor Analysis')


