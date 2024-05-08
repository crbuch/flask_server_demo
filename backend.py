from flask import Flask, request
from flask_ngrok import run_with_ngrok
import uuid
import time
import requests

#dictionary of usernames and passwords (can also be a json file)
known_usernames = {"example_username":"example_password"}

#dictionary of accesstokens and the date they were created
known_accesstokens = {}

app = Flask(__name__) 

#this method should provide you with a public url in the output that acts as a proxy to this server
run_with_ngrok(app) 


@app.route("/Login") 
def login():
    requestBody = request.get_json()

    #when the client makes a request to this endpoint, they need to include the username and password in the request body
    username = requestBody["Username"]
    password = requestBody["Password"]

    #if the username and password are correct
    if known_usernames[username] == password:
       #generates a string of 16 random alpha-numeric characters. This is the auth token
       access_token = uuid.uuid4()

       #we can add the date created so we can remove auth tokens that are older than 60 days for security purposes (this will log the user out)
       date_created = time.time()
       known_accesstokens[access_token] = date_created

       #returns the access token to the client for them to store as a cookie (localstorage)
       return access_token
    else:
       return "Incorrect Password"
    


@app.route("/GetEconData")
def getEcon():
   #here, the client must provide their auth token in order to access this endpoint
   token = request.get_json()["AuthToken"]
   if not token in known_accesstokens.keys():
      return "Unauthorized"
   else:
      #gets the json from the iwell api and forwards it to the client
      econData = requests.request("iwell_api_url_here/")
      return econData





if __name__ == "__main__": 
  app.run()