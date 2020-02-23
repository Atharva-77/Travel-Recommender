# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, redirect,	url_for, request
import pandas as pd
import numpy as np

def recommend_dest(user_ip):
	user_df=pd.read_csv('User History.csv')

	user_features_df=user_df.pivot_table(index=['Name_of_visited_place'],columns=['User_ID'],values='Rating').fillna(0)

	corrMatrix = user_features_df.corr(method='pearson') #relation of hotels with each other

	def similar(user,count_rec):
	  
	  s=corrMatrix.iloc[user]
	  s.sort_values(ascending=False,inplace=True)
	  data=[]
	  w=0
	  for i in s.index:
	    if i!=s.index[user]:
	      a=(set(user_df[user_df['User_ID']==i]['Name_of_visited_place']).difference(set(user_df[user_df['User_ID']==user]['Name_of_visited_place'])))
	      l=list(a)
	      for j in l:
	        data.append([j,user_df[(user_df['User_ID']==i) & (user_df['Name_of_visited_place']==j)]['Rating'].iloc[0]])
	    w+=1
	    if w>=count_rec:
	      break

	  data.sort(key=lambda x:x[0])
	  c=0
	  total=0
	  data_final=[]
	  for i in range(len(data)-1):
	    if data[i][0]==data[i+1][0]:
	      c+=1
	      total+=data[i][1]
	    else:
	      c+=1
	      total+=data[i][1]
	      data_final.append([data[i][0],total/c])
	      c=0
	      total=0
	  c+=1
	  total+=data[len(data)-1][1]
	  data_final.append([data[len(data)-1][0],total/c])
	      
	  return data_final

	ans=similar(user_ip,5)
	ans.sort(key=lambda x:x[1])
	return ans[:5]

# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 
  
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function. 
@app.route('/recommend_places') 
# ‘/’ URL is bound with hello_world() function. 
def recommend():
	a=int(request.get_json()['user_id'])
	r=recommend_dest(a)
	rec='Recommended Places:\n'
	for i in r:
		rec+=(i[0]+'\n')
	return rec
  
# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run() 