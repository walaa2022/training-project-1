import streamlit as st
import pandas as pd
import pickle as pkl
pip install folium
import folium
import numpy as np
import matplotlib.pyplot as plt


#%%writefile project1.py

import base64
import sklearn
import numpy as np

from sklearn.preprocessing import StandardScaler
scaler= StandardScaler()

#Load the saved model
model= pkl.load(open(r'C:\Users\LENOVO\Downloads\logreg_best.pkl', 'rb'))

st.set_page_config(page_title="Predicting success of new restaurants",page_icon="⚕️",layout="centered",initial_sidebar_state="expanded")


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

approx_cost=st.slider('approx_cost_for_2',1,10000,100)

listed_in_types = st.multiselect('type of restaurant',("Delivery",'Dine-out','Desserts','Cafes','Drinks & nightlife','Buffet','Pubs and bars'))

rest_types = st.multiselect('restaurant type', ('Casual Dining', 'Cafe', 'Quick Bites','Delivery', 'Mess', 'Bakery','Dessert Parlor','Pub','Takeaway', 'Delivery','Fine Dining', 'Beverage Shop', 'Sweet Shop', 'Bar','Confectionery', 'Kiosk','Food Truck','Microbrewery', 'Lounge', 'Bar','Food Court','Dhaba', 'Microbrewery','Club','Irani Cafee','Bhojanalya','Pop Up', 'Meat Shop'))

multiple_types = len(rest_types)

cuisineoptions = st.multiselect('type of cuisine',("North Indian","fast food","biryani","continental","Chinese","desserts","Cafe","Mexican","Italian","South Indian","Beverages"))

total_cuisines = len(cuisineoptions)
 

import folium

# Define city coordinates



# Create a map centered on a specific location
map_center = [12.9715987, 77.5945627]  # Replace with the desired center coordinates
zoom_level = 12  # Adjust the zoom level as needed
map = folium.Map(location=map_center, zoom_start=zoom_level)


# Add markers for each city on the map
city_coordinates = {'BTM':[45.954851,-112.496595],'Koramangala 7th Block':[12.936485,77.613478],'Koramangala 5th Block':[12.934843,77.618977],'Koramangala 4th Block':[12.932778,77.629405],'Koramangala 6th Block':[12.939025,77.623848],'Jayanagar':[27.643927,83.052805],'JP Nagar':[12.265594,76.646540],'Indiranagar':[12.973291,77.640467],'Church Street':[40.709746,-74.011604],'MG Road':[12.975526,77.606790],'Brigade Road':[12.969988,77.606534,],'Lavelle Road':[40.765284,-76.373824],'HSR':[18.147500,41.538889],'Marathahalli':[12.955257,77.698416],'Residency Road':[38.731025,-77.526294],'Whitefield':[53.553368,-2.296902],
'Bannerghatta Road':[12.952180,77.604190],'Brookefield':[33.593506,-79.034563],'Old Airport Road':[31.808596,-94.189266],
'Kammanahalli':[13.009346,77.637709],'Kalyan Nagar':[13.022142,77.640337],'Basavanagudi':[12.941726,77.575502],'Sarjapur Road':[12.920441,77.665328],'Electronic City':[15.675090,73.810836],'Bellandur':[12.931032,77.678247],'Frazer Town':[12.998683,77.615525],
'Malleshwaram':[13.002735,77.570325],'Rajajinagar':[12.988234,77.554883],'Banashankari':[15.887678,75.704678],
'New BEL Road':[13.024348,77.572001]}


for city, coordinates in city_coordinates.items():
    folium.Marker(location=coordinates, popup=city).add_to(map)

# Function to handle click event
def on_map_click(event):
    if event.get('type') == 'click':
        selected_city = event.get('name')
        if selected_city:
            st.session_state.selected_city = selected_city
            st.write("Selected city:", selected_city)
            # Update the selectbox value
            st.session_state.selectbox_value = selected_city

# Convert the map to HTML
map_html = map.get_root().render()

# Display the map in Streamlit
st.components.v1.html(map_html, width=800, height=600, scrolling=True)

# Get the selected city from the user
listed_in_city = st.selectbox("Select a city", list(city_coordinates.keys()), key="selectbox", index=0)
# Process the selected city
if listed_in_city:
    # Perform further actions based on the selected city
    st.write("You selected:", listed_in_city)

st.sidebar.subheader("About App")

st.sidebar.info("This web app is helps you to find out whether your restaurant is going to successed or not.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check whether your restaurant is going to successed or not")
st.sidebar.info("Don't forget to rate this app")
feedback = st.sidebar.slider('How much would you rate this app?',min_value=0,max_value=5,step=1)

if feedback:
    st.header("Thank you for rating the app!")
    st.info("Caution: This is just a prediction.") 

# convert inputs to DataFrame
df_new = pd.DataFrame ({'online_order': [online_order], 'book_table':[book_table], "approx_cost": [approx_cost], 'listed_in(city)': [listed_in_city], 'listed_in(types)':[listed_in_types], 'multiple_types': [multiple_types], 'total_cuisines': [total_cuisines]})
    
# load transformer
transformer = pkl.load(open('transformer.pkl','rb'))

#apply transformer on inputs
x_new = transformer.transform (df_new)

# load model                      
loaded_model = pkl.load(open('clf.pkl' ,'rb'))


#predict the output
predictx= loaded_model.predict(x_new)[0]

    
    
if st.button("Predict"):    
  if pred[0] == 0:
    st.error('Warning! this restaurant is not probably going to succeed!')
    
  else:
    st.success('wow, good luck with this successeful resaurant!')
    
