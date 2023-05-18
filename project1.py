import streamlit as st
import pandas as pd
import pickle as pkl
import folium
import numpy as np



#%%writefile project1.py

import base64

import numpy as np

st.title ('Predicting success of new restaurants')
st.image ('https://www.posist.com/restaurant-times/wp-content/uploads/2019/04/The-Secret-Cook-Book-To-A-Successful-Restaurant.jpg')

 # front end elements of the web page 
html_temp = """ 
    <div style ="background-color:pink;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Predicting success of new restaurants</h1> 
    </div> 
    """
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 
st.subheader('by Walaa Nasr ')

#take input from user     
# following lines create boxes in which user can enter data required to make prediction

online_order = st.radio("can you order online?: ", ('yes', 'no'))
book_table = st.radio('can you book a table',("yes","no")) 

# Transform selected options to numerical values
online_order = 1 if online_order == 'yes' else 0
book_table = 1 if book_table == 'yes' else 0

# Get the selected city from the user
location = st.multiselect("Select a city", ('Banashankari', 'Basavanagudi', 'Mysore Road', 'Jayanagar',
       'Kumaraswamy Layout', 'Rajarajeshwari Nagar', 'Vijay Nagar',
       'Uttarahalli', 'JP Nagar', 'South Bangalore', 'City Market',
       'Bannerghatta Road', 'BTM', 'Kanakapura Road', 'Bommanahalli',
       'Electronic City', 'Sarjapur Road', 'Wilson Garden',
       'Shanti Nagar', 'Koramangala 5th Block', 'Richmond Road', 'HSR',
       'Koramangala 7th Block', 'Bellandur', 'Marathahalli', 'Whitefield',
       'East Bangalore', 'Old Airport Road', 'Indiranagar',
       'Koramangala 1st Block', 'Frazer Town', 'MG Road', 'Brigade Road',
       'Lavelle Road', 'Church Street', 'Ulsoor', 'Residency Road',
       'Shivajinagar', 'Infantry Road', 'St. Marks Road',
       'Cunningham Road', 'Race Course Road', 'Commercial Street',
       'Vasanth Nagar', 'Domlur', 'Koramangala 8th Block', 'Ejipura',
       'Jeevan Bhima Nagar', 'Old Madras Road', 'Seshadripuram',
       'Kammanahalli', 'Koramangala 6th Block', 'Majestic',
       'Langford Town', 'Central Bangalore', 'Brookefield',
       'ITPL Main Road, Whitefield', 'Varthur Main Road, Whitefield',
       'Koramangala 2nd Block', 'Koramangala 3rd Block',
       'Koramangala 4th Block', 'Koramangala', 'Hosur Road', 'RT Nagar',
       'Banaswadi', 'North Bangalore', 'Nagawara', 'Hennur',
       'Kalyan Nagar', 'HBR Layout', 'Rammurthy Nagar', 'Thippasandra',
       'CV Raman Nagar', 'Kaggadasapura', 'Kengeri', 'Sankey Road',
       'Malleshwaram', 'Sanjay Nagar', 'Sadashiv Nagar',
       'Basaveshwara Nagar', 'Rajajinagar', 'Yeshwantpur', 'New BEL Road',
       'West Bangalore', 'Magadi Road', 'Yelahanka', 'Sahakara Nagar',
       'Jalahalli', 'Hebbal', 'Nagarbhavi', 'Peenya', 'KR Puram'))

rest_type_ge = st.multiselect('restaurant type', ('Casual Dining', 'Cafe', 'Quick Bites','Delivery', 'Mess', 'Bakery','Dessert Parlor','Pub','Takeaway', 'Delivery','Fine Dining', 'Beverage Shop', 'Sweet Shop', 'Bar','Confectionery', 'Kiosk','Food Truck','Microbrewery', 'Lounge', 'Bar','Food Court','Dhaba', 'Microbrewery','Club','Irani Cafee','Bhojanalya','Pop Up', 'Meat Shop'))

listed_in_types = st.multiselect('type of restaurant',("Delivery",'Dine-out','Desserts','Cafes','Drinks & nightlife','Buffet','Pubs and bars'))

approx_cost=st.slider('approx_cost_for_2',1,10000,100)

cuisineoptions = st.multiselect('type of cuisine',("North Indian","fast food","biryani","continental","Chinese","desserts","Cafe","Mexican","Italian","South Indian","Beverages"))

total_cuisines = len(cuisineoptions)
 
st.sidebar.subheader("About App")

st.sidebar.info("This web app is helps you to find out whether your restaurant is going to successed or not.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check whether your restaurant is going to successed or not")
st.sidebar.info("Don't forget to rate this app")
feedback = st.sidebar.slider('How much would you rate this app?',min_value=0,max_value=5,step=1)

if feedback:
    st.header("Thank you for rating the app!")
    st.info("Caution: This is just a prediction.") 

# convert inputs to DataFrame
df_new = pd.DataFrame ({'online_order': [online_order], 'book_table':[book_table], 'location': [location], 'rest_type_ge': [rest_type_ge],'listed_in_types':[listed_in_types],"approx_cost": [approx_cost], 'total_cuisines': [total_cuisines] })
    
# load transformer
transformer = pkl.load(open('transformer1.pkl','rb'))

#apply transformer on inputs
x_new = transformer.transform(df_new)

# load model                      
model = pkl.load(open('rf.pkl' ,'rb'))


#predict the output
pred= model.predict(x_new)[0]

    
    
if st.button("Predict"):    
  if pred[0] == 0:
    st.error('Warning! this restaurant is not probably going to succeed!')
    
  else:
    st.success('wow, good luck with this successeful resaurant!')
    