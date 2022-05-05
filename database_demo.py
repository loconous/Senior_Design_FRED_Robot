#OK!
#Author: Luis A. Gonzalez Villalobos
#Date: 3/22/2022
#Project: MindSparkBots FRED Logic

import os
import sys
import time
from time import sleep, perf_counter
import firebase_admin
from firebase_admin import credentials, firestore

# Setup to Communicate with Firestore Database
cred = credentials.Certificate("robotServiceAccountKey.json")
firebase_admin.initialize_app(cred)

# Mark the beggining of the code and verify authentication with Firebase
print("Database Initialized and Access Granted! Press CTRL+C to exit")


try:
    run = True
    while run:                                                                             
        database = firestore.client()                                                                                  
        result = database.collection('robots').document("1234").get({"state"}).to_dict()
        print(result['state'])



        # result = database.collection('robots').document("1234").get()
        # if result.exists:
        #     print(result.to_dict())

        # database.collection('robots').document("1234").update({"allowMovement": True})
        # sleep(5)

        # database.collection('robots').document("1234").update({"DemoTouch": "I was here"})
        # sleep(5)
        # database.collection('robots').document("1234").update({"DemoTouch": "I am leaving now"})
        # sleep(5)
        # database.collection('robots').document("1234").update({"DemoTouch": "Nobody has been here"})

        run = False

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

