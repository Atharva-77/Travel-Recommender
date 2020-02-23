# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask, redirect,	url_for, request
import pandas as pd
import numpy as np

def rec_attraction(tags,days,city):
  attraction_df=pd.read_csv('Attraction.csv')
  attract_list_temp=attraction_df.values.tolist()
  attraction_list=[]
  for i in attract_list_temp:
    if i[3]==city and i[0] in tags:
      attraction_list.append(i)

  n=(days*4)//len(tags)
  final_list=[]
  total=days*4
  j=0
  k=0
  attraction_list.sort(key=lambda x:x[0])
  for i in range(len(attraction_list)-1):
    if attraction_list[i][0]==attraction_list[i+1][0]:
      if j<=n:
        final_list.append(attraction_list[i])
        j+=1
        k+=1
    else:
      j=0
  if j<=n:
   	final_list.append(attraction_list[len(attraction_list)-1])
   	k+=1
  #print(final_list)
    
  for i in attraction_list[:]:
  	if i in final_list:
  		attraction_list.remove(i)
  left=total-k
  for i in range(min(left,len(attraction_list))):
    final_list.append(attraction_list[i])
  for i in attract_list_temp[:]:
    if i in attraction_list or i in final_list:
      attract_list_temp.remove(i)
  if left>len(attraction_list):
    left-=len(attraction_list)
    for i in range(left):
      final_list.append(attract_list_temp[i])
  return final_list[:4*days]


# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 
  
# The route() function of the Flask class is a decorator,  
# which tells the application which URL should call  
# the associated function. 
@app.route('/recommend_attractions') 
# ‘/’ URL is bound with hello_world() function. 
def recommend_attraction():
	tags=request.get_json()['tags']
	days=request.get_json()['days']
	city=request.get_json()['city']
	r=rec_attraction(tags,days,city)
	rec='Recommended Attractions:\n'
	c=0
	k=1
	for i in range(len(r)):
		if c%days==0:
			rec+=(str("Day "+str(k)+'\n'))
			k+=1
		rec+=(str(i+1)+'. '+r[i][2]+'\n')
		c+=1
		if c%days==0:
			rec+='\n\n';
	return rec
  
# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run() 