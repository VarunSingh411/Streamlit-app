import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 

st.set_page_config(layout='wide')

df = pd.read_csv("E:\DSMP\ML\Project\startupCleaned_funding.csv")

def load_overall_analysis():
    col1,col2,col3,col4 = st.columns(4)
    #Total invested amount 
    with col1:
        total =round(df['amount'].sum(),2)
        st.subheader('Total Amount Invested:')
        st.metric('Total',str(total)+'Cr')

    #Maximum invested amount 
    with col2:
        max =df.groupby('startup')['amount'].sum().sort_values(ascending =False).head(1).values[0]
        st.subheader('Maximum Amount Invested:')
        st.metric('Max',str(max)+'Cr')

    #Average invested amount
    with col3:
        avg =round(df.groupby('startup')['amount'].sum().mean(),1)
        st.subheader('Avg Amount Invested:')
        st.metric('Avg',str(avg)+'Cr')

    #No of investment every month  :
    st.subheader('No of investment every month:')
    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    df['year']=df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    temp_df =df.groupby(['year','month'])['startup'].count().reset_index()
    temp_df['x_axis'] = temp_df['year'].astype('str')+'-'+temp_df['month'].astype('str')
    fig5,ax5 =plt.subplots()
    ax5.plot(temp_df['x_axis'],temp_df['startup'])
    ax5.set_xlabel('Year-Month')
    ax5.set_ylabel('count')
    st.pyplot(fig5)


def load_ivestor_detail(investor):
    st.title(investor)

    #loading recent investment 
    st.subheader('Recent Investement details:')
    st.dataframe(df[df['investors'].str.contains(investor)][['date','startup','vertical','city','round','amount']].head())
    

    
    #Biggest Investment 
    
    
    
    st.subheader('Biggest Investment:')
    big_series=(df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending =False))
    st.dataframe(big_series)
        
    # Showing graphical view 
    st.subheader('Graphical View')
    fig,ax =plt.subplots()
    ax.bar(big_series.index,big_series.values,color ='red')
    ax.set_ylabel('Amount Invested in Cr')
    ax.set_xlabel('Startup')
    st.pyplot(fig)

   # Sector wise investment
      
    st.subheader('SectorWiseInvestement:') 
    vertical_series= df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
    st.dataframe(vertical_series)

    fig1,ax1 =plt.subplots()
    ax1.pie(vertical_series,labels=vertical_series.index,autopct='%.2f')
    st.pyplot(fig1)

    

    # Round wise investment
    st.subheader('RoundWiseInvestment')
    round_series= df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
    fig2,ax2 =plt.subplots()
    ax2.pie(round_series,labels=round_series.index,autopct='%.2f')
    st.pyplot(fig2)

     # City wise investment
    
    st.subheader('CityWiseInvestment')
    round_series= df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
    fig3,ax3 =plt.subplots()
    ax3.pie(round_series,labels=round_series.index,autopct='%.2f')
    st.pyplot(fig3)

     # Year Wise Investment
    st.subheader('YearWiseInvestment')
    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    df['year']=df['date'].dt.year
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig4,ax4 =plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Amount Invested in Cr')
    st.pyplot(fig4)
     

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select one',['Overall Analysis','Startup Analysis','Investor Analysis'])
if option =='Overall Analysis':
    btn= st.sidebar.button('ShowOverallAnalysis')
    if btn:
       st.title('Overall Analysis')
       load_overall_analysis()

elif option =='Startup Analysis':
   st.sidebar.selectbox('Select Startup',sorted(df['Startup Name'].unique().tolist()))
   btn1 =st.sidebar.button('DisplayStartupDetails')
   st.title('Startup Analysis')
else:
    value =st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 =st.sidebar.button('DisplayInvestorDetails')

    if btn2:
        load_ivestor_detail(value)


    