#OK!
#Author: Luis A. Gonzalez Villalobos
#Date: 3/30/2022
#Project: MindSparkBots - FRED Logic

##==================================================================================
## Libraries
##==================================================================================

import os
import sys
from random import randint
from time import sleep 
from  pycreate2 import Create2
import serial
import firebase_admin
from firebase_admin import credentials, firestore

##==================================================================================
## HELPER FUNCTIONS
##==================================================================================

def batteryCheck(chargeLevel):
    charge = chargeLevel/65535
    return charge

##==================================================================================
## TRANSITIONS
##==================================================================================
'''
Nothing needs to be added in here so far..
If needed, logic may be implemented in the print statement
This will print everytime there is a change in state
'''
class Transition(object):
    # When contructing, we pass it a toState
    # which is going to transition to
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        print("Transitioning...")


##==================================================================================
## STATES
##==================================================================================
'''
Base State listed as Class State
Each created State will inherit from this class
The base object has 3 funtions: enter, execute, and exit
Each new State needs to have implementation for each function
If nothing needs to happen just pass
Shared activities from state can go in the base object
Specific activities per state need to be within the states themselves
'''
class State(object):
    def __init__(self,FSM):
        self.FSM = FSM

    def Enter(self):
        pass
    def Execute (self):                                  
        # Battery check on all state executions
        sensor = bot.get_sensors()
        levelCharge = batteryCheck(sensor.battery_charge)

        # Update DB about charge level
        database = firestore.client()
        result = database.collection('robots').document("1234").get({"battery"}).to_dict() # comment this out
        database.collection('robots').document("1234").update({"battery": result['battery']})

    def Exit(self):
        pass

# First State: TurnRobotOn
class TurnRobotOn(State):
    def __init__(self, FSM):
        super(TurnRobotOn, self).__init__(FSM)

    def Enter(self):
        print("Preparing to turn robot on!")
        super(TurnRobotOn, self).Enter()

        # Start romba and set internal safe state
        bot.start()
        bot.safe()

        # Let App know we can move
        database = firestore.client()  
        database.collection('robots').document("1234").update({"allowMovement": True})

        # Create startup movement path
        path = [
            [-200,-200, 4, 'for'],
            [-100, 100, 1.6, 'turn'],
            [   0,   0, 1, 'stop']
        ]
        # Undocking
        for lft, rht, dt, s in path:
            print(s)
            bot.drive_direct(lft, rht)
            sleep(dt)

    def Execute(self):
        super(TurnRobotOn, self).Execute()
        print("Hello I'm Alfred Botley!")

        # Check state from database
        database = firestore.client()                                       
        result = database.collection('robots').document("1234").get({"state"}).to_dict()

        # Condition to change State
        if(result['state'] != 1):
            if(result['state'] == 0):
                self.FSM.ToTransition("toTurnRobotOff")
            else:
                self.FSM.ToTransition("toSleep")
    
    def Exit(self):
        # if statement here if we want to print different
        # messages depnding on the transition
        print("Moving to a new task...")


# Second State: TurnRobotOff
class TurnRobotOff(State):
    def __init__(self, FSM):
        super(TurnRobotOff, self).__init__(FSM)

    def Enter(self):
        print("Starting to dock!")
        super(TurnRobotOff, self).Enter()

        # Send command for Roomba to start docking
        bot.SCI.write(143)
        print("Docking")

        chargeFlag = True

        while (chargeFlag):
            sensor = bot.get_sensors()
            chargestate = sensor.charger_state
        #    print(chargestate)
            if(chargeFlag >=0 and chargeFlag <=6):
                if (chargestate == 2):
                    chargeFlag = False
                    #print(chargestate)
                else:
                    #print(chargestate)
                    sleep(1)
            else:
                #print(chargestate)
                sleep(1)        
                pass
        
        self.FSM.run = False
        database = firestore.client()  
        database.collection('robots').document("1234").update({"allowMovement": False})

        print('shutting down ... bye')
        bot.drive_stop()
        sleep(0.1)

        # Close the connection
        bot.power()


    def Execute(self):
        super(TurnRobotOff, self).Execute()
        print("Robot is off!")

        # Check state from database
        database = firestore.client()                                       
        result = database.collection('robots').document("1234").get({"state"}).to_dict()

        # Condition to change State
        if(result['state'] != 0):
            if(result['state'] == 1):
                self.FSM.ToTransition("toTurnRobotOn")
            else:
                self.FSM.ToTransition("toSleep")

    def Exit(self):
        print("Waking up!")

