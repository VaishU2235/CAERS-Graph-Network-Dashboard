# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 14:08:29 2021

@author: admin
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objects as go


# Class Begin.....

class Dashboard:
    def __init__(self, data, transformed_data, years, unique_years, orgs, orgs_unique, prods, prods_unique):
        self.data = data
        self.transformed_data = transformed_data
        self.years = years
        self.unique_years = unique_years
        self.orgs = orgs
        self.orgs_unique = orgs_unique
        self.prods = prods 
        self.prods_unique = prods_unique
        
    def get_data_industry(self, k):
        orgs =self.orgs
        years_unique = self.unique_years
        years = self.years
        total=[]
        for i in years_unique:
            sum=0
            for j in range(0,len(years)):
                if(years[j]==i and orgs[j]==k):
                    sum=sum+1
            total.append(sum)
        return total


    def get_data_product(self, k):
        prods = self.prods
        years_unique = self.unique_years
        years = self.years
        total=[]
        for i in years_unique:
            sum=0
            for j in range(0,len(years)):
                if(years[j]==i and prods[j]==k):
                    sum=sum+1
            total.append(sum)
        return total

    def brandwise_trend(self, k):
        total = self.get_data_industry(k)    
        fig = px.line(x = self.unique_years, y = total, title='Year Wise Trend for Industry: '+k, 
                         labels = {'x':'Years', 'y':'No. of Adverse Events'})
        st.plotly_chart(fig, use_container_width=True)


    def symptoms_industry(self, k):
        try:
            text = self.data.loc[self.data['PRI_FDA Industry Name']==k,'SYM_One Row Coded Symptoms'].values 
            wordcloud = WordCloud(background_color="white")
            wordcloud = wordcloud.generate(str(text))
            fig, ax = plt.subplots()
            plt.set_loglevel('WARNING')
            ax.imshow(wordcloud)
            ax.set_title('Most Common Symptoms for Industry: '+k)
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)
        except (ValueError, TypeError):
            st.text('No Symptoms for  this Industry')
         
    
    def outcomes_industry(self, k):
        try:
            text = self.data.loc[self.data['PRI_FDA Industry Name']==k,'AEC_One Row Outcomes'].values 
            wordcloud1 = WordCloud(background_color="white")
            wordcloud1 = wordcloud1.generate(str(text))
            fig1, ax1 = plt.subplots()
            plt.set_loglevel('WARNING')
            ax1.imshow(wordcloud1)
            ax1.set_title('Most Common Outcomes for Industry: '+k)
            ax1.axis('off')
            st.pyplot(fig1, use_container_width=True)
        except (ValueError, TypeError):
            st.text('No Outcomes for  this Industry')
       
    def productwise_trend(self, p):
        total = self.get_data_product(p)    
        fig = px.line(x = self.unique_years, y = total, title='Year Wise Trend for Brand/Product: '+p, 
                         labels = {'x':'Years', 'y':'No. of Adverse Events'})
        st.plotly_chart(fig, use_container_width=True)
        
    def symptoms_product(self, p):
        try:
            text = self.data.loc[self.data['PRI_Reported Brand/Product Name']==p,'SYM_One Row Coded Symptoms'].values 
            wordcloud = WordCloud(background_color="white")
            wordcloud = wordcloud.generate(str(text))
            fig, ax = plt.subplots()
            plt.set_loglevel('WARNING')
            ax.imshow(wordcloud)
            ax.set_title('Most Common Symptoms for Brand/Product: '+p)
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)
        except (ValueError, TypeError):
            st.text('No Symptoms for this Brand/Product')
        
    
    def outcomes_product(self,  p):
        try:
            text = self.data.loc[self.data['PRI_Reported Brand/Product Name']==p,'AEC_One Row Outcomes'].values 
            wordcloud1 = WordCloud(background_color="white")
            wordcloud1 = wordcloud1.generate(str(text))
            fig1, ax1 = plt.subplots()
            plt.set_loglevel('WARNING')
            ax1.imshow(wordcloud1)
            ax1.set_title('Most Common Outcomes for Brand/Product: '+p)
            ax1.axis('off')
            st.pyplot(fig1, use_container_width=True)
        except (ValueError, TypeError):
            st.text('No Outcomes for this Brand/Product')
        
        
    def industry_gender(self):
        fig = px.histogram(self.data['PRI_FDA Industry Name'], color=self.data['CI_Gender'], orientation='h', title='No. of Adverse Events by Industry Names with Gender', 
                           labels = {'value':'Industry Name', 'color':'Gender'}).update_yaxes(categoryorder="total ascending").update_layout(xaxis_title='No. of Adverse Events')
        st.plotly_chart(fig, use_container_width=True)
        
    def industry_product(self):
        fig = px.histogram(self.data['PRI_FDA Industry Name'], color=self.data['PRI_Product Role'], orientation='h', title='No. of Adverse Events by Industry Names with Product Role', 
                           labels = {'value':'Industry Name', 'color':'Product Role'}).update_yaxes(categoryorder="total ascending").update_layout(xaxis_title='No. of Adverse Events')
        st.plotly_chart(fig, use_container_width=True)
        
    def year_gender(self):
        fig = px.histogram(self.transformed_data["RA_CAERS Created Year"], color=self.transformed_data['CI_Gender'], orientation='v', title='No. of Adverse Events by Year with Gender', 
                           labels = {'value':'Years',  'color':'Gender'}).update_layout(yaxis_title='No. of Adverse Events')
        st.plotly_chart(fig, use_container_width=True)
        
    def age_gender(self):
        fig = px.histogram(self.transformed_data["CI_Age"], color=self.transformed_data['CI_Gender'], orientation='v', title='No. of Adverse Events by Age with Gender', 
                           labels = {'value':'Age (in Years)',  'color':'Gender'}).update_xaxes(categoryorder="total ascending").update_layout(yaxis_title='No. of Adverse Events')
        fig.update_xaxes(range=[0, 150])
        st.plotly_chart(fig, use_container_width=True)
        
    
    def pie_bar_charts(self):
        df1 = self.data['PRI_Product Role'].value_counts().to_frame()
        df2 = self.data['CI_Gender'].value_counts().to_frame()
        labels1 = list(df1.index)
        values1 = [74558, 16228]
        fig1 = go.Figure(data=[go.Pie(labels=labels1, values=values1)])
        fig1.update_layout(title_text='% of Adverse Events by Product Role')
        
        labels2 = list(df2.index)
        values2 = [58924, 26943, 4916, 2, 1]
        fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2, hole=.5)])
        fig2.update_layout(title_text='% of Adverse Events by Gender')
        
        fig3 = px.histogram(self.data['PRI_Product Role'], color=self.data['CI_Gender'], title='Product Role VS Gender'
                           , labels = {'value':'Product Role', 'color':'Gender'}).update_yaxes(categoryorder="total ascending").update_layout(yaxis_title='No. of Adverse Events')
        
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        with col3:
            st.plotly_chart(fig3, use_container_width=True)
            
    
    def missing_value(self):
        Missing_total   = self.data.isnull().sum().sort_values(ascending=False) 
        missing_data_info = pd.concat([Missing_total], axis = 1, keys=['Missing_Total'])
        missing_data_info['Attribute_Name'] = missing_data_info.index
        fig = px.bar(missing_data_info, x = 'Attribute_Name', y = 'Missing_Total')
        fig.update_layout(title_text='Total Missing Values by Attributes', xaxis_title="Attributes",yaxis_title="Total Missing Values")
        st.plotly_chart(fig, use_container_width=True)
        
    def age_outlier(self):
        fig = px.box(self.transformed_data, x="CI_Age", points="all")
        fig.update_layout(title_text='Outliers present in Age (In Years)', xaxis_title='Age (In Years)')
        st.plotly_chart(fig, use_container_width=True)
        
    def plot_3d_industry(self, industry):
        orgs = self.orgs
        orgs_unique = self.orgs_unique
        genders = list(self.data['CI_Gender'])
        #ages = list(self.data['CI_Age at Adverse Event']) 
        ages = list(self.transformed_data['CI_Age'])
        years_unique = self.unique_years
        
        
        for k in orgs_unique:
            female=[]
            male=[]
            agef=[]
            agem=[]
            for i in years_unique:
                summ=0
                countm=0
                countf=0
                sumf=0
                for j in range(0,len(self.years)):
                    if(years[j]==i and orgs[j]==industry):
                        if(genders[j]=='Female'):
                            countf=countf+1
                            sumf=sumf+ages[j]
                        if(genders[j]=='Male'):
                            countm=countm+1
                            summ=summ+ages[j]
        
                female.append(countf)
                if(countf!=0):
                    agef.append(sumf/countf)
                else:
                    agef.append(0)
                male.append(countm)
                if(countm!=0):
                    agem.append(summ/countm)
                else:
                    agem.append(0)
        df2 = pd.DataFrame({'years':years_unique, 'female':female, 'male':male, 'agef':agef, 'agem':agem})            
        fig=go.Figure() 
        fig.add_trace(
            go.Scatter3d(
                x=df2["years"],
                y=df2["female"],
                z=df2['agef'],
                name='Female'
            )
        )
        fig.add_trace(
            go.Scatter3d(
                x=df2["years"],
                y=df2["male"],
                z=df2['agem'],
                name='Male'
            )
        )
        fig.update_layout(title = 'Years VS Gender VS Median Age (in Years)', scene=dict(xaxis_title="Years",
            yaxis_title="No. of Adverse Events", zaxis_title="Median Age"))
        st.plotly_chart(fig, use_container_width = True)
        
     
    def bar_chart(self, product):
        fig = px.histogram(self.data.loc[self.data['PRI_Reported Brand/Product Name']==product,'CI_Gender'], 
                           title='No. of Adverse Events by Gender for Brand/Product: '+product, labels = {'value':'Gender'}).update_layout(yaxis_title='No. of Adverse Events')
        fig.update(layout_showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
    def main(self):
        st.set_page_config(layout="wide")
        st.markdown("<h1 style='text-align: center; color: black;'>QUARTERLY DATA EXTRACT (QDE) FROM THE CFSAN Adverse Event Reporting System (CAERS)</h1>", unsafe_allow_html=True)
        #st.title("QUARTERLY DATA EXTRACT (QDE) FROM THE CFSAN Adverse Event Reporting System (CAERS)")
        st.header("Dataset:")
        st.dataframe(self.data.head(10))
    
        col, col0 = st.columns(2)
        with col:
            self.missing_value()
    
        with col0:
            self.age_outlier()
            
        self.pie_bar_charts()
        
        col1, col2 = st.columns(2)
        with col1:
            self.year_gender()
        with col2:
            self.age_gender()
        
        
        col3, col4 = st.columns(2)
        with col3:
            self.industry_gender()
        with col4:
            self.industry_product() 
        
        industry = st.selectbox('Select Industry Name', self.orgs_unique)
        col5, col6 = st.columns(2)
        with col5:
            self.plot_3d_industry(industry)
        with col6:
            self.brandwise_trend(industry)
            
        col7, col8 = st.columns(2)
        with col7:
            self.symptoms_industry(industry)
        with col8:
            self.outcomes_industry(industry)
        
        product = st.selectbox('Select Brand/Product Name', self.prods_unique)
        col9, col10 = st.columns(2)
        with col9:
            self.bar_chart(product)
        with col10:
            self.productwise_trend(product)
        
        col11, col12 = st.columns(2)
        with col11:
            self.symptoms_product(product)
        with col12:
            self.outcomes_product(product)
            
# Class End.....


def convert_age(age, unit):
    if unit == 'Month(s)':
        age = age/12
    elif unit == 'Week(s)':
        age = age/52.143
    elif unit == 'Day(s)':
        age = age/365
    elif unit == 'Decade(s)':
        age = age*10
    else:
        age = age
    return age    
    
data = pd.read_csv('CAERS_ASCII_2004_2017Q2.csv')
transformed_data = pd.read_csv('CAERS_ASCII_2004_2017Q2.csv')
transformed_data['RA_CAERS Created Year'] = transformed_data['RA_CAERS Created Date'].astype(str).str[-4:]
transformed_data['CI_Age'] = transformed_data.apply(lambda x:convert_age(x['CI_Age at Adverse Event'], x['CI_Age Unit']), axis=1)       

dates = list(data['RA_CAERS Created Date'])
years = [int(i[-4:]) for i in dates if type(i)!=float]
unique_years = np.unique(years)
orgs = list(transformed_data['PRI_FDA Industry Name'])
orgs_unique = np.unique(orgs)
prods = list(transformed_data['PRI_Reported Brand/Product Name'])
prods_unique = np.unique(prods)
dash = Dashboard(data, transformed_data, years, unique_years, orgs, orgs_unique, prods, prods_unique)
dash.main()