# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, redirect,	url_for, request
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

travel_df=pd.read_csv("travel.csv")

def recommend_hotel(amenities_ip,city_name):
	def rec_hotel(amenities,city):
	  my_dataframe=pd.DataFrame({'Rating':travel_df['Rating'],'Amenities':travel_df['Amenities'],'Hotel Names':travel_df['Hotel Names'],'City':travel_df['City'],'Address':travel_df['Address']})
	  df=pd.DataFrame({"Rating":2,"Amenities":amenities,"Hotel Names":['abc'],"City":[city]})
	  # print(df)
	  my_dataframe=my_dataframe.append(df,ignore_index=True)
	  my_dataframe=my_dataframe[my_dataframe['City']==city]
	  my_dataframe.reset_index(inplace=True)
	  # print(my_dataframe.iloc[-1])
	  # print(my_dataframe)
	  # print(df.columns)

	  tfv = TfidfVectorizer(min_df=3,  max_features=None, strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',ngram_range=(1, 3),stop_words = 'english')
	# Filling NaNs with empty string
	  my_dataframe['Amenities']= my_dataframe['Amenities'].fillna('')
	 # print(amenities)
	  # Fitting the TF-IDF on the 'Amenities' text
	  tfv_matrix = tfv.fit_transform(my_dataframe['Amenities'])
	# Compute the sigmoid kernel
	  sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
	  my_ratings=np.array(my_dataframe[my_dataframe['City']==city]['Rating'])/5
	  indices = pd.Series(my_dataframe.index, index=my_dataframe['Hotel Names']).drop_duplicates()
	  # print(indices)
	  idx = indices['abc']
	  # l=np.add(sig[idx]*0.5,my_ratings)
	  # print("rating:",my_ratings.shape,"sig:",sig[idx].shape)
	    # Get the pairwsie similarity scores 
	  sig_scores = list(enumerate(sig[idx]))

	    # Sort the hotels
	  sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

	    # Scores of the 5 most similar hotels
	  sig_scores = sig_scores[2:7]

	    # Movie indices
	  hotel_indices = [i[0] for i in sig_scores]
	  my_dataframe=my_dataframe.iloc[:-1,:]
	  return my_dataframe[['Hotel Names','Address','Rating']].iloc[hotel_indices]
	 

	df_hotel_list=rec_hotel([amenities_ip],city_name)
	hotel_list=df_hotel_list.values.tolist()
	return hotel_list




# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 
  
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function. 
@app.route('/recommend_hotels') 
# ‘/’ URL is bound with hello_world() function. 
def recommend_hotels():
	a=request.get_json()['amenities']
	am=''
	for i in a:
		am+=i
	b=request.get_json()['city']
	r=recommend_hotel(am,b)
	print("here")
	rec='Recommended Hotels:\n'
	for i in range(len(r)):
		rec+=(str(i+1)+':'+str(r[i][0])+'\n')
		rec+=(str(r[i][1])+'\n')
		rec+=(str(r[i][2])+'\n')
		rec+='\n\n'
	return rec
  
# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run() 