# Third State: Sleep
class Sleep(State):
    def __init__(self, FSM):
        super(Sleep, self).__init__(FSM)

    def Enter(self):
        print("Starting to Sleep")
        super(Sleep, self).Enter()
        #bot.drive_stop()
        database = firestore.client()  
        database.collection('robots').document("1234").update({"allowMovement": False})

    def Execute(self):
        super(Sleep, self).Execute()
        print("Sleeping")
        sleep(3)

        # Check state from database
        database = firestore.client()                                       
        result = database.collection('robots').document("1234").get({"state"}).to_dict()

        # Condition to change State
        if(result['state'] != 2):
            if(result['state'] == 0):
                self.FSM.ToTransition("toTurnRobotOff")
            else:
                self.FSM.ToTransition("toTurnRobotOn")
    
    def Exit(self):
        print("Done sleeping!")
        # if statement here if we want to print different
        # messages depnding on the transition

##==================================================================================
## FINITE STATE MACHINE
##==================================================================================
'''
FSM Class
All properties of each FSM are listed in init
Add behaviour that will be executed by FSM in every stage
Implement security to not edit or remove states and attributes
'''
class FSM(object):
    def __init__(self, character):
        self.char = character
        # Store all states and transitions in dictionaries
        self.states = {}
        self.transitions = {}
        # Initialize current state and current transition to none
        self.currState = None
        self.prevState = None # Prevent looping
        self.trans = None
        self.run = True
    
    # Set functions to add transtions, states, and set state
    # This has purposely been made to not allow users to remove a state
    # that may already be in the dictionary for states
    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition

    def AddState(self, stateName, state):
        self.states[stateName] = state
    
    def SetState(self, stateName):
        self.prevState = self.currState
        self.currState = self.states[stateName]

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]

    def Execute(self):
        if(self.trans):
            self.currState.Exit()
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.currState.Enter()
            self.trans = None
        self.currState.Execute()


##==================================================================================
## IMPLEMENTATION
##==================================================================================

# Char base object that inherits from object
Char = type("Char", (object,), {})

# Class Robot that inherits from the Char object
class FREDRobot(Char):
    def __init__(self):
        self.FSM = FSM(self)
        # States
        self.FSM.AddState("Sleep", Sleep(self.FSM))
        self.FSM.AddState("TurnRobotOn", TurnRobotOn(self.FSM))
        self.FSM.AddState("TurnRobotOff", TurnRobotOff(self.FSM))
        # Transitions
        self.FSM.AddTransition("toSleep", Transition("Sleep"))
        self.FSM.AddTransition("toTurnRobotOn", Transition("TurnRobotOn"))
        self.FSM.AddTransition("toTurnRobotOff", Transition("TurnRobotOff"))
        # Default State
        self.FSM.SetState("TurnRobotOff")

    def Execute(self):
        self.FSM.Execute()

# Main
if __name__ == '__main__':
    # Create a Create2.
    #port = "/dev/ttyUSB0"  # serial for raspi
    port = "COM9"           # serial for my laptop
    bot = Create2(port)

    # Open a serial connection to Roomba
    # Some functions are not implemented by PyCreate2
    # Use serial interface to send opcodes for specific commands
    #ser = serial.Serial(port, baudrate=115200)

    # Setup to Communicate with Firestore Database
    cred = credentials.Certificate("robotServiceAccountKey.json")
    firebase_admin.initialize_app(cred)

    # Mark the beggining of the code and verify authentication with Firebase
    print("Database Initialized and Access Granted! Press CTRL+C to exit")

    # Create an FSM instance
    r = FREDRobot()

    try:
        while r.FSM.run:                                                           
            r.Execute()

    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

